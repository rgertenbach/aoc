module Main (main) where

import App (Solution, run)
import Data.List (group, sort)

freqs :: String -> [Int]
freqs = map length . group . sort

part1 :: Solution
part1 s = Right $ show $ length twos * length threes
  where
    hists = map freqs $ lines s
    twos = filter (elem 2) hists
    threes = filter (elem 3) hists

dist :: String -> String -> Int
dist a b = length $ filter id $ zipWith (/=) a b

part2 :: Solution
part2 s = case match of
  [] -> Left "No pairs with distance 1 found"
  [(x, y)] -> Right $ show $ [a | (a, b) <- zip x y, a == b]
  _ -> Left "Found more than one pair with distance 1"
  where
    l = lines s
    match = [(x, y) | x <- l, y <- l, x > y, dist x y == 1]

main :: IO ()
main = run part1 part2
