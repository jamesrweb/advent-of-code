open System.IO

let input = File.ReadAllLines @"input.txt"

type 'T SnailFishNumber =
    | IntegerList of 'T SnailFishNumber list
    | IntegerLiteral of 'T

    static member (+)(left, right) = IntegerList [ left; right ]

let explode snailFishNumber =
    let rec traverseLeft snailFishNumber =
        function
        | IntegerList values ->
            IntegerList [ traverseLeft snailFishNumber values.[0]
                          values.[1] ]
        | IntegerLiteral value -> IntegerLiteral(value + snailFishNumber)

    let rec traverseRight snailFishNumber =
        function
        | IntegerList values ->
            IntegerList [ values.[0]
                          traverseRight snailFishNumber values.[1] ]
        | IntegerLiteral value -> IntegerLiteral(value + snailFishNumber)

    let rec loop depth =
        function
        | IntegerLiteral value -> false, IntegerLiteral value, 0, 0
        | IntegerList values ->
            match values.[0], values.[1] with
            | IntegerLiteral left, IntegerLiteral right ->
                match depth with
                | 4 -> true, IntegerLiteral 0, left, right
                | _ -> false, IntegerList values, 0, 0
            | left, right ->
                let (leftExplosion, leftResult, restLeft, restLeftRight) = loop (depth + 1) left
                let (rightExplosion, rightResult, restRight, restRightLeft) = loop (depth + 1) right

                match leftExplosion, rightExplosion with
                | true, _ ->
                    true,
                    IntegerList [ leftResult
                                  traverseLeft restLeftRight right ],
                    restLeft,
                    0
                | _, true ->
                    true,
                    IntegerList [ traverseRight restRight left
                                  rightResult ],
                    0,
                    restRightLeft
                | _, _ -> false, IntegerList values, 0, 0

    snailFishNumber
    |> loop 0
    |> fun (exploded, number, _, _) -> exploded, number

let integerLiteralToIntegerList integerLiteral =
    IntegerList [ IntegerLiteral(integerLiteral / 2)
                  IntegerLiteral((integerLiteral + 1) / 2) ]

let rec split =
    function
    | IntegerList values ->
        let (firstIsSplit, leftResult) = split values.[0]
        let (secondIsSplit, rightResult) = split values.[1]

        match firstIsSplit, secondIsSplit with
        | true, _ -> true, IntegerList [ leftResult; values.[1] ]
        | _, true -> true, IntegerList [ values.[0]; rightResult ]
        | _, _ -> false, IntegerList values
    | IntegerLiteral value ->
        match value with
        | value when value < 10 -> (false, IntegerLiteral value)
        | _ -> true, integerLiteralToIntegerList value

let rec reduceSnailfishNumber snailFishNumber =
    let (exploded, explodedValue) = explode snailFishNumber
    let (split, splitValue) = split snailFishNumber

    match exploded, split with
    | true, _ -> reduceSnailfishNumber explodedValue
    | _, true -> reduceSnailfishNumber splitValue
    | _, _ -> snailFishNumber

let rec calculateMagnitude =
    function
    | IntegerList values -> (+) (calculateMagnitude values.[0] |> (*) 3) (calculateMagnitude values.[1] |> (*) 2)
    | IntegerLiteral value -> value

let parse line =
    let rec loop =
        function
        | [] -> IntegerList [], []
        | head :: tail ->
            match head with
            | '[' ->
                let (leftFirstPairMember, restLeft) = loop tail
                let leftSecondPairMember = List.tail restLeft
                let (rightFirstPairMember, restRight) = loop leftSecondPairMember
                let rightSecondPairMember = List.tail restRight

                IntegerList [ leftFirstPairMember
                              rightFirstPairMember ],
                rightSecondPairMember
            | _ -> IntegerLiteral(head |> string |> int), tail

    line |> Seq.toList |> loop |> fst

let snailFishNumbers = input |> Seq.map parse

let solvePartOne =
    snailFishNumbers
    |> Seq.reduce (fun augend addend -> augend + addend |> reduceSnailfishNumber)
    |> calculateMagnitude

let solvePartTwo =
    snailFishNumbers
    |> Seq.allPairs snailFishNumbers
    |> Seq.distinct
    |> Seq.map (fun (augend, addend) ->
        augend + addend
        |> reduceSnailfishNumber
        |> calculateMagnitude)
    |> Seq.max

printfn "Part one: %d" solvePartOne
printfn "Part two: %d" solvePartTwo
