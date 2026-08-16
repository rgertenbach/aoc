module Main (main) where

import App (Solution, run)
import Data.List (stripPrefix, scanl')
import qualified Data.Set as Set

removePrefix :: String -> String -> String
removePrefix p s = case stripPrefix p s of
  Just x -> x
  Nothing -> s

changes :: String -> [Int]
changes = map parseChange . lines
  where
    parseChange = read . removePrefix "+"

part1 :: Solution
part1 = Right . show . sum . changes

cumsum :: [Int] -> [Int]
cumsum = scanl' (+) 0

findRepeat :: Set.Set Int -> [Int] -> Int
findRepeat _ [] = error "Empty Array"
findRepeat set (x : xs) 
  | Set.member x set = x
  | otherwise = findRepeat (Set.insert x set) xs

part2 :: Solution
part2 = Right . show . findRepeat Set.empty . cumsum . cycle . changes

main :: IO ()
main = run part1 part2
