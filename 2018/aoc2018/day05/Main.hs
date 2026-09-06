module Main (main) where

import App (Solution, run)
import Data.Char (isAlpha, toUpper)

react :: String -> Char -> String
react [] c = [c]
react s@(x : xs) y = if x /= y && toUpper x == toUpper y then xs else y : s

reactCycle :: String -> String
reactCycle = foldl' react "" . filter isAlpha

lengthAfterReactions :: String -> Int
lengthAfterReactions = length . reactCycle

part1 :: Solution
part1 = Right . show . lengthAfterReactions

part2 :: Solution
part2 s = Right $ show $ minimum $ map lengthAfterReactions ss
  where
    p = reactCycle s
    ss = map dropChars $ zip ['a' .. 'z'] ['A' .. 'Z']
    dropChars (l, u) = filter (`notElem` [l, u]) $ p

main :: IO ()
main = run part1 part2
