module Main exposing (main)

import Html
import Input


type alias Round =
    { red : Int
    , green : Int
    , blue : Int
    }


type alias Game =
    { id : Int
    , rounds : List Round
    }


type alias Games =
    List Game


type alias Maximums =
    { maxRed : Int, maxGreen : Int, maxBlue : Int }


main =
    let
        games : Games
        games =
            Input.get
                |> String.trim
                |> String.lines
                |> List.map String.trim
                |> List.filterMap toGame
    in
    Html.ul []
        [ Html.li []
            [ Html.text <| "Part one: " ++ (solvePartOne { maxRed = 12, maxGreen = 13, maxBlue = 14 } games |> String.fromInt)
            ]
        , Html.li []
            [ Html.text <| "Part two: " ++ (solvePartTwo games |> String.fromInt)
            ]
        ]


solvePartOne : Maximums -> Games -> Int
solvePartOne settings games =
    List.filter (isValidGame settings) games
        |> List.map .id
        |> List.sum


solvePartTwo : Games -> Int
solvePartTwo games =
    List.map minimumRequiredCubes games
        |> List.map (\round -> round.red * round.green * round.blue)
        |> List.sum


toGame : String -> Maybe Game
toGame line =
    case String.split ": " line of
        gameWithIdString :: roundsString :: [] ->
            let
                id : Maybe Int
                id =
                    gameWithIdString |> String.dropLeft 5 |> String.toInt

                rounds : Maybe (List Round)
                rounds =
                    roundsString
                        |> String.split "; "
                        |> List.map (String.split ", ")
                        |> List.map toRound
                        |> Just
            in
            Maybe.map2 Game id rounds

        _ ->
            Nothing


toRound : List String -> Round
toRound =
    let
        updateRound : String -> Round -> Round
        updateRound word round =
            case String.split " " word of
                countString :: colorString :: [] ->
                    let
                        count : Int
                        count =
                            String.toInt countString |> Maybe.withDefault 0
                    in
                    case colorString of
                        "red" ->
                            { round | red = round.red + count }

                        "green" ->
                            { round | green = round.green + count }

                        "blue" ->
                            { round | blue = round.blue + count }

                        _ ->
                            round

                _ ->
                    round
    in
    List.foldl updateRound { red = 0, green = 0, blue = 0 }


isValidGame : Maximums -> Game -> Bool
isValidGame settings game =
    let
        maximumRed : Int
        maximumRed =
            game.rounds
                |> List.map .red
                |> List.maximum
                |> Maybe.withDefault 0

        maximumGreen : Int
        maximumGreen =
            game.rounds
                |> List.map .green
                |> List.maximum
                |> Maybe.withDefault 0

        maximumBlue : Int
        maximumBlue =
            game.rounds
                |> List.map .blue
                |> List.maximum
                |> Maybe.withDefault 0
    in
    maximumRed <= settings.maxRed && maximumGreen <= settings.maxGreen && maximumBlue <= settings.maxBlue


minimumRequiredCubes : Game -> Round
minimumRequiredCubes game =
    { red =
        game.rounds
            |> List.map .red
            |> List.maximum
            |> Maybe.withDefault 0
    , green =
        game.rounds
            |> List.map .green
            |> List.maximum
            |> Maybe.withDefault 0
    , blue =
        game.rounds
            |> List.map .blue
            |> List.maximum
            |> Maybe.withDefault 0
    }
