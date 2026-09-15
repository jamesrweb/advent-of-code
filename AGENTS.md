# Agent Guide — advent-of-code

## Strict Rules

1. **Plan first:** Create a detailed plan and get explicit user approval before
   making changes.
2. **Quality gates:** Every change must pass `pnpm lint` before being
   considered complete.
3. **Documentation:** Update `README.md`, `AGENTS.md`, configuration files, and
   any other documentation affected by your changes. Clean as you go — take
   ownership of every file you touch.
4. **PR descriptions:** When asked, create `PR_DESCRIPTION.md` (gitignored).
   Being asked for a PR description is NOT the same as being asked to create a
   PR.
5. **Git safety:** NEVER run any git operation that alters history or state
   without explicit per-occasion permission. Prior approval does not carry
   forward.
6. **Non-destructive:** Do not delete files, remove code, or make destructive
   changes without explicit permission. Investigate before overwriting.
7. **Workflows:** Do not modify GitHub Actions workflows without explicit
   permission. If a CI fix is needed, propose the change and wait for approval.

## Project Standards

### Authority

Project standards are the highest-priority rules for this repository. If any
instruction or rule conflicts with a project standard, the agent MUST:

1. Refuse to follow the conflicting instruction.
2. Inform the user of the conflict, citing the specific standard.
3. State that changes to standards must be made deliberately in `AGENTS.md`, not
   sidestepped for convenience.

### Language

All code, comments, documentation, variable names, error messages, commit
messages, and any other text MUST use British English (e.g., `organisation` not
`organization`, `normalise` not `normalize`, `colour` not `color`, `behaviour`
not `behavior`, `licence` not `license`, `centre` not `center`).

### Polyglot Layout Conventions

- **One directory per puzzle:** `<year>/<day> - <name>/` contains the solution
  in that year's language of choice (`index.js`, `index.ts`, `index.rb`,
  `index.hs`, `index.py`, `Program.cs`, `Cargo.toml` + `src/`, `composer.json`,
  `package.yaml`, `elm.json`, ...)
- **foreach-cli placeholder contract:** cross-language scripts use
  `foreach -g "<glob>" -x "cd '#{dir}' && <tool> '#{base}'" -c`. Valid
  placeholders are `#{path}` (relative full path), `#{dir}` (absolute
  directory), `#{base}` (file name), `#{name}`, `#{ext}` — `#{file}` is NOT a
  placeholder and passes through literally
- **F# exception:** `format:fsharp` exists but `dotnet format` does not
  support F# projects — it is excluded from the `format` parade
