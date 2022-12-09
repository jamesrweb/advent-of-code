module Forest (Forest, setForestVisibilityOrient, setForestVisibility, countVisible, scenicScore) where

import Data.List (foldl', transpose, reverse)
import Tree (Tree, setTreeVisibility, isTreeVisible, viewDistance, treeHeight)

type Forest = [[Tree]]

setForestVisibilityOrient :: Forest -> Forest
setForestVisibilityOrient = fmap setTreeVisibility

setForestVisibility :: Forest -> Forest
setForestVisibility forest = (!!4) $ iterate f forest
  where
        f = rotate . setForestVisibilityOrient
        rotate = (fmap reverse) . transpose

countVisible :: Forest -> Int
countVisible forest = length $ filter isTreeVisible $ concat forest

tracks :: Forest -> Int -> Int -> Forest
tracks forest row column = [reverse left, drop 1 right, reverse up, drop 1 down]
  where (left, right) = splitAt column (forest !! row)
        (up, down) = splitAt row ((transpose forest) !! column)

scenicScore :: Forest -> Int -> Int -> Int
scenicScore forest row column = foldl' (*) 1 $ fmap (viewDistance h) directions
  where directions = tracks forest row column
        h = treeHeight $ (forest !! row) !! column