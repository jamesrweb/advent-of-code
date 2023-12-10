open System
open System.IO

type Race = { Time: UInt64; Record: UInt64 }

let readLines (path: string) : Result<string list, exn> =
    try
        seq {
            use reader = new StreamReader(File.OpenRead(path))

            while not reader.EndOfStream do
                yield reader.ReadLine()
        }
        |> Seq.map (fun string -> string.Trim())
        |> List.ofSeq
        |> Ok
    with ex ->
        Error ex

let totalDistance (race: Race) (buttonPressDurationMs: UInt64) =
    buttonPressDurationMs * (race.Time - buttonPressDurationMs)

let totalDistances (race: Race) =
    List.map (totalDistance race) [ UInt64.MinValue .. race.Time ]

let beatsRecord (race: Race) (distance: UInt64) = distance > race.Record

let winningScenarios (races: Race array) =
    Array.map (fun race -> (race, totalDistances race)) races
    |> Array.map (fun (race: Race, distances) -> (race, List.filter (beatsRecord race) distances))

let solvePartOne (races: Race array) =
    winningScenarios races
    |> Array.map (fun (_, distances: UInt64 list) -> Seq.length distances)
    |> Array.reduce (*)

let solvePartTwo (races: Race array) =
    let time =
        Array.map (fun (race: Race) -> race.Time) races
        |> Array.map Convert.ToString
        |> Array.reduce (+)
        |> UInt64.Parse

    let distance =
        Array.map (fun (race: Race) -> race.Record) races
        |> Array.map Convert.ToString
        |> Array.reduce (+)
        |> UInt64.Parse

    winningScenarios (Array.create 1 { Time = time; Record = distance })
    |> Array.map (fun (_, distances: UInt64 list) -> Seq.length distances)
    |> Array.reduce (*)

let solve (data: string list) : unit =
    let rows =
        List.map (fun (line: string) -> line.Split(" ", StringSplitOptions.RemoveEmptyEntries)) data
        |> List.map (Array.removeAt 0)
        |> List.map (Array.map UInt64.Parse)

    let times_row = List.head rows
    let distance_row = List.head (List.tail rows)

    let races =
        Array.zip times_row distance_row
        |> Array.map (fun (time_ms: UInt64, record_mm: UInt64) -> { Time = time_ms; Record = record_mm })

    printfn "Part one: %A" (solvePartOne races)
    printfn "Part two: %A" (solvePartTwo races)

    ()

match readLines "input.txt" with
| Ok lines -> solve lines
| Error error -> printfn "Error: %A" error.Message
