open System
open System.IO

type LetterWithCoordinate =
    { row: int
      column: int
      character: char }

type CharMapWithCoords = LetterWithCoordinate array
type Crossword = CharMapWithCoords array

let rec searchAndCountOccurrencesOfXmasHelper
    (crossword: Crossword)
    ((x, y): int * int)
    ((dx, dy): int * int)
    (search: string)
    : int =
    match Seq.toList search with
    | [] -> 1
    | char :: rest ->
        try
            if (crossword[y][x]).character = char then
                Seq.map Char.ToString rest
                |> String.concat ""
                |> searchAndCountOccurrencesOfXmasHelper crossword (x + dx, y + dy) (dx, dy)
            else
                0
        with _ ->
            0

let searchAndCountOccurrencesOfXmas (crossword: Crossword) : int =
    let mutable count = 0
    let helper = searchAndCountOccurrencesOfXmasHelper crossword

    for direction in [ (0, 1); (1, 0); (0, -1); (-1, 0); (1, 1); (1, -1); (-1, 1); (-1, -1) ] do
        for charMapWithCoords in crossword do
            for letterWithCoordinate in charMapWithCoords do
                count <-
                    count
                    + helper (letterWithCoordinate.column, letterWithCoordinate.row) direction "XMAS"

    count

let searchAndCountOccurrencesOfMasXs (crossword: Crossword) : int =
    let mutable count = 0

    for charMapWithCoords in crossword do
        for letterWithCoordinate in charMapWithCoords do
            try
                let found: bool =
                    [ (0, 0); (1, 1); (2, 2); (2, 0); (1, 1); (0, 2) ]
                    |> Seq.map (fun (dx, dy) ->
                        let cell =
                            crossword[letterWithCoordinate.row + dy][letterWithCoordinate.column + dx]

                        cell.character)
                    |> Seq.windowed 3
                    |> Seq.filter (fun window ->
                        let word = Seq.map Char.ToString window |> String.concat ""

                        word = "MAS" || word = "SAM")
                    |> Seq.length
                    |> (=) 2

                if found then count <- count + 1 else count <- count
            with _ ->
                count <- count

    count

let toCharMapWithCoords ((rowIndex, line): int * string) : CharMapWithCoords =
    line.ToCharArray()
    |> Seq.indexed
    |> Seq.map (fun (columnIndex, character) ->
        { row = rowIndex
          column = columnIndex
          character = character })
    |> Seq.toArray

let crossword: Crossword =
    File.ReadLines("./input.txt")
    |> Seq.indexed
    |> Seq.map toCharMapWithCoords
    |> Seq.toArray

let partOne: int = searchAndCountOccurrencesOfXmas crossword
let partTwo: int = searchAndCountOccurrencesOfMasXs crossword

printfn $"Part one: {partOne}"
printfn $"Part two: {partTwo}"
