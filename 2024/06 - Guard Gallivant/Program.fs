open System
open System.IO

type GuardFacing =
    | Up
    | Down
    | Left
    | Right

type MapItem =
    | Empty
    | Obstacle
    | Guard of GuardFacing

type Map = MapItem array array

let tryGetFacingForGuard (guard: MapItem) : Option<GuardFacing> =
    match guard with
    | Guard facing -> Some facing
    | _ -> None

let toMapItem (character: char) : MapItem =
    match character with
    | '^' -> Guard Up
    | 'v' -> Guard Down
    | '<' -> Guard Left
    | '>' -> Guard Right
    | '#' -> Obstacle
    | _ -> Empty

let inputMap () : Map =
    File.ReadAllLines("./input.txt")
    |> Seq.map _.ToCharArray()
    |> Seq.map (Array.map toMapItem)
    |> Seq.toArray

let tryFindGuardCoordinates (map: Map) : Option<int * int> =
    Array.indexed map
    |> Array.fold
        (fun accumulator (y, row) ->
            if Option.isSome accumulator then
                accumulator
            else
                let index =
                    Array.tryFindIndex
                        (fun item ->
                            match item with
                            | Guard _ -> true
                            | _ -> false)
                        row

                if Option.isNone index then
                    accumulator
                else
                    let x = Option.get index
                    Some(x, y))
        None

let guardHasExitedTheArea (map: Map) : bool =
    let guardIndex = tryFindGuardCoordinates map

    if Option.isNone guardIndex then
        true
    else
        let x, y = Option.get guardIndex
        let facing = tryGetFacingForGuard (map[y][x]) |> Option.get

        let exitedUp = facing = Up && y <= 0
        let exitedDown = facing = Down && y >= Seq.length map - 1
        let exitedLeft = facing = Left && x <= 0
        let exitedRight = facing = Right && x >= (Seq.head map |> Array.length) - 1

        exitedUp || exitedDown || exitedLeft || exitedRight

let isObstacle ((x, y): int * int) (map: Map) : bool =
    try
        map[y][x] = Obstacle
    with _ ->
        false

type SimulatedGuardMoveState =
    {| map: Map
       exited: bool
       stuck: bool
       visited: (int * int) seq |}

