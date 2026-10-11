{-# LANGUAGE NumericUnderscores #-}

module Main (main) where

import App (Solution, run)
import Data.Bits ()
import qualified Data.Set as Set

type Pot = Char

type Pots = [Pot]

type State = (Int, Pots)

type Birth = Pots

type Births = Set.Set Birth

parseInput :: String -> (Pots, Births)
parseInput s = (initState, rules)
  where
    initLine : _ : ruleLines = lines s
    initState = dropWhile (`notElem` "#.") initLine
    birthLines = filter (('#' ==) . last) ruleLines
    births = map (takeWhile (`elem` "#.")) birthLines
    rules = Set.fromList births

potsStep :: Births -> Pots -> Pots
potsStep births (a : b : c : d : e : rest) = this : following
  where
    this = if Set.member [a, b, c, d, e] births then '#' else '.'
    following = potsStep births $ b : c : d : e : rest
potsStep _ _ = ""

stateStep :: Births -> State -> State
stateStep births (start, pots) = pad (leftTruncatedStart, truncatedPots)
  where
    nextPots = potsStep births pots
    (paddedStart, paddedNextPots) = pad (start + 2, nextPots)
    leadingEmtpy = length $ takeWhile (== '.') paddedNextPots
    leftTruncatedStart = paddedStart + leadingEmtpy
    leftTruncatedPots = drop leadingEmtpy paddedNextPots
    truncatedPots = reverse $ dropWhile (== '.') $ reverse leftTruncatedPots

pad :: State -> State
pad (start, pots) = (start - 5, ("....." ++ pots ++ "....."))

simulate :: Births -> Pots -> [State]
simulate births initPots = pots
  where
    initState = (0, initPots)
    pots = iterate (stateStep births) $ pad initState

points :: State -> [Int]
points (start, pots) = zipWith (\i x -> if x == '#' then i else 0) [start ..] pots

part1 :: Solution
part1 s = Right $ show $ sum $ points $ states !! nSteps
  where
    nSteps = 20
    (state, births) = parseInput s
    states = simulate births state

part2 :: Solution
part2 s = Right $ show $ sum $ points (finalStart, pots)
  where
    nSteps = 50_000_000_000
    (state, births) = parseInput s
    states = simulate births state
    (genStart, _, (potStart, pots)) = head $ dropWhile (\(_, l, c) -> snd l /= snd c) $ zip3 [1 ..] states (drop 1 states)
    additionalSteps = nSteps - genStart
    finalStart = potStart + additionalSteps

main :: IO ()
main = run part1 part2
