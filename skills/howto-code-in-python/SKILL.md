---
name: howto-code-in-python
description: Use when writing, reviewing, or modifying Python code - covers the Ruff/Mypy/uv toolchain, naming, type annotations, idioms and comprehensions, errors and exceptions, dataclasses, imports and module layout, async, and pytest
---

# Writing Python

## Overview

Python house style, distilled from [PEP 8](https://peps.python.org/pep-0008/), [PEP 20](https://peps.python.org/pep-0020/), and [The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/style/). Applies whenever writing, reviewing, or modifying Python code.

Five values, in priority order when they conflict:

1. **Clarity** — a reader can tell what the code does and why.
2. **Simplicity** — it reaches the goal the plainest way available.
3. **Concision** — high signal, low noise.
4. **Maintainability** — it can be changed safely later.
5. **Consistency** — it looks like the code around it.

Clarity breaks ties. Consistency loses them, with one exception: inside a single package, matching the neighbors usually beats being right in isolation.

Prefer the least mechanism. Language construct, then standard library, then an existing dependency, then something new — in that order.

## Non-negotiables

- **`ruff format` everything.** Formatting is not a matter of taste in Python.
- **`ruff check` and `mypy --strict` must pass** before work is done. A `# type: ignore` or `# noqa` needs a specific code and a reason: `# type: ignore[arg-type]  # upstream stub is wrong, see astral-sh/x#123`. Bare ones are banned.
- **Annotate every function signature.** Parameters and return type, including `-> None`. Local variables only when inference fails or the type isn't obvious.
- **4 spaces, never tabs.** Line length is the formatter's problem; leave it at 88 and don't raise it to avoid a wrap.

## Toolchain

One tool per job, all configured in `pyproject.toml`:

| Tool | Job |
|---|---|
| `uv` | Python versions, dependencies, venvs, running, building, publishing |
| `ruff` | Linting (`ruff check`) and formatting (`ruff format`) |
| `mypy` | Type checking |
| `pytest` | Tests |

```toml
[project]
name = "thing"
requires-python = ">=3.11"
dependencies = ["httpx>=0.28"]

[dependency-groups]
dev = ["mypy>=1.15", "pytest>=8", "ruff>=0.9"]

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "D", "SIM", "C4", "RET", "PTH", "RUF"]

[tool.mypy]
strict = true

[build-system]
requires = ["uv_build"]
build-backend = "uv_build"
```

**Ruff:** `select` explicitly, never `extend-select` on top of an implicit default or `select = ["ALL"]`. The set above is a good floor: pycodestyle/Pyflakes for the basics, `I` for import sorting, `N` for PEP 8 naming, `UP` to keep syntax current, `B` for real bugs, `D` for docstrings, `SIM`/`C4`/`RET` for the flabby constructs this guide already forbids, `PTH` to push `os.path` toward `pathlib`. Add `ANN` on a codebase that isn't fully annotated yet, or `S` for security-sensitive code.

**Mypy:** `strict = true` from day one on new code. On an existing untyped codebase, turn strictness on per-module rather than globally weakening it. Never reach for `disallow_untyped_defs = false` as a shortcut. `Any` is a hole in the type system: use `object` when you truly accept anything and narrow with `isinstance`, or a `Protocol` when you mean "something with these methods."

**Version ranges:** lower bounds on what you actually need (`httpx>=0.28`), upper bounds only when you know a specific future version breaks your code.

## Naming

- `snake_case` for functions, methods, variables, modules, and packages. `PascalCase` for classes, type aliases, and `TypeVar`s. `SCREAMING_SNAKE_CASE` for module-level constants. `self` and `cls`, always.
- Module names are short and lowercase; a package name with an underscore is fine when it reads better, but a module named `utils`, `helpers`, `common`, or `misc` describes nothing and becomes a dumping ground. Name the module for what it provides.
- **Scope sets length.** `i` in a two-line comprehension is right; a module-level constant needs a real name. Don't abbreviate to save typing — `response`, not `resp`, unless the surrounding code has already settled on the short form.
- One leading underscore means "internal, don't touch." That's the whole enforcement mechanism, and it's enough. Two leading underscores invoke name mangling and are only for avoiding attribute collisions in a class designed for subclassing — which is almost never what you're doing.
- Don't repeat the module in the name: `http.Client`, not `http.HTTPClient`. Don't prefix getters with `get_` when there's no corresponding action; a plain `owner()` or a `@property` reads better.
- Booleans get `is_`/`has_`/`can_`/`should_` and never a negative: `is_enabled`, not `is_not_disabled`.
- `_` is conventionally throwaway, but it's also `gettext`'s name and the REPL's last-result name. Prefer a named-but-unused variable (`for _index, item in ...`) when clarity is worth more than brevity.

## Comments and docstrings

See `writing-comments` for the general rules. Python-specific:

- Docstrings on public modules, classes, and functions. One line, imperative mood, closing quotes on the same line: `"""Return the parsed config."""`.
- **The annotations are the type documentation.** Don't restate them in a `:param x: (str)` block. Document what a caller can't infer: which exceptions get raised, whether an argument is mutated, thread-safety, ownership of resources.
- Skip the docstring on a private helper whose name and signature already say everything.
- Use [Google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) docstrings.
- A doctest is worth a paragraph of prose.


## Types

- **Builtin generics and PEP 604 unions.** `list[str]`, `dict[str, int]`, `str | None`. Never `List`, `Dict`, `Optional`, or `Union` from `typing` — those spellings are dead.
- Accept the widest type you can use, return the narrowest you can promise: take `Iterable[str]` or `Sequence[str]`, return `list[str]`. Never annotate a parameter as `list` when you only iterate it.
- `Protocol` for structural contracts, defined next to the code that *consumes* it. Reach for `ABC` only when you need shared implementation or runtime enforcement of a real inheritance hierarchy.
- `TypeAlias`-free aliases are fine (`type UserId = str` on 3.12+, plain assignment before that), but a bare alias buys nothing over a comment. When a value needs its own identity, use `NewType` or a frozen dataclass so `UserId` and `OrderId` stop being interchangeable.
- `Literal` for closed string sets in signatures; `enum.StrEnum` when the set needs a name, members, and a home.
- `TypedDict` for JSON-shaped dicts you didn't design. For data you *do* control, use a dataclass — dicts-as-records lose autocompletion, typo-checking, and every method you'd want to hang off them.
- Quote or `from __future__ import annotations` for forward references. Don't add that import reflexively; it changes runtime annotation behavior, which matters to `dataclasses`, `pydantic`, and anything else that reads annotations at runtime.

## Idioms

Python has one obvious way to do most things. Use it.

- **Comprehensions** for map/filter, generator expressions when the result is consumed once or is large. `map`/`filter` with a `lambda` is strictly worse than the comprehension. Nest at most one level; past that, write a loop or a generator function.
- **Unpacking**, not indexing: `for index, item in enumerate(xs)`, `for name, value in d.items()`, `a, b = b, a`, `head, *rest = xs`. `zip(xs, ys, strict=True)` — the `strict` flag turns a silent truncation into an error.
- **`pathlib`**, not `os.path`. `path.read_text()`, `path / "sub" / "file.txt"`, `path.exists()`. String paths are for the boundary where a library demands one.
- **f-strings** for interpolation, `"".join(parts)` for accumulation, `!r` when you want the repr in an error message. The one exception is logging: `logger.info("loaded %s rows", n)` defers formatting until the record is actually emitted, and keeps the message template greppable.
- **Truthiness for emptiness**: `if not items:`, not `if len(items) == 0:`. But `is None` for None, `is not None` for its inverse, and never `== True`.
- **`in` against a `set` or `dict`** for membership, not a list scan. `dict.get(k, default)`, `collections.defaultdict`, and `collections.Counter` exist so you don't hand-roll them.
- **`with` for anything acquired and released.** Files, locks, connections, transactions, temporary state. `contextlib.contextmanager` to write your own; `ExitStack` when the number of resources is dynamic.
- **EAFP over LBYL** where a race is possible or the check duplicates the work: `try: return d[k] except KeyError:` beats `if k in d`. Keep the `try` body to the single line that can actually raise.
- **`match`** only for genuine structural dispatch over shapes. For value dispatch, a dict of handlers or an `if`/`elif` chain is clearer and shorter.
- **Standard library first.** `itertools`, `functools`, `dataclasses`, `datetime`, `pathlib`, `collections`, `contextlib`, `enum`, `json`, `re`, `textwrap`. Reach for a dependency when the stdlib genuinely doesn't cover it, not before.

**Never:**

- Mutable default arguments (`def f(items: list[str] = [])`). The default is created once at definition time and shared across every call. Use `None` and build inside.
- `from module import *`. It hides the origin of every name and breaks every linter's ability to help you.
- Bare `except:` — it swallows `KeyboardInterrupt` and `SystemExit`. Catch the specific exception; `except Exception:` is the widest defensible net.
- Mutating a list while iterating it. Build a new one.
- `eval`, `exec`, or `__import__` on anything derived from input.
- Metaclasses, `__getattr__` dispatch, monkeypatching production code, or decorators that rewrite the signature they wrap. Every one of them makes the code unreadable at the call site to save a few lines at the definition.

## Functions and APIs

- **Keep signatures short.** Four positional parameters is a smell; usually the function is doing two things, or the parameters want to be one object.
- Force clarity at the call site with `*` for keyword-only parameters. `def render(template: str, *, strict: bool = False)` makes `render(t, strict=True)` the only spelling, and boolean positional arguments stop being unreadable.
- `*args`/`**kwargs` only when genuinely forwarding to another callable. As a substitute for naming your parameters, they destroy the signature — for the reader and for mypy.
- `def`, never `name = lambda ...`. A `lambda` belongs inline as a `key=` argument and nowhere else.
- Return one type. A function returning `str | None | list[str]` depending on flags is three functions. Early `return` for guard clauses is good; be consistent about whether the function returns a value at all.
- Generators (`yield`) for streaming and for anything that shouldn't be materialized. Return an iterator when the caller may not need every element.
- **A function that both computes and performs I/O is hard to test.** Split the calculation out as a pure function and let the caller supply the data.

## Classes and data

- **`@dataclass(frozen=True, slots=True)` is the default for a record.** Frozen gets you hashability and rules out a whole class of aliasing bug; slots cuts memory and catches attribute typos. Drop `frozen` only when mutation is the point.
- Use `field(default_factory=list)` for mutable defaults — a plain `= []` on a dataclass field is an error, which is the one place Python protects you from this.
- A class with one method and no state is a function. A class that's only `__init__` and getters is a dataclass. Write the smaller thing.
- Composition over inheritance. Inherit to share an interface, not to reuse a method body.
- `@property` for a cheap derived value that reads like an attribute. If it does I/O, takes an argument, or can be slow, it's a method — the parentheses are the warning label.
- `@functools.cached_property` for expensive derived values on immutable-enough objects; `@functools.lru_cache` only on pure functions with hashable arguments, and never on a method (it keeps `self` alive forever).
- `__repr__` on anything you'll ever see in a traceback or a test failure. `@dataclass` gives you one free.

## Errors

- **Define a package-level base exception and derive from it.** `class ThingError(Exception)`, then `class ConfigError(ThingError)`. Callers get one thing to catch at the boundary and specific types where they need them.
- Never `raise Exception(...)`. It forces callers to catch everything or nothing.
- **`raise ... from err` when re-raising**, so the original traceback survives. `from None` only when the inner exception is a genuine implementation detail that would mislead.
- Attach data as attributes, not by formatting it into the message and making callers parse the string back out.
- Messages are lowercase sentence fragments with no trailing period — they get embedded in longer messages: `f"cannot parse config at {path!r}"`.
- **Don't catch and log.** Handle it or let it propagate; doing both double-reports and takes the decision from the caller. Log at the boundary where you actually decide what to do.
- A swallowed exception needs a comment saying why that's safe. `except Exception: pass` with no explanation is a bug waiting to be filed.
- Validate at the boundary — deserialization, request handling, CLI parsing — and let the interior trust its types. See `defense-in-depth`.

## Modules and layout

- **`src/` layout.** `src/thing/__init__.py`, tests in `tests/` at the root. It makes it impossible to accidentally test the source tree instead of the installed package.
- Absolute imports. Relative imports (`from .parser import parse`) are acceptable within a package; `from ..` reaching up two levels means the module is in the wrong place.
- Imports at the top of the file, grouped stdlib / third-party / local, sorted by `ruff`'s `I` rules. Function-local imports are for breaking an import cycle or deferring a genuinely expensive import — both deserve a comment.
- Import modules, not every name in them: `from collections import abc` then `abc.Sequence`. Importing a handful of names is fine; importing thirty is a sign the module boundary is wrong.
- `__init__.py` re-exports the public API and holds no logic.
- **`if __name__ == "__main__":`** guards every executable script, and the body under it does nothing but call `main()`. Import-time side effects make a module untestable.
- Module-level state is global state. Constants are fine; a mutable module-level dict is a bug that hasn't happened yet.

## Async

Be selective. `async` is for I/O concurrency; everything else stays synchronous. Async spreading into pure logic makes it harder to test and buys nothing.

- `asyncio.run(main())` at the entry point, once.
- **`asyncio.TaskGroup`** for concurrent work — it propagates exceptions and cancels siblings, which `asyncio.gather` does not do properly. Bare `asyncio.create_task` without holding the reference lets the task be garbage-collected mid-flight.
- **Never block the event loop.** No `time.sleep`, no `requests`, no synchronous file I/O in an async function. `asyncio.to_thread` for a blocking call you can't avoid.
- Bounded `asyncio.Queue` and `asyncio.Semaphore` to surface backpressure. Unbounded queues hide it until memory runs out.
- Don't publish both a sync and an async version of the same API. Pick one and let callers bridge.

## Testing

See `writing-good-tests` for what to test, and `property-based-testing` (Hypothesis, in Python) for generative cases. Python-specific:

- **pytest with plain `assert`.** No `unittest.TestCase`, no `assertEqual`, no assertion-helper library — pytest's rewriting already gives you the diff.
- `@pytest.mark.parametrize` for table-driven cases, with `ids=` when the auto-generated names are unreadable.
- Fixtures for setup and teardown, at the narrowest scope that works. `tmp_path` and `monkeypatch` are built in; use them instead of hand-rolled temp directories and global mutation.
- `pytest.raises(SpecificError, match=...)` — assert on the type and something about the message, never on the message alone.
- Test names say what's being verified: `test_parse_rejects_trailing_comma`, not `test_parse_2`.
- Mock at the boundary you own, not deep inside the code under test. A test that patches four internals is testing the implementation, and will break on every refactor.
- Type-check your tests too. They're the first consumer of your API, and an unannotated test suite hides real signature problems.

### Never skip tests

A test that needs an environment variable, credential, network, or fixture must **fail with a clear message** when it's missing. `pytest.mark.skipif`, `pytest.skip()`, and early-return guards turn a missing dependency into a silent pass, so a green suite stops meaning anything. `xfail` is for a known bug with a tracking issue, not for a test you'd rather not fix. If a test can't run, it should be red, not invisible.

## When the guide is silent

Match the surrounding file, then the package. Local consistency covers judgment calls — dataclass versus `NamedTuple`, where to draw a module boundary — but it does not license reintroducing `Optional`, disabling a mypy check, or copying a local pattern that would widen the public API or introduce a bug. Those call for cleanup instead.

## Research before guessing

For an unfamiliar module, an unclear API, or a build failure you can't diagnose immediately, dispatch a research agent instead of iterating by trial and error. They run in isolated context and return summaries.

- `explore-researching-on-the-internet` for package documentation, module versions, and ecosystem conventions.
- Ask that research subagent to inspect remote source when documentation does not reveal how an external repository actually implements something.
