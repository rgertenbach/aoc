import Distribution.Simple
import System.Process (runCommand)

main :: IO ()
main = defaultMainWithHooks simpleUserHooks
  { preConf = \args flags -> do
      _ <- runCommand "gen-hie > hie.yaml"
      preConf simpleUserHooks args flags
  }
