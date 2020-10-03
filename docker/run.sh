#!/bin/sh
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

. ${dir}/shvars

src=$(cd ${dir}/.. && pwd)

set -ex 

#docker run -d --name=$IMAGE -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home $USERNAME/$IMAGE:latest
docker run --name=$HUMANNAME --rm -it --mount type=bind,source=$src,destination=/mnt/git $USERNAME/$IMAGE:$VERSION /bin/bash
