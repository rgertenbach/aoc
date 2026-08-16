module App (run, Solution) where

import System.Environment (getArgs)
import System.Exit (die)
import System.IO (readFile')

type Operation = Either String String

type Solution = String -> Operation

helpMsg :: [String] -> String
helpMsg args = "Failure:\nNeed part (1 or 2) and filepath, got: " ++ show args

runWith :: (String -> Operation) -> String -> IO ()
runWith f fp = do
  file <- readFile' fp
  case f file of
    Left s -> die $ "Failure:\n" ++ s
    Right s -> putStrLn $ "Success:\n" ++ s

run :: Solution -> Solution -> IO ()
run part1 part2 = do
  args <- getArgs
  case args of
    ["1", fp] -> part1 `runWith` fp
    ["2", fp] -> part2 `runWith` fp
    _ -> die $ helpMsg args
