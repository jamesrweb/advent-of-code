module Main exposing (main)

import Browser exposing (element)
import Html exposing (Html, li, pre, text, ul)
import Http exposing (Error(..))
import Maybe exposing (map, map2, map3, withDefault)
import Maybe.Extra exposing (traverse)
import Set exposing (Set)


type alias State =
    { rules : Rules
    , mine : Ticket
    , nearby : Tickets
    }


type alias Rules =
    List Rule


type alias Rule =
    { name : String
    , ranges : Ranges
    }


type alias Ranges =
    List Range


type alias Range =
    { min : Int
    , max : Int
    }


type alias Tickets =
    List Ticket


type alias Ticket =
    List Int


type alias Overview =
    List ( String, Int )


nearbyWithinRange : Rules -> Int -> Bool
nearbyWithinRange rules value =
    rules
        |> List.concatMap .ranges
        |> List.any (inRange value)
        |> not


errorRate : State -> String
errorRate state =
    state.nearby
        |> List.concat
        |> List.filter (nearbyWithinRange state.rules)
        |> List.sum
        |> String.fromInt


validTickets : State -> Tickets
validTickets state =
    List.filter (isValidTicket state.rules) state.nearby


ruleIndex : Rule -> ( Int, Int ) -> Maybe Int
ruleIndex rule ( index, value ) =
    if inRule rule value then
        Just index

    else
        Nothing


applicableRules : Rule -> Ticket -> Set Int
applicableRules rule ticket =
    ticket
        |> List.indexedMap Tuple.pair
        |> List.filterMap (ruleIndex rule)
        |> Set.fromList


ticketsMatchingRule : State -> Rule -> ( String, Ticket )
ticketsMatchingRule state rule =
    validTickets state
        |> List.map (applicableRules rule)
        |> intersections
        |> Set.toList
        |> Tuple.pair rule.name


getOverview : Overview -> List ( String, Ticket ) -> Overview
getOverview solutions candidates =
    case candidates of
        ( name, [ index ] ) :: rest ->
            getOverview
                (( name, index ) :: solutions)
                (List.map (\( k, is ) -> ( k, List.filter (\i -> i /= index) is )) rest)

        _ ->
            solutions


getDepartureInformations : ( String, Int ) -> Maybe Int
getDepartureInformations ( name, index ) =
    if String.startsWith "departure" name then
        Just index

    else
        Nothing


seatOptions : State -> Ticket
seatOptions state =
    let
        targetIndexes =
            state.rules
                |> List.map (ticketsMatchingRule state)
                |> List.sortBy (\( _, indexes ) -> List.length indexes)
                |> getOverview []
                |> List.filterMap getDepartureInformations
                |> Set.fromList
    in
    state.mine
        |> List.indexedMap Tuple.pair
        |> List.filter (\( index, _ ) -> Set.member index targetIndexes)
        |> List.map Tuple.second


intersections : List (Set comparable) -> Set comparable
intersections xs =
    case xs of
        [] ->
            Set.empty

        x :: ys ->
            List.foldl Set.intersect x ys


isValidTicket : Rules -> Ticket -> Bool
isValidTicket rules ticket =
    List.all (\value -> inRules rules value) ticket


inRules : Rules -> Int -> Bool
inRules rules value =
    List.any (\rule -> inRule rule value) rules


inRule : Rule -> Int -> Bool
inRule rule value =
    List.any (\range -> inRange value range) rule.ranges


inRange : Int -> Range -> Bool
inRange value range =
    value >= range.min && value <= range.max


getState : String -> Maybe State
getState string =
    case String.split "\u{000D}\n\u{000D}\n" string of
        [ rules, mine, nearby ] ->
            map3 State
                (parseRules rules)
                (parseMine mine)
                (parseNearbyTickets nearby)

        _ ->
            Nothing


parseRules : String -> Maybe Rules
parseRules string =
    string
        |> String.lines
        |> traverse parseRule


parseRule : String -> Maybe Rule
parseRule string =
    case String.split ": " string of
        [ name, ranges ] ->
            map (Rule name) (parseRanges ranges)

        _ ->
            Nothing


parseRanges : String -> Maybe Ranges
parseRanges string =
    string
        |> String.split " or "
        |> traverse parseRange


parseRange : String -> Maybe Range
parseRange string =
    case String.split "-" string of
        [ min, max ] ->
            map2 Range
                (String.toInt min)
                (String.toInt max)

        _ ->
            Nothing


parseMine : String -> Maybe Ticket
parseMine string =
    case String.words string of
        [ "your", "ticket:", ticket ] ->
            parseTicket ticket

        _ ->
            Nothing


parseTicket : String -> Maybe Ticket
parseTicket string =
    string
        |> String.split ","
        |> traverse String.toInt


parseNearbyTickets : String -> Maybe Tickets
parseNearbyTickets string =
    case String.words string of
        "nearby" :: "tickets:" :: tickets ->
            traverse parseTicket tickets

        _ ->
            Nothing


getInputData : Cmd Msg
getInputData =
    Http.get
        { url = "/src/input.txt"
        , expect = Http.expectString GotInputData
        }


getProduct : State -> String
getProduct state =
    seatOptions state
        |> List.product
        |> String.fromInt


part_one : Maybe State -> String
part_one state =
    state |> map errorRate |> withDefault ""


part_two : Maybe State -> String
part_two state =
    state |> map getProduct |> withDefault ""


type Model
    = Failure Http.Error
    | Loading
    | Success String


init : () -> ( Model, Cmd Msg )
init _ =
    ( Loading, getInputData )


type Msg
    = GotInputData (Result Http.Error String)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GotInputData result ->
            case result of
                Ok data ->
                    ( Success data, Cmd.none )

                Err error ->
                    ( Failure error, Cmd.none )


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none


view : Model -> Html Msg
view model =
    case model of
        Loading ->
            text "Loading..."

        Success data ->
            pre []
                [ ul []
                    [ li [] [ text ("part_one: " ++ part_one (getState data)) ]
                    , li [] [ text ("part_two: " ++ part_two (getState data)) ]
                    ]
                ]

        Failure error ->
            case error of
                BadUrl url ->
                    text ("The URL " ++ url ++ " was invalid")

                Timeout ->
                    text "Unable to reach the server, try again"

                NetworkError ->
                    text "Unable to reach the server, check your network connection"

                BadStatus 500 ->
                    text "The server had a problem, try again later"

                BadStatus 400 ->
                    text "Verify your information and try again"

                BadStatus _ ->
                    text "Unknown error"

                BadBody errorMessage ->
                    text errorMessage


main : Program () Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }
