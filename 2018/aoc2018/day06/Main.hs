module Main (main) where

import App (Solution, run)
import qualified Text.ParserCombinators.ReadP as P

type Point = (Int, Int)

parsePoint :: P.ReadP Point
parsePoint = do
  _ <- P.skipSpaces
  x <- P.readS_to_P reads
  _ <- P.char ','
  _ <- P.skipSpaces
  y <- P.readS_to_P reads
  return (x, y)

parsePoints :: ReadS [Point]
parsePoints = P.readP_to_S $ P.many parsePoint

manhattan :: Point -> Point -> Int
manhattan (x1, y1) (x2, y2) = abs (x1 - x2) + abs (y1 - y2)

closest :: Point -> [Point] -> [Point]
closest p ps = filter ((== minDist) . distToP) ps
  where
    distToP = manhattan p
    minDist = minimum $ map distToP ps

totalManhattan :: [Point] -> Point -> Int
totalManhattan ps p = sum $ map (manhattan p) ps

extendsInfinitely :: Int -> [Point] -> Point -> Bool
extendsInfinitely _ [] _ = error "List must not be empty"
extendsInfinitely maxl1 ps p@(x, y) = any isClosest extent
  where
    extent = [(x - maxl1, y), (x + maxl1, y), (x, y - maxl1), (x, y + maxl1)]
    isClosest t = closest t ps == [p]

findArea :: [Point] -> Point -> Int
findArea ps p@(x, y) = extent3Dir [y, y - 1 ..] + extent3Dir [y + 1 ..]
  where
    isClosest p' = closest p' ps == [p]
    extent1Dir = length . takeWhile isClosest
    extent2Dir y' = extent1Dir [(x - o, y') | o <- [0 ..]] + extent1Dir [(x + o, y') | o <- [1 ..]]
    extent3Dir = sum . takeWhile (> 0) . map extent2Dir

part1 :: Solution
part1 s = case parsePoints s of
  [] -> Left "No Parse"
  results -> Right $ show $ maximum $ map (findArea points) finite
    where
      points = fst $ last results
      maxl1 = maximum [manhattan p1 p2 | p1 <- points, p2 <- points] + 1
      finite = [p | p <- points, not $ extendsInfinitely maxl1 points p]

part2 :: Solution
part2 s = case parsePoints s of
  [] -> Left "No Parse"
  results -> Right $ show $ length $ filter tm [(x, y) | x <- xs, y <- ys]
    where 
      points = fst $ last results
      xs = [minimum $ map fst points .. maximum $ map fst points]
      ys = [minimum $ map snd points .. maximum $ map snd points]
      tm = (< 10000) . totalManhattan points


main :: IO ()
main = run part1 part2
