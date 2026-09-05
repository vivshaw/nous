# `Zod` Reference: Schema Validation and Type Inference

Runtime schema validation that infers static TypeScript types from a single declaration.

## Installation
```bash
npm install zod
```

## Core Concept
```typescript
import * as z from 'zod';

const Point = z.object({
  x: z.number(),
  y: z.number(),
});

type Point = z.infer<typeof Point>;  // { x: number; y: number }
```

The schema is the source of truth. Never hand-write a type that duplicates a schema — infer it.

## Parsing

```typescript
Point.parse(value);        // returns typed value, throws ZodError on failure
Point.safeParse(value);    // returns { success: true, data } | { success: false, error }
await Point.parseAsync(value);
await Point.safeParseAsync(value);
```

**Prefer `safeParse` at boundaries.** Errors become values you can route into a `Result`, rather than exceptions thrown from deep inside a call stack.

```typescript
const parsed = Point.safeParse(input);
if (!parsed.success) {
  return err(new ValidationError(z.prettifyError(parsed.error)));
}
return ok(parsed.data);
```

## Type Inference

- `z.infer<typeof S>` — the parsed (output) type
- `z.input<typeof S>` — the accepted input type (differs when transforms or defaults are present)
- `z.output<typeof S>` — alias for `z.infer`

## Schema Constructors

### Primitives
- `z.string()`, `z.number()`, `z.bigint()`, `z.boolean()`, `z.symbol()`
- `z.date()`
- `z.null()`, `z.undefined()`, `z.void()`
- `z.any()`, `z.unknown()`, `z.never()`
- `z.literal('draft')`, `z.literal([200, 201])`
- `z.enum(['red', 'green', 'blue'])`

### Objects & Records
- `z.object({ ... })` — unknown keys are stripped
- `z.strictObject({ ... })` — unknown keys are an error
- `z.looseObject({ ... })` — unknown keys pass through
- `z.record(keySchema, valueSchema)`
- `z.map(keySchema, valueSchema)`, `z.set(schema)`

### Arrays & Tuples
- `z.array(T)` — also `T.array()`
- `z.tuple([A, B])`, `z.tuple([A], RestSchema)`

### Composition
- `z.union([A, B])`
- `z.discriminatedUnion('type', [A, B])` — faster and gives far better errors; use it whenever a tag field exists
- `z.intersection(A, B)`
- `z.lazy(() => Schema)` — recursive types

### Wrappers
- `.optional()` / `z.optional(T)` — allows `undefined`
- `.nullable()` / `z.nullable(T)` — allows `null`
- `.nullish()` — allows both
- `.readonly()` — freezes the parsed output
- `.brand<'UserId'>()` — nominal typing on top of a primitive

### Other
- `z.instanceof(SomeClass)`
- `z.custom<Hex>((v) => typeof v === 'string' && /^0x/.test(v))`
- `z.file()`, `z.json()`
- `z.templateLiteral([z.literal('user_'), z.string()])`
- `z.stringbool()` — parses `'true'` / `'false'` env-var strings

## String Formats

Top-level format schemas, not chained methods:

```typescript
z.email();
z.uuid();
z.url();
z.iso.datetime();
```

Available: `z.email()`, `z.uuid()`, `z.url()`, `z.httpUrl()`, `z.hostname()`, `z.emoji()`, `z.base64()`, `z.base64url()`, `z.hex()`, `z.jwt()`, `z.nanoid()`, `z.cuid()`, `z.ulid()`, `z.ipv4()`, `z.ipv6()`, `z.cidrv4()`, `z.cidrv6()`, `z.mac()`, `z.e164()`, `z.creditCard()`, `z.iso.date()`, `z.iso.time()`, `z.iso.datetime()`, `z.iso.duration()`.

Custom formats: `z.stringFormat('slug', (v) => /^[a-z-]+$/.test(v))`.

## Constraints

**Strings:** `.min()`, `.max()`, `.length()`, `.regex()`, `.includes()`, `.startsWith()`, `.endsWith()`, `.trim()`, `.lowercase()`, `.uppercase()`

**Numbers:** `.gt()`, `.gte()`, `.lt()`, `.lte()`, `.int()`, `.positive()`, `.negative()`, `.multipleOf()`

**Arrays:** `.min()`, `.max()`, `.length()`, `.nonempty()`

```typescript
z.string().min(1).max(120);
z.number().int().gte(0).lte(100);
```

## Object Methods

```typescript
const User = z.object({ id: z.uuid(), name: z.string(), email: z.email() });

User.shape.email;              // reach into a field's schema
User.keyof();                  // z.enum(['id', 'name', 'email'])
User.extend({ role: Role });   // add or override fields
User.pick({ id: true });
User.omit({ email: true });
User.partial();
User.required();
User.catchall(z.unknown());    // schema for unlisted keys
```

## Refinements and Transforms

