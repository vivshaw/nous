# Static Analysis Reference: Configuration, Linting, Formatting

Machine-enforceable half of the house style. Everything here is a starting point to be committed as-is, not a menu. The defaults are strict on purpose.

## The stack

| Tool | Job | Config file |
|---|---|---|
| `typescript` | Type checking | `tsconfig.json` |
| `oxlint` + `oxlint-tsgolint` | Linting, including type-aware rules | `.oxlintrc.json` |
| `oxfmt` | Formatting and import sorting | `.oxfmtrc.json` |
| `knip` | Rmoving unused files, exports, and dependencies | `knip.json` |
| `dpdm` | Circular dependency detection | `dpdm.config.ts` |

```sh
npm i -D typescript oxlint oxlint-tsgolint oxfmt knip dpdm
```

**Oxfmt owns import order.** The linter's sorting rules stay off so the two never fight.

## TypeScript Configuration

Use the latest TypeScript major version. As of the time this document was written, that's version 7.

### `tsconfig.json`

```jsonc
{
  "compilerOptions": {
    // Module resolution. "bundler" for anything behind Vite/webpack/esbuild;
    // "nodenext" for code Node runs directly.
    "moduleResolution": "bundler",
    "moduleDetection": "force",
    "lib": ["esnext", "dom", "dom.iterable"],
    "types": [],

    // strict: true is the TS 7 default and covers noImplicitAny, strictNullChecks,
    // strictFunctionTypes, strictBindCallApply, strictPropertyInitialization,
    // noImplicitThis, alwaysStrict, and useUnknownInCatchVariables. Declared
    // anyway so the intent survives a downgrade.
    "strict": true,

    // Beyond strict. All mandatory. None of these are implied by `strict`.
    "noUncheckedIndexedAccess": true,
    "noPropertyAccessFromIndexSignature": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "allowUnreachableCode": false,
    "allowUnusedLabels": false,

    // Emit and interop discipline
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "erasableSyntaxOnly": true,
    "noEmit": true,
    "skipLibCheck": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### Why these, specifically

| option | what it buys |
|---|---|
| `noUncheckedIndexedAccess` | `arr[i]` and `record[key]` become `T \| undefined`. The single highest-value flag outside `strict` — it makes the most common real-world crash a type error. |
| `noPropertyAccessFromIndexSignature` | Forces `obj["key"]` for index-signature fields, so a typo in a dotted access is caught instead of inferred. |
| `exactOptionalPropertyTypes` | `{a?: string}` no longer accepts `{a: undefined}`. Pairs with the house rule that **`null` means absent** — with both on, `undefined` stops leaking in as a second way to say nothing. |
| `noImplicitOverride` | Renaming a base method no longer silently orphans the subclass override. |
| `noUnusedLocals` / `noUnusedParameters` | Dead locals fail the build rather than accumulating. Prefix genuinely-unused params with `_`. |
| `verbatimModuleSyntax` | Imports are emitted exactly as written, so `import type` is load-bearing rather than cosmetic. Required for `erasableSyntaxOnly` to mean anything. |
| `erasableSyntaxOnly` | Bans enums, parameter properties, and `import =` — TypeScript syntax with runtime behavior. The house style already forbids enums; this enforces it, and keeps files runnable by Node's type stripping. |
| `skipLibCheck` | Skips `.d.ts` checking. Kept on for speed; the tradeoff is real but the alternative is debugging other people's type definitions. |

`isolatedDeclarations` is deliberately absent. Turn it on only for a published library where `.d.ts` build time is a measured problem — it demands explicit types on every export and is a heavy tax elsewhere.

### Path aliases

If needed, you can use path aliases. The aliases resolve through `paths` relative to the tsconfig directory:

```jsonc
{
  "compilerOptions": {
    "paths": {"@/*": ["./src/*"]}
  }
}
```

## Oxlint

### Strictness level

The baseline is: **every built-in category at `error`**, including `pedantic`, `restriction`, and `nursery`, then a curated off-list for the rules that are pure noise or that contradict the house style.

Type-aware rules need `oxlint-tsgolint` and TypeScript 7+.

### `.oxlintrc.json`

```jsonc
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "options": {"typeAware": true},
  "plugins": ["typescript", "import", "promise", "unicorn", "oxc", "eslint", "node", "vitest"],
  "categories": {
    "correctness": "error",
    "suspicious": "error",
    "pedantic": "error",
    "perf": "error",
    "style": "error",
    "restriction": "error",
    "nursery": "error"
  },
  "rules": {
    // ---- House style, enforced ----
    "typescript/array-type": ["error", {"default": "generic"}],
    "typescript/consistent-type-definitions": ["error", "type"],
    "typescript/consistent-type-assertions": ["error", {"assertionStyle": "as"}],
    "typescript/consistent-type-imports": "error",
    "typescript/no-explicit-any": "error",
    "typescript/no-non-null-assertion": "error",
    "typescript/no-unsafe-type-assertion": "error",
    "typescript/no-namespace": "error",
    "typescript/no-require-imports": "error",
    "typescript/no-empty-object-type": "error",
    "typescript/explicit-module-boundary-types": "error",
    "typescript/explicit-function-return-type": [
      "error",
      {"allowExpressions": true, "allowTypedFunctionExpressions": true, "allowHigherOrderFunctions": true}
    ],
    "typescript/ban-ts-comment": [
      "error",
      {"ts-ignore": true, "ts-nocheck": true, "ts-expect-error": {"descriptionFormat": "^: .+"}}
    ],
    "import/no-default-export": "error",
    "oxc/no-barrel-file": ["error", {"threshold": 0}],
    "eslint/eqeqeq": ["error", "always"],
    "eslint/max-params": ["error", 3],
    "unicorn/catch-error-name": ["error", {"name": "error"}],
    "unicorn/error-message": "error",
    "unicorn/throw-new-error": "error",
    "unicorn/prefer-node-protocol": "error",

    // ---- Type-aware. Requires options.typeAware ----
    "typescript/no-floating-promises": "error",
    "typescript/no-misused-promises": "error",
    "typescript/no-unnecessary-condition": "error",
    "typescript/no-unnecessary-type-assertion": "error",
    "typescript/strict-boolean-expressions": "error",
    "typescript/switch-exhaustiveness-check": "error",
    "typescript/prefer-nullish-coalescing": "error",
    "typescript/require-await": "error",
    "typescript/restrict-plus-operands": "error",
    "typescript/use-unknown-in-catch-callback-variable": "error",
    "typescript/no-deprecated": "error",
    "typescript/no-misused-spread": "error",
    "typescript/unbound-method": "error",
    "typescript/no-confusing-void-expression": ["error", {"ignoreArrowShorthand": true}],
    "typescript/no-unsafe-assignment": "error",
    "typescript/no-unsafe-argument": "error",
    "typescript/no-unsafe-call": "error",
    "typescript/no-unsafe-member-access": "error",
    "typescript/no-unsafe-return": "error",
    "typescript/prefer-readonly-parameter-types": "error",

    // ---- Hygiene ----
    "import/no-cycle": "error",
    "import/no-self-import": "error",
    "import/no-duplicates": "error",
    "import/no-mutable-exports": "error",
    "import/no-extraneous-dependencies": "error",
    "import/first": "error",
    "promise/no-return-wrap": "error",
    "promise/prefer-await-to-then": "error",
    "node/no-process-env": "error",
    "eslint/no-console": "error",
    "eslint/no-param-reassign": "error",
    "eslint/no-shadow": ["error", {"hoist": "functions"}],
    "eslint/no-warning-comments": "error",
    "eslint/curly": ["error", "all"],
    "eslint/no-else-return": "error",
    "eslint/prefer-template": "error",
    "eslint/max-lines-per-function": ["error", {"max": 60, "skipBlankLines": true, "skipComments": true}],
    "eslint/max-lines": ["error", {"max": 1500, "skipBlankLines": true, "skipComments": true}],
    "eslint/max-classes-per-file": ["error", 1],
    "eslint/max-nested-callbacks": ["error", 4],

    // ---- Off: conflicts with the house style ----
    "import/prefer-default-export": "off",
    "import/no-named-export": "off",
    "import/no-namespace": "off",
    "import/consistent-type-specifier-style": "off",
    "unicorn/no-null": "off",
    "eslint/no-undefined": "off",
    "unicorn/no-useless-undefined": "off",
    "eslint/func-style": "off",

    // ---- Off: owned by another tool ----
    "eslint/sort-imports": "off",
    "eslint/sort-keys": "off",
    "import/exports-last": "off",
    "import/group-exports": "off",

    // ---- Off: noise from blanket category enablement ----
    "eslint/no-ternary": "off",
    "eslint/no-continue": "off",
    "eslint/no-negated-condition": "off",
    "eslint/no-await-in-loop": "off",
    "eslint/no-void": "off",
    "eslint/id-length": "off",
    "eslint/new-cap": "off",
    "eslint/max-statements": "off",
    "eslint/max-depth": "off",
    "eslint/complexity": "off",
    "eslint/no-magic-numbers": "off",
    "eslint/func-names": "off",
    "eslint/prefer-object-spread": "off",
    "eslint/require-yield": "off",
    "unicorn/filename-case": "off",
    "oxc/no-optional-chaining": "off",
    "oxc/no-rest-spread-properties": "off",
    "oxc/no-map-spread": "off"
  },
  "overrides": [
    {
      "files": ["**/*.{test,spec}.{ts,tsx}", "**/__tests__/**/*.{ts,tsx}"],
      "rules": {
        "typescript/no-explicit-any": "off",
        "typescript/no-unsafe-type-assertion": "off",
        "typescript/no-non-null-assertion": "off",
        "eslint/max-lines-per-function": "off"
      }
    },
    {
      "files": ["**/scripts/**/*.{ts,mts,cts}", "**/*.config.{ts,mts,cts,js,mjs}", "**/tools/**/*.ts"],
      "rules": {
        "eslint/no-console": "off",
        "import/no-default-export": "off",
        "node/no-process-env": "off"
      }
    }
  ]
}
```

## Oxfmt

Oxfmt can format TypeScript as well as sort imports, sort `package.json` fields, and sort Tsilwind classes.

### `.oxfmtrc.jsonc`

```jsonc
{
  "$schema": "./node_modules/oxfmt/configuration_schema.json",

  // Matches the code samples throughout the house style.
  "printWidth": 100,
  "singleQuote": true,
  "bracketSpacing": false,
  "semi": true,
  "trailingComma": "all",
  "arrowParens": "always",

  // Import sorting is DISABLED by default. Turn it on.
  "sortImports": true,

  "sortPackageJson": {"sortScripts": true}
}
```

### Import sorting

`"sortImports": true` enables it with defaults, which already produce the house grouping:

```json
["builtin", "external", ["internal", "subpath"], ["parent", "sibling", "index"], "style", "unknown"]
```

That is Node built-ins → external packages → internal aliases → relative imports, blank line between each group, alphabetical within a group. `internalPattern` defaults to `["~/", "@/", "#"]`, so the conventional `@/` alias is recognized with no extra config. Side-effect imports are left unsorted, on purpose — reordering them can change behavior.


Options that need information from outside the file are unsupported, notably `tsconfigPath`. Classify aliases with `internalPattern` or `customGroups` instead.

Oxfmt honors `.gitignore` and `.prettierignore`, plus `ignorePatterns` in the config.

## Knip

Knip finds dead, unreferenced code: unused files, unused exports, unused dependencies, and dependencies used but never declared. It keeps a codebase from silently accreting cruft.

Knip is considerably more accurate in a codebase with no barrel files. Luckily, we restrict barrel files already.

### `.knip.jsonc`

```jsonc
{
  "$schema": "https://unpkg.com/knip@6/schema.json",
  "entry": ["src/index.ts", "src/main.ts", "scripts/*.ts"],
  "project": ["src/**/*.{ts,tsx}", "scripts/**/*.ts"],

  // Report exports that are only used inside their own file. They should be local.
  "ignoreExportsUsedInFile": false,

  // Entry files get a pass by default. Check them too.
  "includeEntryExports": true,

  // dpdm owns cycle detection. See below.
  "rules": {"cycles": "off"}
}
```

Monorepos configure per-workspace and let the root config stay thin:

```jsonc
{
  "workspaces": {
    ".": {"entry": ["scripts/*.ts"], "project": ["scripts/**/*.ts"]},
    "packages/*": {"entry": ["src/index.ts"], "project": ["src/**/*.ts"]}
  }
}
```

### Running it

- `knip`: The full report.
- `knip --production`: Drops tests, configs, stories, and `devDependencies`. Use when auditing what actually ships.
- `knip --strict`: Implies `--production`, plus workspace isolation and direct-dependency-only checking.
- `knip --fix`: auto-removes unused exports and dependencies. **Read the diff.** It cannot tell a genuinely dead export from one consumed by something knip cannot see.
- `knip --cache`: 10-40% faster on repeat runs.

Escape hatches, in descending order of preference: fix the code, add the file to `entry`, tag the export `@public` via `tags`, and only then `ignoreDependencies` / `ignore`. Reaching for `ignore` first turns knip into decoration.

## Dpdm

Dpdm detects circular imports across the whole graph. It understands `tsconfig.json` path mapping, package-local tsconfigs, and project references, and it prints the **full cycle chain** rather than just flagging a file.

### `dpdm.config.ts`

```typescript
import {defineConfig} from 'dpdm';

