module Main (main) where

import           Data.Function (on)
import           Data.List     (groupBy, sortOn)
import           Data.Ord      (Down (..))

data Coord = Coord Int Int
  deriving (Eq, Show)
data LoopEdge = LoopEdge Coord Coord
  deriving (Eq, Show)
data Rect = Rect { tl :: Int
                 , tr :: Int
                 , bl :: Int
                 , br :: Int
                 }
  deriving (Eq, Show)
data FloorLayout = FloorLayout { redTileList      :: [Coord]
                               , layoutDimensions :: Dimensions2D
                               }
  deriving (Eq, Show)
data Dimensions2D = Dimensions2D { width  :: Int
                                 , height :: Int
                                 }
  deriving (Eq, Show)

parseRedTileCoords :: String -> [Coord]
parseRedTileCoords input = map parseLine $ lines input
  where
    parseLine :: String -> Coord
    parseLine line =
        Coord (read x) (read y)
        where
          (x, rest) = break (== ',') line
          y = drop 1 rest

calculateTileLayoutDimensions :: [Coord] -> Dimensions2D
calculateTileLayoutDimensions coords =
  Dimensions2D { width = width, height = height}
  where
    coordX (Coord x _) = x
    coordY (Coord _ y) = y
    width = foldr (max . coordX) 0 coords + 1
    height = foldr (max . coordY) 0 coords + 1

constructTileLayout :: Dimensions2D -> [Coord] -> FloorLayout
constructTileLayout dimensions redTileCoords =
    FloorLayout redTileCoords dimensions

largestRectangle :: FloorLayout -> Bool -> Int
largestRectangle layout isPartOne =
    maximum (0 : map bestRectangleFrom startingTiles)
  where
    redTiles      = redTileList layout
    startingTiles = startingTilesIn
    loopEdges     = wrappingLoopEdges

    wrappingLoopEdges :: [LoopEdge]
    wrappingLoopEdges = case redTiles of
        []       -> []
        (c : cs) -> zipWith LoopEdge (c : cs) (cs ++ [c])

    startingTilesIn :: [Coord]
    startingTilesIn =
        [ tile
        | ys <- groupBy ((==) `on` yOf) (sortOn yOf redTiles)
        , length ys >= 2
        , tile <- ys
        ]
      where
        yOf (Coord _ y) = y

    bestRectangleFrom :: Coord -> Int
    bestRectangleFrom start =
        maximum (0 : map (rectangleArea start) oppositeCorners)
      where
        oppositeCorners =
            filter (cornerIsAllowed start) $
            byFurthestDistance start

    -- The part flag decides which red corner pairs are allowed: any pair in
    -- part one, only pairs inside the red/green loop in part two.
    cornerIsAllowed :: Coord -> Coord -> Bool
    cornerIsAllowed start corner
      | isPartOne = True
      | otherwise = isRectangleWithinLoop start corner

    isRectangleWithinLoop :: Coord -> Coord -> Bool
    isRectangleWithinLoop corner1 corner2 =
        not (hasCrossingEdge rect)
      where
        rect = normaliseRectangle corner1 corner2

    normaliseRectangle :: Coord -> Coord -> Rect
    normaliseRectangle (Coord x1 y1) (Coord x2 y2) =
        Rect { tl = min x1 x2, tr = max x1 x2
             , bl = min y1 y2, br = max y1 y2
             }

    hasCrossingEdge :: Rect -> Bool
    hasCrossingEdge rect = any (edgeCrossesInterior rect) loopEdges

    inHorizontalBounds :: Rect -> Int -> Bool
    inHorizontalBounds rect x = x > tl rect && x < tr rect

    inVerticalBounds :: Rect -> Int -> Bool
    inVerticalBounds rect y = y > bl rect && y < br rect

    overlapsHorizontalSpan :: Rect -> Int -> Int -> Bool
    overlapsHorizontalSpan rect a b = max a b > tl rect && min a b < tr rect

    overlapsVerticalSpan :: Rect -> Int -> Int -> Bool
    overlapsVerticalSpan rect a b = max a b > bl rect && min a b < br rect

    -- Strict inequalities: an edge touching the rectangle boundary is fine,
    -- since boundary tiles are red or green.
    edgeCrossesInterior :: Rect -> LoopEdge -> Bool
    edgeCrossesInterior rect (LoopEdge (Coord x1 y1) (Coord x2 y2))
      | y1 == y2  = inVerticalBounds rect y1 && overlapsHorizontalSpan rect x1 x2
      | x1 == x2  = inHorizontalBounds rect x1 && overlapsVerticalSpan rect y1 y2
      | otherwise = False

    byFurthestDistance :: Coord -> [Coord]
    byFurthestDistance (Coord x y) =
        sortOn (Down . horizontalDistance) $
        sortOn (Down . verticalDistance) $
        filter (/= Coord x y) redTiles
      where
        horizontalDistance (Coord cx _) = abs (cx - x)
        verticalDistance   (Coord _ cy) = abs (cy - y)

    rectangleArea :: Coord -> Coord -> Int
    rectangleArea (Coord x1 y1) (Coord x2 y2) =
        (abs (x2 - x1) + 1) * (abs (y2 - y1) + 1)

solve :: FloorLayout -> Bool -> Int
solve layout isPartOne =
    largestRectangle layout isPartOne

main :: IO ()
main = do
  input <- readFile "input.txt"

  let
    redTileCoords = parseRedTileCoords input
    dimensions = calculateTileLayoutDimensions redTileCoords
    layout = constructTileLayout dimensions redTileCoords

  putStrLn $ (++) "Part one: " $ show $ solve layout True
  putStrLn $ (++) "Part two: " $ show $ solve layout False
