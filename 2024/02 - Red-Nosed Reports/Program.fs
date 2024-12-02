open System.IO

type Level = int

type Levels = Level array

type SafetyReport =
    | Safe
    | Unsafe

type LevelSafetyAggregator =
    {| previousLevel: Level
       safetyLevel: SafetyReport |}

let toLevels (line: string) : Levels =
    line.Split(null) |> Array.filter (fun entry -> entry <> "") |> Array.map int

let calculateIfLevelIsSafeInAggregate (accumulator: LevelSafetyAggregator) (level: Level) : LevelSafetyAggregator =
    if accumulator.safetyLevel = Unsafe then
        {| safetyLevel = Unsafe
           previousLevel = level |}
    else if
        level <> accumulator.previousLevel
        && level >= accumulator.previousLevel - 3
        && level <= accumulator.previousLevel + 3
    then
        {| safetyLevel = Safe
           previousLevel = level |}
    else
        {| safetyLevel = Unsafe
           previousLevel = level |}

let calculateIfLevelsAreSafe (levels: Levels) : SafetyReport =
    match Array.toList levels with
    | head :: tail ->
        Seq.fold
            calculateIfLevelIsSafeInAggregate
            {| safetyLevel = Safe
               previousLevel = head |}
            tail
        |> _.safetyLevel
    | [] -> Safe

let levelsAreMonoDirectional (levels: Levels) : bool =
    let ascendingLevels = Array.sort levels

    ascendingLevels = levels || Array.rev ascendingLevels = levels

let calculateSafetyLevelWithoutProblemDampener (levels: Levels) : SafetyReport =
    if levelsAreMonoDirectional levels then
        calculateIfLevelsAreSafe levels
    else
        Unsafe

let calculateSafetyLevelWithProblemDampener (levels: Levels) : SafetyReport =
    let toPossibility (possibilities: Level array list) (index: int) : Level array list =
        let possibility = Array.removeAt index levels |> List.singleton

        List.append possibility possibilities

    let possibilities: Levels list =
        List.fold toPossibility [ levels ] [ 0 .. Array.length levels - 1 ]

    let safetyReports: SafetyReport list =
        List.map calculateSafetyLevelWithoutProblemDampener possibilities

    if List.exists (fun safetyReport -> safetyReport = Safe) safetyReports then
        Safe
    else
        Unsafe

let countSafeSafetyLevelReports (safetyReports: SafetyReport seq) : int =
    Seq.filter (fun safetyReport -> safetyReport = Safe) safetyReports |> Seq.length

let levels: Levels seq = Seq.map toLevels (File.ReadLines("./input.txt"))

let partOne: int =
    Seq.map calculateSafetyLevelWithoutProblemDampener levels
    |> countSafeSafetyLevelReports

let partTwo: int =
    Seq.map calculateSafetyLevelWithProblemDampener levels
    |> countSafeSafetyLevelReports

printfn $"Part one: {partOne}"
printfn $"Part two: {partTwo}"
