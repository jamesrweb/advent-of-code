namespace Playground

type Connection =
    {|
        leftIndex: int
        rightIndex: int
        squaredDistance: int64
    |}

type ConnectionBuilder(configuration: Configuration) =
    static member private SquaredDistance(left: Coordinate3D, right: Coordinate3D) : int64 =
        let differenceX = right.x - left.x
        let differenceY = right.y - left.y
        let differenceZ = right.z - left.z

        pown differenceX 2 + pown differenceY 2 + pown differenceZ 2

    static member private Connections(junctionBoxes: JunctionBoxes) : Connection array =
        let indices = [| 0 .. junctionBoxes.Length - 1 |]

        let createConnection (leftIndex: int, rightIndex: int) =
            {|
                leftIndex = leftIndex
                rightIndex = rightIndex
                squaredDistance = ConnectionBuilder.SquaredDistance(junctionBoxes[leftIndex], junctionBoxes[rightIndex])
            |}

        Array.allPairs indices indices
        |> Array.filter (fun (leftIndex, rightIndex) -> leftIndex < rightIndex)
        |> Array.map createConnection
        |> Array.sortBy _.squaredDistance

    member _.BuildPartOne(junctionBoxes: JunctionBoxes) : Connection array =
        ConnectionBuilder.Connections junctionBoxes
        |> Array.truncate configuration.connectionCount

    member _.BuildPartTwo(junctionBoxes: JunctionBoxes) : Connection array =
        ConnectionBuilder.Connections junctionBoxes
