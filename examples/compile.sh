#! /bin/bash

# Create build dir
mkdir -p build

g++ -O0 src/insertionsort.cpp -o build/insertionsort
g++ -O0 src/quicksort.cpp -o build/quicksort
g++ -O0 src/bubblesort.cpp -o build/bubblesort
g++ -O0 src/stdsort.cpp -o build/stdsort
