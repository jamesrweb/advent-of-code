# Advent of Code

My Advent of Code contributions. Advent of Code is a yearly Advent calendar of
small programming puzzles that can be solved in any language. I use it to learn
languages and practise problem solving, so each puzzle directory under a year
folder uses whichever language I chose for that day's challenge. Each year also
includes a per-year `README.md` summarising each challenge, the language used,
and the stars earned.

## Features

- One self-contained directory per puzzle, `YYYY/<day> - <name>/`, with the
  input files and the solution
- Languages vary per puzzle by choice. `JavaScript`, `TypeScript`, `Python`,
  `Ruby`, `Haskell`, `Rust`, `C`, `C#`, `F#`, `PHP`, `Kotlin`, and `Elm` have
  all been used
- Per-year summaries with per-day results tables

## Installation

Clone the repository and install the root workspace, which covers every puzzle
project that has its own manifest:

```bash
git clone git@github.com:jamesrweb/advent-of-code.git
cd advent-of-code
pnpm install
```

The `pnpm format:*` and `pnpm lint:*` scripts shell out to the per-language
toolchains, so those must be available on the machine too. Rust is pinned by
`rust-toolchain.toml`. The other tools (`black`, `rubyfmt`, `stylish-haskell`,
`dotnet` with `fantomas`) follow the usual install docs for each language.

## Usage

Browse to a puzzle directory and run its solution in that puzzle's language, for
example the 2020 day 1 JavaScript puzzle:

```bash
cd "2020/01 - Report Repair"
node index.js
```

Puzzles with a `package.json` (the JavaScript and TypeScript ones) install via
the root workspace with `pnpm install`.

## Repository layout

```
./
├── .agents/               # agent configuration (DotAgents protocol)
├── .github/               # CI workflow, Dependabot config, PR template
├── 2020/ ... 2025/        # one directory per puzzle, grouped by year
├── .gitattributes         # git attributes
├── .gitignore             # git ignore rules
├── .stylish-haskell.yaml  # Haskell formatter config
├── AGENTS.md              # agent-facing guide
├── biome.json             # Biome config for the JS/TS puzzles
├── CLAUDE.md              # symlink to AGENTS.md
├── LICENSE                # MIT licence
├── package.json           # root scripts fanning out per language
├── pnpm-lock.yaml         # single root lockfile
├── pnpm-workspace.yaml    # workspace member globs
├── README.md              # this file
└── rust-toolchain.toml    # Rust toolchain channel
```

Each puzzle's solution runs with its own language's toolchain. JavaScript
puzzles run with `node`, TypeScript puzzles via their own manifest, Python with
`python3`, Ruby with `ruby`, Haskell with `stylish-haskell`, Rust with `cargo`,
C# and F# with `dotnet`, and Elm puzzles with `elm`.

## Development

The root scripts fan out to every language used across the puzzles:

| Command                                     | Description                                                 |
| ------------------------------------------- | ----------------------------------------------------------- |
| `pnpm format`                               | Formats every puzzle in its own language's formatter        |
| `pnpm lint`                                 | Checks every puzzle in its own language's linter (the gate) |
| `pnpm format:js` / `pnpm lint:js`           | `Biome` format/check for JavaScript and TypeScript puzzles  |
| `pnpm format:csharp` / `pnpm lint:csharp`   | `dotnet format` for the C# puzzles                          |
| `pnpm format:fsharp` / `pnpm lint:fsharp`   | `fantomas` for the F# puzzles                               |
| `pnpm format:rust` / `pnpm lint:rust`       | `cargo fmt` for the Rust puzzles                            |
| `pnpm format:ruby` / `pnpm lint:ruby`       | `rubyfmt` for the Ruby puzzles                              |
| `pnpm format:haskell` / `pnpm lint:haskell` | `stylish-haskell` for the Haskell puzzles                   |
| `pnpm format:python` / `pnpm lint:python`   | `black` for the Python puzzles                              |

The usual flow after changing a puzzle is `pnpm format` and then `pnpm lint`.
Every change must pass `pnpm lint`. CI runs these checks automatically.

## Contributing

This is my personal contributions repository. I add new puzzles each December
during the event.

## Documentation

Each puzzle directory is self-contained. The earlier year directories include a
per-year `README.md` with results tables. Agent-facing docs for this repo live
in `AGENTS.md` and `.agents/`.

## Licence

Licensed under the [MIT Licence](LICENSE).
