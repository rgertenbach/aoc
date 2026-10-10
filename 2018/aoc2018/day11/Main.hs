module Main (main) where

import App (Solution, run)
import Data.Vector.Unboxed as Vec ((!))
import qualified Data.Vector.Unboxed as Vec

gridSize :: Int
gridSize = 300

power :: Int -> Int -> Int -> Int
power y x serial =
  let rackId = x + 10
      expanded = (rackId * y + serial) * rackId
   in expanded `div` 100 `mod` 10 - 5

data Grid = Grid Int (Vec.Vector Int)

gridGen :: Int -> Int -> Grid
gridGen n serial =
  Grid n (Vec.fromList [power y x serial | y <- [1 .. n], x <- [1 .. n]])

gridIdx :: Int -> Int -> Grid -> Int
gridIdx y x (Grid n g) = g ! (y * n + x)

gridCumSum :: Grid -> Grid
gridCumSum (Grid n v) = Grid newN $ Vec.fromList $ concat cumGrid
  where
    newN = n + 1
    rowCumSum y = Vec.toList $ Vec.scanl (+) 0 $ Vec.slice (y * n) n v
    cumRows = [rowCumSum y | y <- [0 .. n - 1]]
    zeroRow = replicate newN 0
    addRows = zipWith (+)
    cumGrid = scanl addRows zeroRow $ cumRows

gridIdxConv :: Int -> Int -> Int -> Grid -> Int
gridIdxConv k y x g = bottomRight - topRight - bottomLeft + topLeft
  where
    topLeft = gridIdx y x g
    topRight = gridIdx y (x + k) g
    bottomLeft = gridIdx (y + k) x g
    bottomRight = gridIdx (y + k) (x + k) g

gridMaxConvPos :: Int -> Grid -> (Int, Int, Int, Int)
gridMaxConvPos k g@(Grid n _) = maximum [(gridIdxConv k y x g, y, x, k) | y <- [0 .. n - k - 1], x <- [0 .. n - k - 1]]

part1 :: Solution
part1 s = Right $ show $ (x + 1, y + 1)
  where
    g = gridGen gridSize $ read s
    cg = gridCumSum g
    (_, y, x, _) = gridMaxConvPos 3 cg

part2 :: Solution
part2 s = Right $ show $ (x + 1, y + 1, k)
  where
    cg = gridCumSum $ gridGen gridSize $ read s
    (_, y, x, k) = maximum $ map (flip gridMaxConvPos cg) [1 .. gridSize]

main :: IO ()
main = run part1 part2
