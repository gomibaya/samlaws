#!/bin/sh
# 0.2.0: Modificado para que lea config de CONFIG

prg=$0
if [ ! -e "$prg" ]; then
  case $prg in
    (*/*) exit 1;;
    (*) prg=$(command -v -- "$prg") || exit;;
  esac
fi
dir=$(
  cd -P -- "$(dirname -- "$prg")" && pwd -P
) || exit

if [ ! -f $dir/Dockerfile ]; then
 echo "Error. Dockerfile no accesible"
fi

oldpwd=$(pwd)
cd $dir
cd ..

. ${dir}/shvars

set -ex 

docker build -f ${dir}/Dockerfile -t ${LOCALUSERNAME}/$IMAGE:$VERSION .

cd $oldpwd
