namespace Playground

open System.IO

type Coordinate3D = {| x: int64; y: int64; z: int64 |}
type JunctionBoxes = Coordinate3D array

type JunctionBoxesLoader =
    static member Load(path: string) : JunctionBoxes =
        let parseLine (line: string) : Coordinate3D option =
            let coordinates = line.Split(",") |> Array.map int64

            match coordinates with
            | [| x; y; z |] -> Some {| x = x; y = y; z = z |}
            | _ -> None

        File.ReadLines path |> Seq.choose parseLine |> Seq.toArray
