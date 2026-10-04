{-# LANGUAGE NamedFieldPuns #-}

module Main (main) where

import App (Solution, run)
import qualified Data.Set as Set
import qualified Text.ParserCombinators.ReadP as ReadP

data Vec2 = Vec2 {x :: Int, y :: Int} deriving (Eq, Ord)

addVec2 :: Vec2 -> Vec2 -> Vec2
addVec2 (Vec2 x1 y1) (Vec2 x2 y2) = Vec2 {x = x1 + x2, y = y1 + y2}

data Particle = Particle {pos :: Vec2, vel :: Vec2}

moveParticle :: Particle -> Particle
moveParticle (Particle pos vec) = Particle (addVec2 pos vec) vec

bbox :: [Particle] -> (Int, Int, Int, Int)
bbox ps = (minX, minY, maxX, maxY)
  where
    positions = map pos ps
    minX = minimum $ map x positions
    minY = minimum $ map y positions
    maxX = maximum $ map x positions
    maxY = maximum $ map y positions

area :: [Particle] -> Int
area ps = (maxX - minX + 1) * (maxY - minY + 1)
  where
    (minX, minY, maxX, maxY) = bbox ps

parseParticle :: ReadP.ReadP Particle
parseParticle = do
  _ <- ReadP.skipSpaces
  _ <- ReadP.string "position=<"
  _ <- ReadP.skipSpaces
  px <- ReadP.readS_to_P reads
  _ <- ReadP.char ','
  _ <- ReadP.skipSpaces
  py <- ReadP.readS_to_P reads
  _ <- ReadP.skipSpaces
  _ <- ReadP.char '>'
  _ <- ReadP.skipSpaces
  _ <- ReadP.string "velocity=<"
  vx <- ReadP.readS_to_P reads
  _ <- ReadP.char ','
  _ <- ReadP.skipSpaces
  vy <- ReadP.readS_to_P reads
  _ <- ReadP.skipSpaces
  _ <- ReadP.char '>'
  return $ Particle {pos = Vec2 {x = px, y = py}, vel = Vec2 {x = vx, y = vy}}

parseInput :: String -> Maybe [Particle]
parseInput s = case (ReadP.readP_to_S $ ReadP.many parseParticle) s of
  [] -> Nothing
  parsed -> Just $ fst $ last parsed

plot :: [Particle] -> String
plot ps = unlines [makeRow r | r <- [minY .. maxY]]
  where
    positions = map pos ps
    occupied = Set.fromList $ positions
    (minX, minY, maxX, maxY) = bbox ps
    makeRow r =
      [ if Set.member (Vec2 {x = c, y = r}) occupied then '█' else ' '
      | c <- [minX .. maxX]
      ]

maxConc :: Int -> [Particle] -> (Int, String)
maxConc i ps = if area ps < area nextPs then (i, plot ps) else maxConc (i + 1) nextPs
  where
    nextPs = map moveParticle ps

part1 :: Solution
part1 s = case parseInput s of
  Nothing -> Left $ "Could not parse\n" ++ s
  Just particles -> Right $ snd $ maxConc 0 particles

part2 :: Solution
part2 s = case parseInput s of
  Nothing -> Left $ "Could not parse\n" ++ s
  Just particles -> Right $ show $ fst $ maxConc 0 particles

main :: IO ()
main = run part1 part2
