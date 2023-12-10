createPairs :: [Integer] -> [(Integer, Integer)]
createPairs [] = []
createPairs [_] = []
createPairs (x:y:xs) = (x, y) : createPairs (y:xs)

difference :: (Integer, Integer) -> Integer
difference (a, b) =
        b - a

linePairings :: [Integer] -> Integer
linePairings line | all (== 0) line = 0
linePairings line = last line + (linePairings $ map difference $ createPairs line)

linePairingsInverted :: [Integer] -> Integer
linePairingsInverted line | all (== 0) line = 0
linePairingsInverted line = head line - (linePairingsInverted $ map difference $ createPairs line)

parseLine :: String -> [Integer]
parseLine line =
    map read $ words line

solvePartOne :: [[Integer]] -> Integer
solvePartOne rows =
        sum $ map linePairings rows

solvePartTwo :: [[Integer]] -> Integer
solvePartTwo rows =
        sum $ map linePairingsInverted rows

main :: IO ()
main =
    do
        contents <- readFile "input.txt"
        let rows = map parseLine $ lines contents
        let partOne = solvePartOne rows
        let partTwo = solvePartTwo rows

        putStrLn $ "Part one: " ++ show partOne
        putStrLn $ "Part two: " ++ show partTwo