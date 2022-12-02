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


type Action
    = Rock
    | Paper
    | Scissors
    | Invalid


type Move
    = Us Action
    | Them Action


type RoundResults
    = Win Action
    | Draw Action
    | Loss Action


type DesiredOutcome
    = WinDesired
    | LossDesired
    | DrawDesired


toMove : String -> Result String Move
toMove v =
    case v of
        "A" ->
            Ok (Them Rock)

        "B" ->
            Ok (Them Paper)

        "C" ->
            Ok (Them Scissors)

        "X" ->
            Ok (Us Rock)

        "Y" ->
            Ok (Us Paper)

        "Z" ->
            Ok (Us Scissors)

        _ ->
            Err "Unknown move"


toOutcome : String -> Result String DesiredOutcome
toOutcome v =
    case v of
        "X" ->
            Ok LossDesired

        "Y" ->
            Ok DrawDesired

        "Z" ->
            Ok WinDesired

        _ ->
            Err "Unknown outcome"


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
            ul []
                [ li []
                    [ convertInputToMoves contents
                        |> solvePartOne
                        |> String.fromInt
                        |> (++) "Part one: "
                        |> text
                    ]
                , li []
                    [ convertInputToMovesWithDesiredOutcome contents
                        |> solvePartTwo
                        |> String.fromInt
                        |> (++) "Part two: "
                        |> text
                    ]
                ]


solvePartOne : List ( Move, Move ) -> Int
solvePartOne =
    List.foldl followStrategyGuide 0


solvePartTwo : List ( Move, DesiredOutcome ) -> Int
solvePartTwo =
    List.map desiredOutcomeToMoves >> List.foldl followStrategyGuide 0


desiredOutcomeToMoves : ( Move, DesiredOutcome ) -> ( Move, Move )
desiredOutcomeToMoves ( move, outcome ) =
    case ( actionFromMove move, outcome ) of
        ( Rock, WinDesired ) ->
            ( move, Us Paper )

        ( Paper, WinDesired ) ->
            ( Them Paper, Us Scissors )

        ( Scissors, WinDesired ) ->
            ( Them Scissors, Us Rock )

        ( Rock, LossDesired ) ->
            ( Them Rock, Us Scissors )

        ( Paper, LossDesired ) ->
            ( Them Paper, Us Rock )

        ( Scissors, LossDesired ) ->
            ( Them Scissors, Us Paper )

        ( Rock, DrawDesired ) ->
            ( Them Rock, Us Rock )

        ( Paper, DrawDesired ) ->
            ( Them Paper, Us Paper )

        ( Scissors, DrawDesired ) ->
            ( Them Scissors, Us Scissors )

        _ ->
            ( Them Invalid, Us Invalid )


actionFromMove : Move -> Action
actionFromMove move =
    case move of
        Us u ->
            u

        Them t ->
            t


followStrategyGuide : ( Move, Move ) -> Int -> Int
followStrategyGuide moves score =
    score + (calculateRoundResults moves |> roundResultsToPoints)


calculateRoundResults : ( Move, Move ) -> RoundResults
calculateRoundResults moves =
    case moves of
        ( Us u, Them t ) ->
            compareActions ( u, t )

        ( Them t, Us u ) ->
            compareActions ( u, t )

        _ ->
            Loss Invalid


compareActions : ( Action, Action ) -> RoundResults
compareActions actions =
    case actions of
        ( Rock, Paper ) ->
            Loss Rock

        ( Rock, Scissors ) ->
            Win Rock

        ( Scissors, Paper ) ->
            Win Scissors

        ( Scissors, Rock ) ->
            Loss Scissors

        ( Paper, Rock ) ->
            Win Paper

        ( Paper, Scissors ) ->
            Loss Paper

        ( Rock, Rock ) ->
            Draw Rock

        ( Paper, Paper ) ->
            Draw Paper

        ( Scissors, Scissors ) ->
            Draw Scissors

        _ ->
            Loss Invalid


roundResultsToPoints : RoundResults -> Int
roundResultsToPoints result =
    case result of
        Win action ->
            winScore + actionToPoints action

        Draw action ->
            drawScore + actionToPoints action

        Loss action ->
            lossScore + actionToPoints action


actionToPoints : Action -> Int
actionToPoints action =
    case action of
        Rock ->
            rockPoints

        Paper ->
            paperPoints

        Scissors ->
            scissorsPoints

        Invalid ->
            0


convertInputToMoves : String -> List ( Move, Move )
convertInputToMoves input =
    input
        |> String.lines
        |> List.map (String.split " " >> List.map toMove)
        |> List.filterMap
            (\x ->
                case x of
                    [ Ok them, Ok us ] ->
                        Just ( them, us )

                    _ ->
                        Nothing
            )


convertInputToMovesWithDesiredOutcome : String -> List ( Move, DesiredOutcome )
convertInputToMovesWithDesiredOutcome input =
    input
        |> String.lines
        |> List.map (String.split " " >> toMoveWithOutcome)
        |> List.filterMap
            (\x ->
                case x of
                    Ok ( move, outcome ) ->
                        Just ( move, outcome )

                    _ ->
                        Nothing
            )


toMoveWithOutcome : List String -> Result String ( Move, DesiredOutcome )
toMoveWithOutcome v =
    case v of
        [ move, outcome ] ->
            Result.map2 Tuple.pair (toMove move) (toOutcome outcome)

        _ ->
            Err "Invalid input"


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
