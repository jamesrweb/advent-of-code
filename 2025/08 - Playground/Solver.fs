namespace Playground

type Solver(configuration: Configuration) =
    let junctionBoxes = JunctionBoxesLoader.Load configuration.path
    let initialCircuits = List.init junctionBoxes.Length Set.singleton
    let connectionBuilder = ConnectionBuilder(configuration)

    static member private Connect (circuits: Set<int> list) (connection: Connection) : Set<int> list =
        let leftCircuits, rest = List.partition (Set.contains connection.leftIndex) circuits
        let rightCircuits, rest = List.partition (Set.contains connection.rightIndex) rest

        match leftCircuits, rightCircuits with
        | [ leftCircuit ], [ rightCircuit ] -> Set.union leftCircuit rightCircuit :: rest
        | [ leftCircuit ], [] -> leftCircuit :: rest
        | [], [ rightCircuit ] -> rightCircuit :: rest
        | [], [] -> Set.ofList [ connection.leftIndex; connection.rightIndex ] :: rest
        | _ -> rest

    member _.SolvePartOne() : int =
        connectionBuilder.BuildPartOne junctionBoxes
        |> Array.fold Solver.Connect initialCircuits
        |> List.map Set.count
        |> List.sortDescending
        |> List.truncate 3
        |> List.reduce (*)

    member _.SolvePartTwo() : int64 =
        let connections = connectionBuilder.BuildPartTwo junctionBoxes

        let distance (connection: Connection) : int64 =
            junctionBoxes[connection.leftIndex].x * junctionBoxes[connection.rightIndex].x

        let circuitStates =
            Seq.scan Solver.Connect initialCircuits connections |> Seq.skip 1

        Seq.zip connections circuitStates
        |> Seq.find (fun (_, circuits) -> List.length circuits = 1)
        |> fst
        |> distance
