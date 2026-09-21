{-# LANGUAGE OverloadedRecordDot #-}

module Main (main) where

import App (Solution, run)

data Node = Node
  { numChildren :: Int,
    numMetadata :: Int,
    children :: [Node],
    metadata :: [Int]
  }
  deriving (Show)

parseNode :: Int -> [Int] -> ([Node], [Int])
parseNode 0 r = ([], r)
parseNode _ [] = ([], [])
parseNode _ [r] = ([], [r])
parseNode n (c : m : xs) =
  ( Node
      { numChildren = c,
        numMetadata = m,
        children = ch,
        metadata = take m remainder
      }
      : rest,
    t
  )
  where
    (ch, remainder) = parseNode c xs
    (rest, t) = parseNode (n - 1) (drop m remainder)

parseTree :: String -> ([Node], [Int])
parseTree s = parseNode 1 $ map read $ words s

sumMetaData :: Node -> Int
sumMetaData node = (sum node.metadata) + (sum $ map sumMetaData node.children)

part1 :: Solution
part1 s = case parseTree s of
  ([t], []) -> Right $ show $ sumMetaData t
  x -> Left $ "Unsuccessful parse: " ++ show x

valueRoot :: Node -> Int
valueRoot node@Node {numChildren = 0} = sumMetaData node
valueRoot Node {children = c, metadata = m} = sum $ map foo m
  where
    len = length c
    foo i = if i <= 0 || i > len then 0 else valueRoot $ c !! (i - 1)

part2 :: Solution
part2 s = case parseTree s of
  ([t], []) -> Right $ show $ valueRoot t
  x -> Left $ "Unsuccessful parse: " ++ show x

main :: IO ()
main = run part1 part2
