#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Created by Roger on 2018/3/29
import subprocess


def run_one_time(shell_file):
    subprocess.call(["sh", "%s" % shell_file])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser('Multi Process Run Shell')
    parser.add_argument('-s', dest='shell', help='Shell File Name')
    parser.add_argument('-n', dest='number', help='Process Number')
    args = parser.parse_args()

    for i in range(argps.number):
        print("[%4d-th Run] %s" % (args.number, args.shell))
        run_one_time(shell_file)