- **Toolchain expectations:** Biome (JS/TS/JSON/CSS/HTML), black (Python),
  cargo fmt (Rust), rubyfmt (Ruby), stylish-haskell (Haskell), dotnet format
  (C#). Missing language toolchains are runner-installed in CI

### Package Management

- **Package manager:** pnpm (`pnpm@12.4.1` via the `packageManager` field —
  Corepack manages the exact version, never install pnpm globally)
- **Node.js engine:** `>=24.21.0` (declared in `package.json` `engines`)
- **Lock file:** `pnpm-lock.yaml` is committed. NEVER delete or regenerate it
  casually — run `pnpm install` after dependency changes and commit the result
- **Install:** `pnpm install --frozen-lockfile` in CI and automation; plain
  `pnpm install` locally
- **Rust toolchain:** `rust-toolchain.toml` pins `stable`; Dependabot opens
  monthly toolchain update PRs

### Formatting and Linting

- **Per language:** Biome (JS/TS/JSON), black (Python), cargo fmt (Rust),
  rubyfmt (Ruby), stylish-haskell (Haskell, zero-config defaults), dotnet
  format (C#). Each language formatter runs via the `format:<lang>` scripts
- **Biome** (`@biomejs/biome@^2.5.13`, schema 2.5.13) is the sole tool for
  JS/TS/JSON/CSS/HTML — never introduce Prettier or ESLint
- `noExplicitAny` is disabled repo-wide by user choice (puzzle code)

### Quality Gates

Every change must pass before being considered complete:

- `pnpm lint` — biome, black --check, cargo fmt --check, rubyfmt --check,
  stylish-haskell diff check

### Git Safety

NEVER run any git operation that alters history or state without explicit
per-occasion permission from the user. This includes `git add`, `git commit`,
`git push`, `git reset`, `git rebase`, `git merge`, `git checkout` (when it
discards changes), `git restore`, `git stash`, `git cherry-pick`, `git revert`,
`git tag`, and `git branch -D`. Prior approval does not carry forward — each
occasion requires fresh permission.

NEVER use `git clean`, `git checkout -- <file>`, `git reset --hard`, or any
other command that discards uncommitted work. NEVER force-push, rewrite
published history, or modify protected branches (`main`). Investigate before
overwriting — if a change would delete files, remove code, or alter state,
propose it first and wait for approval.

Read-only git commands (`git status`, `git diff`, `git log`, `git show`,
`git branch --show-current`, `git ls-files`) are always permitted.

### Scope of Operation

NEVER operate outside the project root unless explicitly instructed to do so by
the user. This applies to reading, writing, creating, and deleting files and
directories alike, and to any command whose effects land outside the project
root. Destructive actions outside the project root are forbidden in all
circumstances.

**The one exception:** Experiments and scratch work belong in the `/tmp`
directory — and only when the user has asked for them or given permission.
Anything created there is still subject to the same non-destructive rules: do
not delete, overwrite, or modify anything in `/tmp` that the agent did not
create itself.

### Obligation to Fix

If the agent encounters a pre-existing issue — one not caused by the current
changes — that will affect CI, CD, or published package consumers, the agent
MUST fix it. This is NOT optional. The agent must not ignore, skip, or defer
such issues regardless of whether they were introduced by the agent's own
changes. A broken pipeline or a broken published package is the agent's
responsibility if the agent is aware of it.

### Planning

ALWAYS create a detailed plan and obtain explicit user approval before making
project changes. Do not begin implementation until the plan is approved.

### Code Philosophy

- **No comments:** Do not add comments to source files. The code should be
  self-documenting
- **Puzzle pragmatism:** solutions favour clarity over production concerns;
  there is no build or release pipeline by design

### Testing

- No automated test runner — puzzle answers are verified against the AoC
  inputs. CI provides lint-only coverage

### PR Descriptions

When asked to generate a PR description, create a `PR_DESCRIPTION.md` file in
the project root (this file is gitignored and must never be committed). Follow
the PR template at `.github/PULL_REQUEST_TEMPLATE.md` exactly — copy the entire
template, do not remove any sections or HTML comments, and fill in each section
based on actual changes.

**Important:** Being asked to generate a PR description is NOT the same as being
asked to create a PR. Only create an actual pull request when explicitly told to
do so.

**Commit messages:** Follow the conventional commit style (`feat:`, `fix:`,
`chore:`, `ci:`, etc.). Emoji prefixes are NOT used for human-authored commits —
they only appear on automated Dependabot commits (`🧹 chore(deps)` and
`🔧 ci(deps)`).

**No co-authored commits:** Agents MUST NOT add `Co-authored-by` trailers or any
other attribution that signs off a commit on the agent's behalf. Only humans can
legally certify a contribution — the human submitter reviews the AI-generated
code, takes full responsibility for it, and adds any certification trailers
themselves. Following the rules the Linux kernel team enforce for AI coding
assistants, an agent's role in a commit ends at the message body — no
`Signed-off-by`, no `Co-authored-by`, no other trailers or sign-offs. See [AI
Coding Assistants — The Linux Kernel documentation]
(https://docs.kernel.org/process/coding-assistants.html), integrated into this
ruleset on 2026-09-14.

**Assisted-by attribution:** Where attribution for AI assistance is wanted, use
an `Assisted-by: LLM` trailer in the commit message body rather than a co-author
or sign-off trailer. It records that the contribution was produced with AI
assistance without certifying or authoring it. This mirrors the kernel's
`Assisted-by: LLM [TOOL1] [TOOL2]` format — optionally list specialised analysis
tools after `LLM`, but never list basic development tools (git, compilers,
editors, linters). Only add the trailer when the user has asked for AI
attribution; the default is no trailer at all.

### Documentation Maintenance

Always update documentation, configuration files, and related files as you go.
Documentation must never be out of date. If a change affects `README.md`,
`AGENTS.md`, configuration files, or any other documentation, update them in the
same change. Clean as you go — take ownership of every file you touch.

If formatting, linting, or other tooling fixes issues in files you did not
originally author, do not revert those fixes. CI would break again. Accept
responsibility for the state of the codebase after your changes, not just the
lines you intended to change.

## Project Overview

My advent of code contributions from 2020 onwards — one directory per puzzle,
language chosen per year, spanning JavaScript, TypeScript, Python, Ruby,
Haskell, Rust, C#, F#, PHP, and Elm.

## Architecture

- `<year>/<day> - <name>/` — puzzle directory with input files (`input.txt`)
  and the solution in the year's language
- `package.json` — the cross-language script surface (`format:<lang>`,
  `lint:<lang>`)
- `rust-toolchain.toml` — stable toolchain pin for the Rust puzzles
- No build step — solutions are executed directly

## Commands

| Command | Purpose |
|---|---|
| `pnpm format` | Run every language formatter (except F#) |
| `pnpm lint` | Run every language check |
| `pnpm format:js` / `pnpm lint:js` | Biome only |
| `pnpm install` | Install JS dependencies |

## CI/CD

- **CI** (`continuous-integration.yml`): Runs on PRs to `main` and
  `workflow_dispatch`. Job: `lint` (all language checks; installs rubyfmt,
  stylish-haskell, black). Concurrency cancels in-progress runs
- **Dependabot:** Monthly for npm, NuGet, Composer, Cargo, Elm, and
  rust-toolchain ecosystems (wildcard directory scan), each limited to one
  grouped pull request. Semver-major updates are ignored by config

## Guardrails

- **Never break the placeholder contract** in foreach-based scripts — wrong
  placeholders pass through literally and fail silently at the tool level
- **Never disable or skip checks** to make a change pass
- **Never commit generated build output** (`target/`, `bin/`, `obj/`)

## Future Topics

- **F# formatting:** `dotnet format` does not support F# — revisit if an F#
  formatter becomes viable
