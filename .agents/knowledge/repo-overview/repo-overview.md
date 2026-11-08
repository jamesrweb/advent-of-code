---
kind: note
id: repo-overview
title: Repo overview - advent-of-code
context: auto
summary: What the Advent of Code repository is, how puzzles are laid out across languages and years, and how CI checks them.
tags: overview, architecture, advent-of-code, polyglot
---

# Repo overview - advent-of-code

## What this is

Advent of Code contributions from 2020 onwards. One directory per puzzle,
language chosen per puzzle. Languages used so far: C, JavaScript, TypeScript,
Python, Ruby, Haskell, Rust, C#, F#, PHP, Kotlin, and Elm.

## Architecture

- `YYYY/<day> - <name>/` - a self-contained puzzle with input files and the
  solution in the chosen language
- The root `pnpm-workspace.yaml` ties the puzzles that have a `package.json`
  into a single workspace with one root lockfile. Never create nested lockfiles.
  Run `pnpm install` at the root after changing any nested manifest. For the
  other languages the root `package.json` only defines the format and lint
  scripts.
- `rust-toolchain.toml` pins the Rust toolchain.

## Commands

The root scripts fan out per language:

- `pnpm format` / `pnpm lint` run all `format:<lang>` / `lint:<lang>`
  sub-scripts in parallel: `js` (`Biome`), `csharp` and `fsharp`
  (`dotnet format` / `fantomas`), `rust` (`cargo fmt`), `ruby` (`rubyfmt`),
  `haskell` (`stylish-haskell`), `python` (`black`).
- Per-language sub-scripts iterate files with a null-delimited
  `git ls-files -z | xargs --null` pipeline and `cd` into each file's directory.
  Never gate a check on a fan-out tool that always exits 0.
- `pnpm install` installs the whole workspace from the root lockfile.

## CI/CD

CI (`continuous-integration.yml`) runs on pushes to `main`, on all pull
requests, and on manual dispatch. It installs the per-language toolchains
(haskell, ruby, dotnet, python are partly preinstalled on the runner) and runs
`pnpm lint`. Concurrency cancels in-progress runs. There is no CD workflow.
`Dependabot` runs monthly across the npm, NuGet, Composer, Cargo, Elm, and
rust-toolchain ecosystems, each limited to one grouped pull request.

## Conventions

- Puzzle solutions stay self-contained per directory. Comments are used
  sparingly, for non-obvious bits, and docstrings or docblocks where the
  language supports them.
- F# has no support in `dotnet format`, so the F# formatter is invoked directly
  as `dotnet fantomas`.
- The Haskell linter has no check flag, so the check pipes the formatter output
  through `diff`.
