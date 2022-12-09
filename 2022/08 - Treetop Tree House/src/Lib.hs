module Lib (takeWhile1) where

takeWhile1 :: (a -> Bool) -> [a] -> [a]
takeWhile1 _ [] = []
takeWhile1 f (x:xs)
  | f x == True = x : (takeWhile1 f xs)
  | otherwise = [x]