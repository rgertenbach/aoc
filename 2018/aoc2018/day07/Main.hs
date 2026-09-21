module Main (main) where

import App (Solution, run)
import Data.Char (ord)
import Data.List (sortBy)
import qualified Data.Map as Map
import Data.Ord (comparing)
import qualified Text.ParserCombinators.ReadP as P

type Edge = (Char, Char)

type Deps = Map.Map Char [Char]

type Prerequisite = Char

type TopoNode = (Char, [Prerequisite])

type Task = (Char, Int)

parseEdge :: P.ReadP Edge
parseEdge = do
  _ <- P.skipSpaces
  _ <- P.string "Step "
  src <- P.get
  _ <- P.string " must be finished before step "
  tgt <- P.get
  _ <- P.string " can begin."
  _ <- P.skipSpaces
  return (src, tgt)

parseInput :: ReadS [Edge]
parseInput = P.readP_to_S $ P.many parseEdge

-- Adds the dependency of the target and the target with no dependencies if new.
addEdge :: Deps -> Edge -> Deps
addEdge m (s, t) = Map.insertWith (++) s [] $ Map.insertWith (++) t [s] m

topoSortCmp :: TopoNode -> TopoNode -> Ordering
topoSortCmp = comparing (\(c, deps) -> (length deps, c))

-- Topological sort based on a graph of dependencies.
topoSort :: [TopoNode] -> [Char]
topoSort kvs = case sortBy topoSortCmp kvs of
  [] -> ""
  (topKey, _) : rest -> topKey : (topoSort $ markTaskDone topKey rest)

part1 :: Solution
part1 s = case parseInput s of
  [] -> Left "Nothing parsed"
  xs -> Right $ topoSort $ Map.toList $ foldl' addEdge Map.empty $ fst $ last xs

timeReq :: Char -> Int
timeReq c = 1 + 60 + ord c - ord 'A'

-- Add a task to the in-progress tasks returning a list sorted by end-time.
addTask :: [Task] -> Char -> Int -> [Task]
addTask tasks task endTime = sortBy (comparing snd) ((task, endTime) : tasks)

-- Removes a task from all dependencies
markTaskDone :: Char -> [TopoNode] -> [TopoNode]
markTaskDone c nodes = [(task, filter (/= c) deps) | (task, deps) <- nodes]

-- Returns the next task to finish (and remainders)
nextDone :: [Task] -> Maybe (Task, [Task])
nextDone [] = Nothing
nextDone (t : ts) = Just (t, ts)

-- Returns the next doable task (if available) that is unblocked.
nextDoable :: [TopoNode] -> Maybe (Char, [TopoNode])
nextDoable [] = Nothing
nextDoable tasks = case sortBy topoSortCmp tasks of
  (t, []) : ts -> Just (t, ts)
  _ -> Nothing

parallelTopo :: Int -> [Char] -> [Task] -> [TopoNode] -> Maybe Int
parallelTopo _ _ [] [] = Nothing
parallelTopo _ _ inProgress [] = Just $ maximum $ map snd inProgress
parallelTopo t done inProgress toDo = case (length inProgress, nextDoable toDo) of
  (0, Nothing) -> Nothing
  (_, Nothing) -> parallelTopo doneTime doneIfWaiting inProgressIfWaiting toDoIfWaiting
  (5, Just _) -> parallelTopo doneTime doneIfWaiting inProgressIfWaiting toDoIfWaiting
  (_, Just (doableC, remainingToDo)) -> parallelTopo t done (addTask inProgress doableC (t + timeReq doableC)) remainingToDo
  where
    (doneTime, doneIfWaiting, inProgressIfWaiting, toDoIfWaiting) = case nextDone inProgress of
      Nothing -> (0, done, inProgress, toDo)
      Just ((c, dt), r) -> (dt, c : done, r, markTaskDone c toDo)

part2 :: Solution
part2 s = case parseInput s of
  [] -> Left "Nothing parsed"
  xs -> Right $ show $ parallelTopo 0 "" [] deps
    where
      deps = Map.toList $ foldl' addEdge Map.empty $ fst $ last xs

main :: IO ()
main = run part1 part2
