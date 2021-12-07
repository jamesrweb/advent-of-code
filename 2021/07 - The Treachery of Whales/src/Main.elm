module Main exposing (main)

import Browser
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
                positions =
                    convertInputToPositions contents |> List.sort
            in
            ul []
                [ li [] [ solvePartOne positions |> (++) "Part one: " |> text ]
                , li [] [ solvePartTwo positions |> (++) "Part two: " |> text ]
                ]


solvePartOne : List Int -> String
solvePartOne positions =
    let
        median =
            medianValueInList positions

        cost =
            List.foldl (costReducer median) 0 positions
    in
    String.fromInt cost


solvePartTwo : List Int -> String
solvePartTwo positions =
    let
        mean =
            List.sum positions // List.length positions

        cost =
            List.foldl (realCostReducer mean) 0 positions
    in
    String.fromInt cost


convertInputToPositions : String -> List Int
convertInputToPositions contents =
    List.map mapStringToInt (String.split "," contents)


mapStringToInt : String -> Int
mapStringToInt string =
    Maybe.withDefault 0 (String.toInt string)


drop : List Int -> Int -> List Int
drop list count =
    List.drop count list


medianValueInList : List Int -> Int
medianValueInList list =
    List.length list // 2 |> drop list |> List.head |> Maybe.withDefault 0


triangular : Int -> Int
triangular n =
    (n * (n + 1)) // 2


costReducer : Int -> Int -> Int -> Int
costReducer median position accumulator =
    accumulator + abs (median - position)


realCostReducer : Int -> Int -> Int -> Int
realCostReducer mean position accumulator =
    abs (mean - position) |> triangular |> (+) accumulator



-- HTTP


getInputData : Cmd Msg
getInputData =
    Http.get
        { url = "/input.txt"
        , expect = Http.expectString GotInputData
        }
