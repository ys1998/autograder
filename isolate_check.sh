#!/bin/bash

mkdir -p temp_$1

cp *.py temp_$1/
cp my_batch/$1/mira.py temp_$1/
cp -r data/ temp_$1/
cd temp_$1/
python3 test.py
cd ..
rm -rf temp_$1