module Main (main) where

import App (Solution, run)
import Data.Vector as Vec ((!))
import qualified Data.Vector as Vec

power :: Int -> Int -> Int -> Int
power y x serial = expanded `div` 100 `mod` 10 - 5
  where
    rackId = x + 10
    expanded = (rackId * y + serial) * rackId

data Grid = Grid Int (Vec.Vector Int)

grid :: Int -> Int -> Grid
grid n serial =
  Grid n (Vec.fromList [power y x serial | y <- [1 .. n], x <- [1 .. n]])

gridIdx :: Int -> Int -> Grid -> Int
gridIdx y x (Grid n g) = g ! (y * n + x)

convSum :: Int -> Grid -> Grid
convSum k g@(Grid n _) = Grid (n - k + 1) (Vec.fromList [conv y x | y <- rng, x <- rng])
  where
    rng = [0 .. n - k]
    conv r c = sum $ [gridIdx (r + y - 1) (c + x - 1) g | y <- [1 .. k], x <- [1 .. k]]

gridMaxPos :: Grid -> (Int, Int, Int)
gridMaxPos g@(Grid n _) = maximum tuples
  where
    tuples = [(gridIdx y x g, x + 1, y + 1) | y <- [0 .. n - 1], x <- [0 .. n - 1]]

part1 :: Solution
part1 s = Right $ show $ gridMaxPos $ convSum 3 $ grid 300 $ read s

-- 233,187,13
-- 6:46
-- Cumsum!
part2 :: Solution
part2 s = Right $ show $ maximum convSums
  where
    g = grid 300 $ read s
    convSums = [(gridMaxPos $ convSum k g, k) | k <- [1 .. 300]]

main :: IO ()
main = run part1 part2
