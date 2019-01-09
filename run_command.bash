#!/usr/bin/env bash
# -*- coding:utf-8 -*-
# Created by Roger on 2018/6/13

# Init Value
RUNTIME=10
BASHCMD=""

while getopts 'd:k:s:c:' OPT; do
    case ${OPT} in
        k)
            RUNTIME="$OPTARG";;
        c)
            BASHCMD="$OPTARG";;
    esac
done

echo "Run Time     is" ${RUNTIME};
echo "Bash Command is" ${BASHCMD};

for ((i = 0; i != $RUNTIME; i++))
do
    ${BASHCMD}
done
