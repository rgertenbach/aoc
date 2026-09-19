#!/bin/sh
#
# @param $1: The day id

mkdir "day$1"
cp Template.hs "day$1/Main.hs"

cat >> package.yaml << EOF 
  day$1:
    main:               Main.hs
    source-dirs:        day$1
    ghc-options:
    - -threaded
    - -rtsopts
    - -with-rtsopts=-N
    dependencies:
    - aoc2018

EOF

stack build
gen-hie > hie.yaml
