#!/bin/sh
# Packs the build into dist/beyond-the-titanic-<target>.tar.gz (.zip for
# Windows) for av: the program at the top with its data files beside it
# (it finds them there), README.md, PATCHES.md, the game's INSTRUCT.TXT and
# the licences.
#
#   asciiverse/package.sh x86_64-unknown-linux-musl
set -eu
cd "$(dirname "$0")/.."
target="$1"
case "$target" in *windows*) exe=.exe ;; *) exe= ;; esac
stage=stage/beyond-the-titanic
rm -rf "$stage" && mkdir -p "$stage" dist
cp "out/beyond-the-titanic$exe" "$stage/"
cp src/ROOMS1 src/ROOMS2 src/SPECIAL1 src/SPECIAL2 src/LINE "$stage/"
cp README.md PATCHES.md INSTRUCT.TXT gpl-3.0.txt agpl-3.0.txt "$stage/"
if [ -n "$exe" ]; then
  (cd "$stage" && zip -qr "../../dist/beyond-the-titanic-$target.zip" .)
else
  tar -czf "dist/beyond-the-titanic-$target.tar.gz" -C "$stage" .
fi
ls dist
