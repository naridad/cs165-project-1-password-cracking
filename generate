#!/bin/bash
charset=({a..z})
permute(){
  (($1 == 0)) && { echo "$2"; return; }
  for char in "${charset[@]}"
  do
    permute "$((${1} - 1 ))" "$2$char"
  done
}
permute "$1"
