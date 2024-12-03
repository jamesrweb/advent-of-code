open System.IO
open System.Text.RegularExpressions

let toMatches (withConditionalInstructions: bool) (memoryMap: string) : int option seq =
    let mutable capture = true

    let mapIntegers (group: Match) =
        let found = memoryMap.Substring(group.Index, group.Length)
        let start = "mul(".Length
        let finish = found.Length - 2

        found[start..finish].Split(",") |> Array.map int |> Array.fold (*) 1

    seq {
        for group in Regex.Matches(memoryMap, "don't()|do()|mul\((\d{1,3}),(\d{1,3})\)", RegexOptions.Compiled) do
            if withConditionalInstructions && group.Value.StartsWith("don't") then
                capture <- false
            else if withConditionalInstructions && group.Value.StartsWith("do") then
                capture <- true

            if (not withConditionalInstructions || capture) && group.Value.StartsWith("mul") then
                mapIntegers group |> Some
            else
                None
    }

let matchOptionsToSumEquivalent (option: int option) : int =
    match option with
    | Some value -> value
    | None -> 0

let partOne: int =
    toMatches false (File.ReadAllText("./input.txt"))
    |> Seq.map matchOptionsToSumEquivalent
    |> Seq.sum

let partTwo: int =
    toMatches true (File.ReadAllText("./input.txt"))
    |> Seq.map matchOptionsToSumEquivalent
    |> Seq.sum

printfn $"Part one: {partOne}"
printfn $"Part two: {partTwo}"