export default defineConfig({
  files: ['./src/index.ts'],
  exitCode: 'circular:1',
  transform: true, // ignore type-only imports; they are erased and cannot cycle at runtime
  tree: false,
  warning: false,
  progress: false,
});
```

`dpdm` with no arguments then picks the config up.

Useful invocations:

- `dpdm --no-tree --no-warning ./src/index.ts`: cycles only, human-readable.
- `dpdm -T ./src/index.ts`: skip type-only imports. Almost always what you want, as an `import type` cycle is not a runtime cycle.
- `dpdm --skip-dynamic-imports circular ./src/index.ts`: treat `import()` as a legitimate cycle break, which it is.
- `dpdm --group-by-package './packages/*/src/index.ts'`: monorepo view, cycles grouped by nearest `package.json`.

## Wiring it all together

```jsonc
{
  "scripts": {
    "format": "oxfmt .",
    "format:check": "oxfmt --check .",
    "typecheck": "tsc --noEmit",
    "lint": "oxlint --type-aware",
    "lint:fix": "oxlint --type-aware --fix",
    "deadcode": "knip",
    "cycles": "dpdm",

    "check": "npm run format:check && npm run typecheck && npm run lint && npm run deadcode && npm run cycles"
  }
}
```

**Format locally, verify in CI.** Set up tools like precommit hooks or IDE integrations to automatically format with Oxfmt locally. Then in CI, configure Oxfmt as a blocking check.

## Adopting this on an existing codebase

Turning everything on at once produces thousands of findings and gets the whole config reverted. Ratchet instead:

1. **Formatter first.** Run `oxfmt .` across the repo and commit it alone, as a single mechanical commit. Everything after this has a readable diff.
2. **tsconfig, one flag at a time.** `noUncheckedIndexedAccess` first. Then the rest of the list.
3. **Oxlint categories, escalating.** `correctness` → `suspicious` → `pedantic` → `perf` → `style` → `restriction` → `nursery`. Fix and commit at each step.
4. **Type-aware rules.** Install `oxlint-tsgolint` and turn on `typeAware` last. It is the slowest pass and the one most likely to surface latent async bugs.
5. **Knip and dpdm.** Run both, fix what they find, then wire them into CI and Git hooks so they stay fixed.

Two rules for the whole process:

- **Never silence a finding you have not read.** `// oxlint-disable-next-line` without a comment explaining why is a bug with a lid on it.
- **When you must downgrade a rule, say so in the config.** A `"warn"` with a comment is a tracked debt. A deleted line is an abandoned standard.
