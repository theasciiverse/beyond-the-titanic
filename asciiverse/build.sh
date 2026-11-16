#!/bin/sh
# Builds Beyond the Titanic into out/ with Free Pascal 3.2.2, from
# src/BEYOND.PAS (which includes the other .PAS files) and src/avcrt.pas.
# The compiler and its target flags come from the environment, so one
# script serves every target (see .github/workflows/release.yml):
#
#   asciiverse/build.sh                                  # Linux: static by default
#   FPC=ppca64 FPCFLAGS="-XR$(xcrun --show-sdk-path)" asciiverse/build.sh   # macOS
#   FPCFLAGS=-Twin64 EXE=.exe asciiverse/build.sh        # Windows, from Linux
set -eu
cd "$(dirname "$0")/.."
export TERM="${TERM:-xterm}"
FPC="${FPC:-fpc}"
FPCFLAGS="${FPCFLAGS:-}"
EXE="${EXE:-}"
rm -rf out/units
mkdir -p out/units
# -Sg: the game uses goto; -Xs: strip; -XX -CX: smart linking
# shellcheck disable=SC2086
$FPC -O2 -Sg -Xs -XX -CX $FPCFLAGS -FUout/units -FEout \
  "-obeyond-the-titanic$EXE" src/BEYOND.PAS
rm -rf out/units
echo "built out/beyond-the-titanic$EXE"
