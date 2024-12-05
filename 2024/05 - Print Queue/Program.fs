open System.IO

type Rule = {| before: int; after: int |}
type Rules = Rule seq
type Pages = int array
type Book = Pages seq

type Ordering =
    | Ordered
    | Unordered

type PageWithOrdering = {| ordering: Ordering; pages: Pages |}
type PagesWithOrdering = PageWithOrdering seq

let toRules (input: string) : Rules =
    input.Split("\n")
    |> Array.map (fun rule ->
        match List.ofArray <| rule.Split "|" with
        | before :: [ after ] ->
            Some
                {| before = int before
                   after = int after |}
        | _ -> None)
    |> Array.filter Option.isSome
    |> Array.map Option.get
    |> Seq.ofArray

let toPages (input: string) : Book =
    input.Split("\n")
    |> Array.map (fun pages ->
        match List.ofArray <| pages.Split "," with
        | [] -> None
        | xs -> Some <| List.map int xs)
    |> Array.filter Option.isSome
    |> Array.map Option.get
    |> Array.map Array.ofList
    |> Seq.ofArray

let toRulesAndPages (input: string array) : Result<{| rules: Rules; book: Book |}, string> =
    match List.ofArray input with
    | rules :: [ pages ] ->
        Ok
            {| rules = toRules rules
               book = toPages pages |}
    | _ -> Error "Missing enough information to generate rules and pages."

let rulesAndPages: {| book: Book; rules: Rules |} =
    File.ReadAllText("./input.txt")
    |> _.Split("\n\n")
    |> toRulesAndPages
    |> Result.defaultWith (fun _ -> {| rules = []; book = [] |})

let orderingOfPages (pages: Pages) (rules: Rules) : Ordering =
    Seq.map
        (fun (rule: Rule) ->
            let containsBefore = Array.contains rule.before pages
            let containsAfter = Array.contains rule.after pages

            if containsBefore && containsAfter then
                let afterIndex = Array.findIndex (fun page -> page = rule.after) pages
                let subset = Array.take afterIndex pages

                if Array.contains rule.before subset then
                    Some Ordered
                else
                    Some Unordered
            else if containsAfter && not containsBefore then
                Some Ordered
            else
                None)
        rules
    |> Seq.filter Option.isSome
    |> Seq.map Option.get
    |> Seq.forall ((=) Ordered)
    |> fun valid -> if valid then Ordered else Unordered

let flip (f: 'a -> 'b -> 'c) (b: 'b) (a: 'a) : 'c = f a b

let reorderPages (pages: Pages) (rules: Rules) : Pages =
    Seq.fold
        (fun (accumulator: Pages) (rule: Rule) ->
            let containsBefore = Array.contains rule.before accumulator
            let containsAfter = Array.contains rule.after accumulator

            if containsBefore && containsAfter then
                let afterIndex = Array.findIndex (fun page -> page = rule.after) accumulator
                let subset = Array.take afterIndex accumulator

                if Array.contains rule.before subset then
                    accumulator
                else
                    Array.removeAt afterIndex accumulator
                    |> (fun ps -> Array.singleton rule.after |> Array.append ps)

            else
                accumulator)
        pages
        rules

let reorderUntilOrderingRulesAreMet (pageWithOrdering: PageWithOrdering) (rules: Rules) =
    if pageWithOrdering.ordering = Ordered then
        pageWithOrdering
    else
        List.fold
            (fun (accumulator: PageWithOrdering) (current: int) ->
                let reorderedPages = reorderPages accumulator.pages rules

                {| pages = reorderedPages
                   ordering = orderingOfPages reorderedPages rules |})
            pageWithOrdering
            [ 0 .. Seq.length pageWithOrdering.pages ]

let toPagesWithOrdering (accumulator: PagesWithOrdering) (pages: Pages) : PagesWithOrdering =
    let pagesWithOrdering =
        {| pages = pages
           ordering = orderingOfPages pages rulesAndPages.rules |}

    Seq.append [ pagesWithOrdering ] accumulator

let partOne: int =
    Seq.fold toPagesWithOrdering [] rulesAndPages.book
    |> Seq.filter (fun pageWithOrdering -> pageWithOrdering.ordering = Ordered)
    |> Seq.map (fun pageWithOrdering ->
        let middle = pageWithOrdering.pages.Length / 2 |> int

        pageWithOrdering.pages[middle])
    |> Seq.sum

let partTwo: int =
    Seq.fold toPagesWithOrdering [] rulesAndPages.book
    |> Seq.filter (fun pageWithOrdering -> pageWithOrdering.ordering = Unordered)
    |> Seq.map (fun pagesWithOrdering -> reorderUntilOrderingRulesAreMet pagesWithOrdering rulesAndPages.rules)
    |> Seq.map (fun pageWithOrdering ->
        let middle = pageWithOrdering.pages.Length / 2 |> int

        pageWithOrdering.pages[middle])
    |> Seq.sum

printfn $"Part one: {partOne}"
printfn $"Part two: {partTwo}"
