#!/bin/bash
PARAMS=('-m 6 -q 70 -mt -af -progress')
for D in $(find . -type d); do
  # cd $D
  echo $D
  cd $D

  for FILE in *.{jpg,jpeg,png,svg,tif,tiff}; do
    [ -e "$FILE" ] || continue
    # Here "$FILE" exists
    cwebp $PARAMS "$FILE" -o "${FILE%.*}".webp

  done

  cd ~

done

#TODO: Turn into git precommit hook