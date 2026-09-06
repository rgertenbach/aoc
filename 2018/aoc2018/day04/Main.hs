{-# LANGUAGE DuplicateRecordFields #-}

module Main (main) where

import App (Solution, run)
import Data.Foldable (maximumBy)
import Data.List (findIndex, sortBy)
import qualified Data.Map as Map
import Data.Ord (comparing)
import Text.ParserCombinators.ReadP (readP_to_S)
import qualified Text.ParserCombinators.ReadP as P

data Timestamp = Timestamp
  { year :: Int,
    month :: Int,
    day :: Int,
    hour :: Int,
    minute :: Int
  }
  deriving (Show, Eq, Ord)

data Action = BeginShift | FallAsleep | WakeUp deriving (Eq, Show)

data Log = Log
  {getTime :: Timestamp, getAction :: Action, getId :: Maybe Int}
  deriving (Show)

data Guard = Guard {getId :: Int, getSleep :: [Int]}

makeGuard :: Int -> Guard
makeGuard i = Guard {getId = i, getSleep = replicate 60 0}

minutesSinceMidnight :: Timestamp -> Int
minutesSinceMidnight Timestamp {hour = h, minute = m} = if h >= 23 then 0 else m

updateGuard :: Guard -> Log -> Guard
updateGuard Guard {getId = i, getSleep = s} Log {getAction = a, getTime = t} =
  let v = if a == FallAsleep then 1 else 0
      m = minutesSinceMidnight t
   in Guard {getId = i, getSleep = take m s ++ replicate (60 - m) v}

updateGuards :: [Guard] -> Log -> [Guard]
updateGuards gs Log {getId = Just i, getAction = BeginShift} = makeGuard i : gs
updateGuards (g : gs) l = updateGuard g l : gs
updateGuards _ Log {getId = Nothing, getAction = BeginShift} = error "Bad Input"
updateGuards [] _ = error "Bad Input"

parseTimestamp :: P.ReadP Timestamp
parseTimestamp = do
  _ <- P.char '['
  y <- P.readS_to_P reads
  _ <- P.char '-'
  m <- P.readS_to_P reads
  _ <- P.char '-'
  d <- P.readS_to_P reads
  _ <- P.skipSpaces
  hr <- P.readS_to_P reads
  _ <- P.char ':'
  mt <- P.readS_to_P reads
  _ <- P.char ']'

  return $ Timestamp {year = y, month = m, day = d, hour = hr, minute = mt}

parseAction :: P.ReadP (Action, Maybe Int)
parseAction = do
  _ <- P.skipSpaces
  P.choice [readSleep, readWakeUp, readStart]
  where
    readSleep = do
      _ <- P.string "falls asleep"
      return (FallAsleep, Nothing)
    readWakeUp = do
      _ <- P.string "wakes up"
      return (WakeUp, Nothing)
    readStart = do
      _ <- P.string "Guard #"
      guardId <- P.readS_to_P reads
      _ <- P.string " begins shift"
      return (BeginShift, Just guardId)

parseLog :: P.ReadP Log
parseLog = do
  t <- parseTimestamp
  _ <- P.skipSpaces
  (a, i) <- parseAction
  return $ Log {getTime = t, getAction = a, getId = i}

runInputParser :: String -> Log
runInputParser s = case readP_to_S parseLog s of
  [(l, "")] -> l
  [] -> error $ "Couldn't parse " ++ show s
  _ -> error $ "Ambiguous parse for " ++ show s

type SleepMap = Map.Map Int [Int]

addDuty :: SleepMap -> Guard -> SleepMap
addDuty m Guard {getId = i, getSleep = s} = Map.insertWith (zipWith (+)) i s m

parseSleeps :: String -> [(Int, [Int])]
parseSleeps s =
  let logs = sortBy (comparing getTime) $ map runInputParser $ lines s
      duties = foldl' updateGuards [] logs
   in Map.toList $ foldl' addDuty Map.empty duties

part1 :: Solution
part1 s = Right $ show $ sleepiestGuard * sleepiestMinute
  where
    (sleepiestGuard, ss) = maximumBy (comparing $ sum . snd) $ parseSleeps s
    (sleepiestMinute, _) = maximumBy (comparing snd) $ zip [0 ..] ss

part2 :: Solution
part2 s = Right $ show $ sleepiestGuard * sleepiestMinute
  where
    (sleepiestGuard, ss) = maximumBy (comparing $ maximum . snd) $ parseSleeps s
    (sleepiestMinute, _) = maximumBy (comparing snd) $ zip [0 ..] ss

main :: IO ()
main = run part1 part2
