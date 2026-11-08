# Agent Guide - advent-of-code

## About this repository

This repository contains my Advent of Code contributions from 2020 onwards.
There is one directory per puzzle, and the language is chosen per puzzle, based
on what I want to learn or what fits that day's challenge. Languages used so far
span C, JavaScript, TypeScript, Python, Ruby, Haskell, Rust, C#, F#, PHP,
Kotlin, and Elm.

## Layout

```
./
├── .agents/               # agent configuration (DotAgents protocol)
├── .git/                  # git internals
├── .github/
│   ├── workflows/         # CI workflow
│   ├── dependabot.yml     # `Dependabot` configuration
│   └── PULL_REQUEST_TEMPLATE.md
├── .idea/                 # JetBrains IDE state, gitignored
├── node_modules/          # installed dependencies, gitignored
├── .venv/                 # Python virtual environment, gitignored
├── 2020/ ... 2025/        # one directory per puzzle year
├── AGENTS.md              # this file
├── CLAUDE.md              # symlink to AGENTS.md
├── LICENSE                # MIT licence
├── README.md              # human-facing documentation
├── biome.json             # `Biome` configuration
├── package.json           # pnpm manifest and per-language scripts
├── pnpm-lock.yaml         # pnpm lockfile
├── pnpm-workspace.yaml    # pnpm workspace settings (year globs)
├── rust-toolchain.toml    # Rust toolchain pin
├── .gitattributes         # git attributes
└── .gitignore             # git ignore rules
```

Each `YYYY/<day> - <name>/` directory is a self-contained puzzle with its input
files and the solution in the chosen language. The root `pnpm-workspace.yaml`
and `package.json` tie the JavaScript and TypeScript puzzles into one workspace
and define the format and lint scripts for every language.

## Commands

| Command               | Purpose                                                        |
| --------------------- | -------------------------------------------------------------- |
| `pnpm format`         | Formats every puzzle language (fans out to the sub-scripts)    |
| `pnpm lint`           | Lints every puzzle language (fans out to the sub-scripts)      |
| `pnpm format:js`      | Formats the JavaScript and TypeScript puzzles with `Biome`     |
| `pnpm format:csharp`  | Formats the C# puzzles with `dotnet format`                    |
| `pnpm format:fsharp`  | Formats the F# puzzles with `fantomas`                         |
| `pnpm format:rust`    | Formats the Rust puzzles with `cargo fmt`                      |
| `pnpm format:ruby`    | Formats the Ruby puzzles with `rubyfmt`                        |
| `pnpm format:haskell` | Formats the Haskell puzzles with `stylish-haskell`             |
| `pnpm format:python`  | Formats the Python puzzles with `black`                        |
| `pnpm lint:js`        | Lints the JavaScript and TypeScript puzzles with `Biome`       |
| `pnpm lint:python`    | Checks the Python puzzles with `black`                         |
| `pnpm lint:rust`      | Checks the Rust puzzles with `cargo fmt` --check               |
| `pnpm lint:ruby`      | Checks the Ruby puzzles with `rubyfmt` --check                 |
| `pnpm lint:haskell`   | Checks the Haskell puzzles with `stylish-haskell`              |
| `pnpm lint:csharp`    | Checks the C# puzzles with `dotnet format` --verify-no-changes |
| `pnpm lint:fsharp`    | Checks the F# puzzles with `fantomas` check                    |

Every change must pass `pnpm lint` before it is complete.

## Standards

The rules in this file and in the `.agents/` tree are authoritative for this
repository. Change them deliberately, in those files, rather than working around
them.

## Tooling

Formatting and linting are done per language. JavaScript and TypeScript use
`Biome`. The other languages use their own formatters and linters, driven by the
`pnpm` scripts. Python tooling runs via the repo's virtual environment.

## Conventions

Never gate a check on a fan-out tool that always exits successfully. Anything
that must fail CI iterates files with a null-delimited `git ls-files` pipeline
instead. Keep puzzle solutions self-contained per directory. Comments are used
sparingly, for the bits that are not obvious from the code, and docstrings or
docblocks are used where a language supports them. The F# formatter is driven
through a direct tool invocation because the .NET formatter does not support F#
projects.

## CI/CD and releases

CI runs on pushes to `main`, on all pull requests, and on manual dispatch,
checking every language. Installing the per-language toolchains in CI is part of
the workflow. There is no CD. `Dependabot` runs monthly across the ecosystems in
use.

## Guardrails

Never disable or skip a lint, format, or check to make a change pass. Fix the
code, not the gate. Never commit generated build output. Never publish or create
releases locally.

## Pointers

- `.agents/agents.md` - the slim agent guidelines for this repository
- `.agents/knowledge/repo-overview/` - the injected repo overview note
- `README.md` - the human-facing documentation

## Open topics

- None.
