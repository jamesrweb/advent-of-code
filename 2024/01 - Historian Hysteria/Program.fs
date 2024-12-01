open System
open System.IO

type LeftRight = int * int
type Side = int list

type LeftAndRightMappings(lefts: Side, rights: Side) =
    member this.lefts = lefts
    member this.rights = rights

    static member init() : LeftAndRightMappings =
        LeftAndRightMappings(Side.Empty, Side.Empty)

    member this.appendLeft(left: int) =
        let nextLefts = (left :: this.lefts |> List.sort)

        LeftAndRightMappings(nextLefts, this.rights)

    member this.appendRight(right: int) =
        let nextRights = (right :: this.rights |> List.sort)

        LeftAndRightMappings(this.lefts, nextRights)

    member this.appendLeftRight(left: int, right: int) =
        this.appendLeft(left).appendRight right

let aggregateLeftsAndRightsMappings (lrm: LeftAndRightMappings) ((left, right): LeftRight) : LeftAndRightMappings =
    lrm.appendLeftRight (left, right)


let parseInputToLeftAndRightMappings (line: string) : Result<LeftRight, string> =
    let parts = line.Split(null) |> Array.filter (fun entry -> entry <> "")

    if Array.length parts <> 2 then
        Error "Invalid input provided"
    else
        let parsedA, a = Int32.TryParse(parts[0])
        let parsedB, b = Int32.TryParse(parts[1])

        if (parsedA && parsedB) then
            Ok(a, b)
        else
            String.Format("Could not parse either the left or right hand value to an Int32. Received: %d, %d", a, b)
            |> Error

let calculateDistances (lrm: LeftAndRightMappings) : int list =
    List.zip lrm.lefts lrm.rights
    |> List.map (fun (left, right) -> Math.Abs(right - left))

let calculateSimilarityScores (lrm: LeftAndRightMappings) : int list =
    List.countBy id lrm.rights
    |> List.map (fun (right, count) -> if List.contains right lrm.lefts then right * count else 0)

let aggregatedLeftRightMappings =
    File.ReadLines("./input.txt")
    |> Seq.map parseInputToLeftAndRightMappings
    |> Seq.map (fun result -> Result.defaultWith (fun _ -> (0, 0)) result)
    |> Seq.fold aggregateLeftsAndRightsMappings (LeftAndRightMappings.init ())

let partOne = calculateDistances aggregatedLeftRightMappings |> List.sum
let partTwo = calculateSimilarityScores aggregatedLeftRightMappings |> List.sum

printfn $"Part one: {partOne}"
printfn $"Part two: {partTwo}"