```typescript
// Extra validation that types can't express
const Password = z.string().min(8).refine(
  (v) => /[0-9]/.test(v),
  { error: 'Password must contain a digit' },
);

// Cross-field validation
const Range = z.object({ start: z.number(), end: z.number() })
  .refine((r) => r.start <= r.end, {
    error: 'start must not exceed end',
    path: ['start'],
  });

// Multiple issues from one check
const Slug = z.string().superRefine((v, ctx) => {
  if (v !== v.toLowerCase()) ctx.addIssue({code: 'custom', message: 'must be lowercase'});
  if (v.includes(' ')) ctx.addIssue({code: 'custom', message: 'must not contain spaces'});
});

// One-way transform (changes the output type)
const Trimmed = z.string().transform((v) => v.trim());

// Chain a second schema after a transform
const NumericId = z.string().transform(Number).pipe(z.number().int());
```

**Refine, don't coerce, at trust boundaries.** `z.coerce.number()` accepts `true` and `[]`; reserve coercion for genuinely stringly-typed inputs (query params, env vars) and prefer `z.stringbool()` / explicit `.pipe()` chains where the intent should be visible.

## Defaults and Fallbacks

```typescript
z.string().default('anonymous');   // applied when input is undefined
z.string().prefault('  x  ');      // default is itself parsed/transformed
z.number().catch(0);               // fallback when validation fails
```

`.default()` makes the field optional in `z.input` but required in `z.infer` — that asymmetry is the point.

## Codecs (Bidirectional Transforms)

```typescript
const IsoDate = z.codec(z.iso.datetime(), z.date(), {
  decode: (s) => new Date(s),
  encode: (d) => d.toISOString(),
});

z.decode(IsoDate, '2026-01-01T00:00:00Z');  // Date
z.encode(IsoDate, new Date());              // string
```

Use codecs when the wire format and the domain model differ and you need both directions — serialization boundaries, DB row mapping.

## Error Handling

```typescript
const result = Schema.safeParse(input);
if (!result.success) {
  result.error.issues;             // structured issues: { code, path, message }
  z.treeifyError(result.error);    // nested shape mirroring the schema
  z.flattenError(result.error);    // { formErrors, fieldErrors } — good for forms
  z.prettifyError(result.error);   // human-readable multi-line string
}
```

Customize messages per-check or per-schema:

```typescript
z.string().min(5, { error: 'Name must be at least 5 characters' });
z.string({ error: 'Name is required' });
```

## Metadata and JSON Schema

```typescript
const Email = z.email().meta({
  title: 'Email address',
  description: 'Primary contact address',
});

z.toJSONSchema(User);
z.toJSONSchema(User, { target: 'draft-2020-12', io: 'input' });
```

Use `z.toJSONSchema()` whenever an actual JSON Schema document is required — OpenAPI specs, config schemas, LLM tool definitions. Options: `target`, `io`, `unrepresentable`, `cycles`, `reused`, `metadata`, `override`, `uri`.

For multiple interlinked schemas, register IDs and convert the registry:

```typescript
z.globalRegistry.add(User, { id: 'User' });
z.toJSONSchema(z.globalRegistry);
```

## Common Patterns

### Boundary validation
```typescript
const ApiResponse = z.object({
  users: z.array(User),
  nextCursor: z.string().nullable(),
});

async function fetchUsers(): Promise<Result<z.infer<typeof ApiResponse>, ValidationError>> {
  const raw: unknown = await (await fetch('/api/users')).json();
  const parsed = ApiResponse.safeParse(raw);
  return parsed.success
    ? ok(parsed.data)
    : err(new ValidationError(z.prettifyError(parsed.error)));
}
```

### Discriminated unions
```typescript
const Event = z.discriminatedUnion('type', [
  z.object({ type: z.literal('click'), x: z.number(), y: z.number() }),
  z.object({ type: z.literal('key'), key: z.string() }),
]);

type Event = z.infer<typeof Event>;  // narrows on `type`
```

### Recursive types
```typescript
const Category = z.object({
  name: z.string(),
  get children() {
    return z.array(Category);
  },
});
```

Getters give inference without an explicit type annotation; `z.lazy()` still works when a getter won't fit.

### Generic schema factories
```typescript
function paginated<T extends z.ZodType>(item: T) {
  return z.object({
    items: z.array(item),
    total: z.number().int().nonnegative(),
  });
}

const PaginatedUsers = paginated(User);
```

### Branded IDs
```typescript
const UserId = z.uuid().brand<'UserId'>();
type UserId = z.infer<typeof UserId>;  // string & z.$brand<'UserId'>
```

A plain `string` no longer assigns to `UserId`, so ID mix-ups become compile errors.

## Performance Notes

- Schemas compile their validators lazily on first parse; hoist schemas to module scope rather than constructing them per call.
- `z.discriminatedUnion` short-circuits on the tag instead of trying every member — much faster than `z.union` for tagged data.
- Reach for `zod/mini` (`import * as z from 'zod/mini'`) only when bundle size is the binding constraint; it trades the chainable API for a functional one (`z.optional(z.string())`, `z.check(...)`) in exchange for a much smaller footprint.