let simulateGuardMove (simulatedGuardMoveState: SimulatedGuardMoveState) (index: int) : SimulatedGuardMoveState =
    if simulatedGuardMoveState.exited then
        simulatedGuardMoveState
    else if index = int Int16.MaxValue then
        {| simulatedGuardMoveState with
            exited = true
            stuck = true |}
    else
        let x, y = tryFindGuardCoordinates simulatedGuardMoveState.map |> Option.get
        let facing = tryGetFacingForGuard (simulatedGuardMoveState.map[y][x]) |> Option.get

        let nextSimulatedGuardMoveState =
            {| simulatedGuardMoveState with
                visited = Seq.append simulatedGuardMoveState.visited [ (x, y) ] |}

        match facing with
        | Up ->
            if y > 0 && isObstacle (x, y - 1) nextSimulatedGuardMoveState.map then
                nextSimulatedGuardMoveState.map[y][x] <- Guard Right

                {| nextSimulatedGuardMoveState with
                    exited = guardHasExitedTheArea nextSimulatedGuardMoveState.map |}
            else if y > 0 then
                nextSimulatedGuardMoveState.map[y][x] <- Empty
                nextSimulatedGuardMoveState.map[y - 1][x] <- Guard Up

                {| nextSimulatedGuardMoveState with
                    exited = guardHasExitedTheArea nextSimulatedGuardMoveState.map
                    visited = Seq.append nextSimulatedGuardMoveState.visited [ (x, y - 1) ] |}
            else
                nextSimulatedGuardMoveState.map[y][x] <- Empty

                {| nextSimulatedGuardMoveState with
                    exited = guardHasExitedTheArea nextSimulatedGuardMoveState.map |}

        | Down ->
            if
                y < Array.length nextSimulatedGuardMoveState.map - 1
                && isObstacle (x, y + 1) nextSimulatedGuardMoveState.map
            then
                nextSimulatedGuardMoveState.map[y][x] <- Guard Left

                {| nextSimulatedGuardMoveState with
                    exited = guardHasExitedTheArea nextSimulatedGuardMoveState.map |}
            else if y < Array.length nextSimulatedGuardMoveState.map - 1 then
                nextSimulatedGuardMoveState.map[y][x] <- Empty
                nextSimulatedGuardMoveState.map[y + 1][x] <- Guard Down

                {| nextSimulatedGuardMoveState with
                    exited = guardHasExitedTheArea nextSimulatedGuardMoveState.map
                    visited = Seq.append nextSimulatedGuardMoveState.visited [ (x, y + 1) ] |}
            else
                nextSimulatedGuardMoveState.map[y][x] <- Empty

                {| nextSimulatedGuardMoveState with
                    exited = guardHasExitedTheArea nextSimulatedGuardMoveState.map |}
        | Left ->
            if x > 0 && isObstacle (x - 1, y) nextSimulatedGuardMoveState.map then
                nextSimulatedGuardMoveState.map[y][x] <- Guard Up

                {| nextSimulatedGuardMoveState with
                    exited = guardHasExitedTheArea nextSimulatedGuardMoveState.map |}
            else if x > 0 then
                nextSimulatedGuardMoveState.map[y][x] <- Empty
                nextSimulatedGuardMoveState.map[y][x - 1] <- Guard Left

                {| nextSimulatedGuardMoveState with
                    exited = guardHasExitedTheArea nextSimulatedGuardMoveState.map
                    visited = Seq.append nextSimulatedGuardMoveState.visited [ (x - 1, y) ] |}
            else
                nextSimulatedGuardMoveState.map[y][x] <- Empty

                {| nextSimulatedGuardMoveState with
                    exited = guardHasExitedTheArea nextSimulatedGuardMoveState.map |}

        | Right ->
            if
                x < Array.length nextSimulatedGuardMoveState.map[y] - 1
                && isObstacle (x + 1, y) nextSimulatedGuardMoveState.map
            then
                nextSimulatedGuardMoveState.map[y][x] <- Guard Down

                {| nextSimulatedGuardMoveState with
                    exited = guardHasExitedTheArea nextSimulatedGuardMoveState.map |}
            else if x < Array.length nextSimulatedGuardMoveState.map[y] - 1 then
                nextSimulatedGuardMoveState.map[y][x] <- Empty
                nextSimulatedGuardMoveState.map[y][x + 1] <- Guard Right

                {| nextSimulatedGuardMoveState with
                    exited = guardHasExitedTheArea nextSimulatedGuardMoveState.map
                    visited = Seq.append nextSimulatedGuardMoveState.visited [ (x + 1, y) ] |}
            else
                nextSimulatedGuardMoveState.map[y][x] <- Empty

                {| nextSimulatedGuardMoveState with
                    exited = guardHasExitedTheArea nextSimulatedGuardMoveState.map |}

let guardMoves (map: Map) : SimulatedGuardMoveState =
    Seq.ofList [ 0 .. int Int16.MaxValue ]
    |> Seq.fold
        simulateGuardMove
        {| map = map
           exited = guardHasExitedTheArea map
           stuck = false
           visited = Seq.empty |}

let collectDuplicateVisitationPoints
    (visitedPoints: (int * int) seq)
    (visited: (int * int) seq)
    (point: int * int)
    : (int * int) seq =
    let points = Seq.filter ((=) point) visitedPoints

    if Seq.length points > 1 then
        Seq.append visited [ point ]
    else
        visited

let findDuplicateVisitationPoints (visitedPoints: (int * int) seq) : (int * int) seq =
    Seq.fold (collectDuplicateVisitationPoints visitedPoints) Seq.empty visitedPoints
    |> Seq.distinct

let isLocationWhereBlockingWouldCauseRouteLooping ((x, y): int * int) : bool =
    let nextMap = inputMap ()

    nextMap[y][x] <- Obstacle

    guardMoves nextMap |> _.stuck

let countOfLocationsWhereObstaclesWouldCauseRouteLooping
    (moves: SimulatedGuardMoveState)
    (guardIndex: int * int)
    : int =
    findDuplicateVisitationPoints moves.visited
    |> Seq.append [ Seq.last moves.visited ]
    |> Seq.filter (fun point -> point <> guardIndex)
    |> Seq.filter isLocationWhereBlockingWouldCauseRouteLooping
    |> Seq.length

let partOne: int =
    inputMap () |> guardMoves |> _.visited |> Seq.distinct |> Seq.length

let partTwo: int =
    let map = inputMap ()

    match tryFindGuardCoordinates map with
    | Some index ->
        let moves = guardMoves map

        countOfLocationsWhereObstaclesWouldCauseRouteLooping moves index
    | None -> 0

printfn $"Part one: {partOne}"
printfn $"Part two: {partTwo}"
