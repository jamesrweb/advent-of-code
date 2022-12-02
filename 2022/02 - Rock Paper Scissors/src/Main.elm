module Main exposing (main)

import Browser
import Dict exposing (Dict)
import Html exposing (..)
import Http
import List



-- MAIN


main : Program () Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }



-- MODEL


type Model
    = Failure
    | Loading
    | Success String


init : () -> ( Model, Cmd Msg )
init _ =
    ( Loading, getInputData )



-- UPDATE


type Msg
    = GotInputData (Result Http.Error String)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg _ =
    case msg of
        GotInputData result ->
            case result of
                Ok contents ->
                    ( Success contents, Cmd.none )

                Err _ ->
                    ( Failure, Cmd.none )



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none



-- VIEW


view : Model -> Html Msg
view model =
    case model of
        Failure ->
            p []
                [ text "Could not load the input data for some reason, is there an input.txt in the `src/` directory?"
                ]

        Loading ->
            p [] [ text "Loading input data..." ]

        Success contents ->
            let
                steps : List ( Char, Char )
                steps =
                    String.lines contents
                        |> List.filter filterEmptyStrings
                        |> List.map removeSpaces
                        |> List.filterMap toActions
            in
            ul []
                [ li []
                    [ steps
                        |> solvePartOne
                        |> String.fromInt
                        |> (++) "Part one: "
                        |> text
                    ]
                , li []
                    [ steps
                        |> solvePartTwo
                        |> String.fromInt
                        |> (++) "Part two: "
                        |> text
                    ]
                ]


solvePartOne : List ( Char, Char ) -> Int
solvePartOne =
    List.map simulateGameStep >> List.sum


solvePartTwo : List ( Char, Char ) -> Int
solvePartTwo =
    List.map simulateDesiredOutcome >> List.sum


simulateGameStep : ( Char, Char ) -> Int
simulateGameStep ( theirs, ours ) =
    let
        ourMoveScore : Int
        ourMoveScore =
            Dict.get ours inputDict |> Maybe.withDefault 0

        theirMoveScore : Int
        theirMoveScore =
            Dict.get theirs inputDict |> Maybe.withDefault 0
    in
    score { ours = ourMoveScore, theirs = theirMoveScore }


simulateDesiredOutcome : ( Char, Char ) -> Int
simulateDesiredOutcome ( theirs, ours ) =
    let
        ourMoveScore : Int
        ourMoveScore =
            Dict.get theirs desiredSolutionDict
                |> Maybe.withDefault Dict.empty
                |> Dict.get ours
                |> Maybe.withDefault 0

        theirMoveScore : Int
        theirMoveScore =
            Dict.get theirs inputDict
                |> Maybe.withDefault 0
    in
    score { ours = ourMoveScore, theirs = theirMoveScore }


score : { ours : Int, theirs : Int } -> Int
score ({ ours, theirs } as scores) =
    if isWin scores then
        ours + winScore

    else if ours == theirs then
        ours + drawScore

    else
        ours + lossScore


isWin : { ours : Int, theirs : Int } -> Bool
isWin { ours, theirs } =
    (theirs == rockPoints && ours == paperPoints)
        || (theirs == paperPoints && ours == scissorsPoints)
        || (theirs == scissorsPoints && ours == rockPoints)


inputDict : Dict Char Int
inputDict =
    Dict.empty
        |> Dict.insert 'A' rockPoints
        |> Dict.insert 'B' paperPoints
        |> Dict.insert 'C' scissorsPoints
        |> Dict.insert 'X' rockPoints
        |> Dict.insert 'Y' paperPoints
        |> Dict.insert 'Z' scissorsPoints


desiredSolutionDict : Dict Char (Dict Char Int)
desiredSolutionDict =
    let
        aDict =
            Dict.empty
                |> Dict.insert 'X' scissorsPoints
                |> Dict.insert 'Y' rockPoints
                |> Dict.insert 'Z' paperPoints

        bDict =
            Dict.empty
                |> Dict.insert 'X' rockPoints
                |> Dict.insert 'Y' paperPoints
                |> Dict.insert 'Z' scissorsPoints

        cDict =
            Dict.empty
                |> Dict.insert 'X' paperPoints
                |> Dict.insert 'Y' scissorsPoints
                |> Dict.insert 'Z' rockPoints
    in
    Dict.empty
        |> Dict.insert 'A' aDict
        |> Dict.insert 'B' bDict
        |> Dict.insert 'C' cDict


filterEmptyStrings : String -> Bool
filterEmptyStrings =
    String.trim >> String.isEmpty >> not


removeSpaces : String -> String
removeSpaces =
    String.filter ((==) ' ' >> not)


toActions : String -> Maybe ( Char, Char )
toActions line =
    case String.toList line of
        [ theirs, ours ] ->
            Just ( theirs, ours )

        _ ->
            Nothing


winScore : Int
winScore =
    6


drawScore : Int
drawScore =
    3


lossScore : Int
lossScore =
    0


rockPoints : Int
rockPoints =
    1


paperPoints : Int
paperPoints =
    2


scissorsPoints : Int
scissorsPoints =
    3



-- HTTP


getInputData : Cmd Msg
getInputData =
    Http.get
        { url = "/input.txt"
        , expect = Http.expectString GotInputData
        }
