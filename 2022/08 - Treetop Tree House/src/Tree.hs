module Tree (Tree, readTree, isTreeVisible, treeHeight, setTreeVisibility, viewDistance) where

import Data.List (foldl')
import Lib (takeWhile1)

type Height = Int
type Visible = Bool

data Tree = Tree Height Visible
  deriving (Show, Eq)

readTree :: Char -> Tree
readTree h = Tree (read [h]) False

isTreeVisible :: Tree -> Bool
isTreeVisible (Tree _ v) = v

treeHeight :: Tree -> Int
treeHeight (Tree h _) = h

setTreeVisibility :: [Tree] -> [Tree]
setTreeVisibility row = reverse $ snd $ foldl' vis (-1, []) row
  where vis (highest, tagged) (Tree height visible)
          | height > highest = (height, (Tree height True) : tagged)
          | otherwise = (highest, (Tree height visible) : tagged)

viewDistance :: Int -> [Tree] -> Int
viewDistance height trees = length $ takeWhile1 (< height) $ fmap treeHeight trees