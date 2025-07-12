#!/bin/bash
if [ -z "$1" ]; then
  echo "Uso: $0 caminho_arquivo.py"
  exit 1
fi
grep -E "^(class|def) " "$1"
