open System.IO

type Equation = { test: int64; integers: int64 seq }

type Operator =
    | Add
    | Multiply
    | Concatenate

let apply (operator: Operator) (lhs: int64) (rhs: int64) : int64 =
    match operator with
    | Add -> lhs + rhs
    | Multiply -> lhs * rhs
    | Concatenate -> int64 <| string lhs + string rhs

type PotentialEquationsForOutput =
    {| output: int64
       equations: string seq |}

let parseLineToEquation (line: string) : Equation option =
    match List.ofArray <| line.Split(":") with
    | result :: [ rest ] ->
        let parts = rest.Trim() |> _.Split(" ") |> Array.map int64 |> Seq.ofArray

        Some
            { test = int64 result
              integers = parts }
    | _ -> None

let equations () : Equation seq =
    File.ReadLines "./input.txt"
    |> Seq.map parseLineToEquation
    |> Seq.filter Option.isSome
    |> Seq.map Option.get

let rec isValidEquationHelper (operators: Operator seq) (goal: int64) (current: int64) (rest: int64 seq) : bool =
    if (Seq.isEmpty rest && current <> goal) || current > goal then
        false
    else if current = goal && Seq.isEmpty rest then
        true
    else
        let applyOperator (operator: Operator) : bool =
            let next = Seq.head rest
            let result = apply operator current next

            isValidEquationHelper operators goal result <| Seq.tail rest

        Seq.map applyOperator operators |> Seq.contains true

let isValidEquation (operators: Operator seq) (equation: Equation) : bool =
    match List.ofSeq equation.integers with
    | [] -> false
    | x :: xs -> isValidEquationHelper operators equation.test x xs

let sumValidEquations (operators: Operator seq) (equations: Equation seq) : int64 =
    Seq.filter (isValidEquation operators) equations |> Seq.sumBy _.test

let partOne () : int64 =
    equations () |> sumValidEquations [ Add; Multiply ]

let partTwo () : int64 =
    equations () |> sumValidEquations [ Add; Multiply; Concatenate ]

printfn $"Part one: {partOne ()}"
printfn $"Part two: {partTwo ()}"
