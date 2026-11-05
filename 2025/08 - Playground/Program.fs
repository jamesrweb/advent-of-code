open Playground

[<EntryPoint>]
let main _ =
    let configurationBuilder = ConfigurationBuilder({| isExampleInput = false |})
    let configuration = configurationBuilder.Build()
    let solver = Solver(configuration)

    printfn $"Part one: {solver.SolvePartOne()}"
    printfn $"Part two: {solver.SolvePartTwo()}"

    0
