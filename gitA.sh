#!/bin/bash

# Ellenőrzés: megadtál commit message-et?
if [ -z "$1" ]; then
  echo "❌ Hibás használat: kérlek adj meg egy commit üzenetet."
  echo "Használat: ./git-auto.sh \"Commit üzenet\""
  exit 1
fi

# Git parancsok
git add .
git commit -m "$1"
git push

echo "✅ Commit és push sikeresen végrehajtva: '$1'"