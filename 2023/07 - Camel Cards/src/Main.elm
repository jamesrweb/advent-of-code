module Main exposing (main)

import Html exposing (Html)
import Input
import List.Extra


main : Html msg
main =
    let
        hands : List String
        hands =
            Input.get
                |> String.trim
                |> String.lines
    in
    Html.ul []
        [ Html.li []
            [ Html.text <| "Part one: " ++ String.fromInt (solvePartOne hands)
            ]
        , Html.li []
            [ Html.text <| "Part two: " ++ String.fromInt (solvePartTwo hands)
            ]
        ]


jokerValuePartOne : Int
jokerValuePartOne =
    11


jokerValuePartTwo : Int
jokerValuePartTwo =
    1


solvePartOne : List String -> Int
solvePartOne =
    List.filterMap (toHand True)
        >> List.sortWith sortByRank
        >> List.map .bid
        >> List.indexedMap (\index bid -> (index + 1) * bid)
        >> List.sum


solvePartTwo : List String -> Int
solvePartTwo =
    List.filterMap (toHand False)
        >> List.sortWith sortByRank
        >> List.map .bid
        >> List.indexedMap (\index bid -> (index + 1) * bid)
        >> List.sum


type alias CardValue =
    Int


toCardValue : Bool -> Char -> Maybe CardValue
toCardValue isPartOne input =
    case input of
        'A' ->
            Just 14

        'K' ->
            Just 13

        'Q' ->
            Just 12

        'J' ->
            (if isPartOne then
                jokerValuePartOne

             else
                jokerValuePartTwo
            )
                |> Just

        'T' ->
            Just 10

        '9' ->
            Just 9

        '8' ->
            Just 8

        '7' ->
            Just 7

        '6' ->
            Just 6

        '5' ->
            Just 5

        '4' ->
            Just 4

        '3' ->
            Just 3

        '2' ->
            Just 2

        _ ->
            Nothing


type Rank
    = FiveOfAKind
    | FourOfAKind
    | FullHouse
    | ThreeOfAKind
    | TwoPair
    | OnePair
    | HighCard


rankOrder : List Rank
rankOrder =
    [ FiveOfAKind
    , FourOfAKind
    , FullHouse
    , ThreeOfAKind
    , TwoPair
    , OnePair
    , HighCard
    ]


type alias Hand =
    List CardValue


type alias HandInfo =
    { hand : Hand
    , bid : Int
    , rank : Rank
    }


toRank : Bool -> Hand -> Rank
toRank isPartOne hand =
    let
        ( wildcardValues, fixedValues ) =
            List.partition
                ((if isPartOne then
                    jokerValuePartOne

                  else
                    jokerValuePartTwo
                 )
                    |> (==)
                )
                hand

        wildCardValuesCount : Int
        wildCardValuesCount =
            List.length wildcardValues
    in
    if isPartOne then
        List.Extra.gatherEquals hand
            |> List.map (\( _, list ) -> List.length list + 1)
            |> groupCountsToRank

    else if wildCardValuesCount == 5 then
        FiveOfAKind

    else
        List.Extra.gatherEquals fixedValues
            |> List.sortBy (\( _, tail ) -> negate (List.length tail))
            |> List.indexedMap
                (\index ( _, list ) ->
                    let
                        next : Int
                        next =
                            1 + List.length list
                    in
                    if index == 0 then
                        next + wildCardValuesCount

                    else
                        next
                )
            |> groupCountsToRank


groupCountsToRank : List Int -> Rank
groupCountsToRank groupCounts =
    let
        isFiveOfAKind : Bool
        isFiveOfAKind =
            List.member 5 groupCounts

        isFourOfAKind : Bool
        isFourOfAKind =
            List.member 4 groupCounts

        isFullHouse : Bool
        isFullHouse =
            List.member 3 groupCounts && List.member 2 groupCounts

        isThreeOfAKind : Bool
        isThreeOfAKind =
            List.member 3 groupCounts

        isTwoPair : Bool
        isTwoPair =
            List.filter ((==) 2) groupCounts |> List.length |> (==) 2

        isOnePair : Bool
        isOnePair =
            List.member 2 groupCounts
    in
    if isFiveOfAKind then
        FiveOfAKind

    else if isFourOfAKind then
        FourOfAKind

    else if isFullHouse then
        FullHouse

    else if isThreeOfAKind then
        ThreeOfAKind

    else if isTwoPair then
        TwoPair

    else if isOnePair then
        OnePair

    else
        HighCard


toHand : Bool -> String -> Maybe HandInfo
toHand isPartOne input =
    case String.words input of
        handString :: bidString :: [] ->
            let
                hand : Hand
                hand =
                    String.toList handString |> List.filterMap (toCardValue isPartOne)

                bid : Maybe Int
                bid =
                    String.toInt bidString

                rank : Rank
                rank =
                    toRank isPartOne hand
            in
            Maybe.map3 HandInfo (Just hand) bid (Just rank)

        _ ->
            Nothing


sortByRank : HandInfo -> HandInfo -> Order
sortByRank handA handB =
    let
        rankAIndex : Int
        rankAIndex =
            List.Extra.elemIndex handA.rank rankOrder
                |> Maybe.withDefault 0

        rankBIndex : Int
        rankBIndex =
            List.Extra.elemIndex handB.rank rankOrder
                |> Maybe.withDefault 0
    in
    if rankAIndex < rankBIndex then
        GT

    else if rankAIndex > rankBIndex then
        LT

    else
        List.map2 compare handA.hand handB.hand
            |> List.Extra.find ((/=) EQ)
            |> Maybe.withDefault EQ
