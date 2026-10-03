{-# LANGUAGE NamedFieldPuns #-}

module Main (main) where

import App (Solution, run)
import Data.Char (isDigit)
import qualified Data.Map as Map
import Data.Sequence (Seq (Empty, (:<|), (:|>)), ViewR ((:>)))
import qualified Data.Sequence as Seq

type PlayerScores = Map.Map Int Int

type Marbles = Seq.Seq Int

data GameState = GameState
  { players :: Int,
    active :: Int,
    scores :: PlayerScores,
    marbles :: Marbles
  }

initialGameState :: Int -> GameState
initialGameState numPlayers =
  GameState
    { players = numPlayers,
      active = 1,
      scores = Map.fromList [(p, 0) | p <- [1 .. numPlayers]],
      marbles = Seq.fromList [0]
    }

-- Number of marbles in the game before acting on this one.
marblesInGame :: Int -> Int
marblesInGame marble = marble - 2 * ((marble - 1) `div` 23)

incPlayer :: Int -> Int -> Int
incPlayer numPlayers player = (player + 1) `mod` numPlayers

addMarble :: GameState -> Int -> GameState
addMarble GameState {players, active, scores, marbles = Empty} _ =
  GameState {players, active, scores, marbles = Seq.fromList [0]}
addMarble GameState {players, active, scores, marbles = (x :<| Empty)} new =
  GameState
    { players,
      active = incPlayer players active,
      scores,
      marbles = Seq.fromList ([new, x])
    }
addMarble GameState {players, active, scores, marbles = m@(x :<| y :<| ys)} new
  | new `mod` 23 == 0 =
      GameState
        { players,
          active = incPlayer players active,
          scores = Map.update updateScore active scores,
          marbles = Seq.drop 1 $ right <> left
        }
  | otherwise =
      GameState
        { players,
          active = incPlayer players active,
          scores,
          marbles = (new :<| ys) :|> x :|> y
        }
  where
    (left, right) = Seq.splitAt (marblesInGame new - 7) m
    otherRemoved = sum $ Seq.take 1 right
    updateScore s = Just $ s + new + otherRemoved

parseLine :: String -> (Int, Int)
parseLine s = (numPlayers, pointsLast)
  where
    numPlayers = read $ takeWhile isDigit s
    pointsLast = read $ takeWhile isDigit $ dropWhile (not . isDigit) $ dropWhile isDigit s

play :: (Int, Int) -> Int
play (numPlayers, pointsLast) = maximum $ map snd $ Map.toList $ scores finalState
  where
    marbles = [1 .. pointsLast]
    finalState = foldl addMarble (initialGameState numPlayers) marbles

part1 :: Solution
part1 s = Right $ show $ map play $ map parseLine $ lines s

part2 :: Solution
part2 s = Right $ show $ map play $ map (\(np, mp) -> (np, mp * 100)) $ map parseLine $ lines s

main :: IO ()
main = run part1 part2
