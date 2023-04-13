#!/bin/bash
#usage
#./generate.sh [number of characters] > [file name]
#ie creates all 6 character combinations
#   and creates and puts them inside a file named passwords
#./generate.sh 6 > passwords
charset=({a..z})
permute(){
  (($1 == 0)) && { echo "$2"; return; }
  for char in "${charset[@]}"
  do
    permute "$((${1} - 1 ))" "$2$char"
  done
}
permute "$1"
