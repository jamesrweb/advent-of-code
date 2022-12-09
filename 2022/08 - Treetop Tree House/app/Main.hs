module Main (main) where

import Forest (Forest, countVisible, setForestVisibility, scenicScore)
import Tree (readTree)

main :: IO ()
main = do
        contents <- readFile "app/input.txt"

        let forest = fmap (fmap readTree) $ lines $ contents

        print $ (++) "Part one: " $ show $ solvePartOne forest
        print $ (++) "Part two: " $ show $ solvePartTwo forest


solvePartOne :: Forest -> Int
solvePartOne = countVisible . setForestVisibility

solvePartTwo :: Forest -> Int
solvePartTwo forest = maximum scores
   where row_count = length forest
         column_count = length $ head forest
         scores = [scenicScore forest rows columns | rows <- [0 .. (row_count - 1)], columns <- [0 .. (column_count - 1)]]

