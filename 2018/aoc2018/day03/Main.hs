module Main (main) where

import App (Solution, run)
import Data.List (sort)
import qualified Data.List.NonEmpty as NonEmpty
import qualified Data.Map as Map
import qualified Text.ParserCombinators.ReadP as P
import Text.Read (Read (readPrec), lift)

type V2 = (Int, Int)

data Claim = Claim {getId :: Int, getPoints :: [V2]} deriving (Show)

rasterize :: (V2, V2) -> [V2]
rasterize ((x, y), (w, h)) =
  [ (x', y')
  | x' <- [x .. x + w - 1],
    y' <- [y .. y + h - 1]
  ]

instance Read Claim where
  readPrec = lift $ do
    _ <- P.char '#'
    c <- P.readS_to_P reads
    _ <- P.string " @ "
    x <- P.readS_to_P reads
    _ <- P.char ','
    y <- P.readS_to_P reads
    _ <- P.string ": "
    w <- P.readS_to_P reads
    _ <- P.char 'x'
    h <- P.readS_to_P reads
    return $ Claim c $ rasterize ((x, y), (w, h))

countPoints :: [V2] -> Map.Map V2 Int
countPoints ps = Map.fromList $ map makeF grouped
  where
    grouped = NonEmpty.group $ sort ps
    makeF vs = (NonEmpty.head vs, length vs)

lookupCount :: Map.Map V2 Int -> V2 -> Int
lookupCount freqs p = Map.findWithDefault 0 p freqs

part1 :: Solution
part1 = Right . show . Map.size . Map.filter (> 1) . countPoints . concatMap (getPoints . read) . lines

part2 :: Solution
part2 s = case filter isAlone claims of
  [] -> Left "No single found"
  [x] -> Right $ show $ getId x
  _ -> Left "Found more than one single"
  where
    claims = map read $ lines s
    freqs = countPoints $ concatMap getPoints $ claims
    isAlone = all ((1 ==) . lookupCount freqs) . getPoints

main :: IO ()
main = run part1 part2
