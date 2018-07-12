#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Created by Roger on 2018/6/20
import math
import multiprocessing as mp
import os
import random as py_random
import subprocess
from collections import OrderedDict


def load_config_from_file(filename):
    cmd_option = OrderedDict()
    with open(filename) as fin:
        base_cmd = fin.readline().strip()
        log_folder = fin.readline().strip()
        for line in fin:
            att = line.strip().split('\t')
            cmd_option[att[0]] = att[1:]
    return base_cmd, cmd_option, log_folder


def get_exp_id():
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    from datetime import datetime
    exp_str = datetime.now().strftime("%y%m%d")
    for i in range(4):
        exp_str += py_random.choice(alpha)
    return exp_str


def get_log_filename(log_folder, cmd_candidate):
    """
    :param log_folder:
    :param cmd_candidate:   len % 2 == 0
        [cmd, opt, cmd, opt]
    :return:
    """
    assert len(cmd_candidate) % 2 == 0
    log_filename_list = []
    for index in range(len(cmd_candidate) // 2):
        log_filename_list += ["%s_%s" % (cmd_candidate[2 * index].replace('-', ''), cmd_candidate[2 * index + 1])]
    log_filename = log_folder + os.sep + '_'.join([get_exp_id()] + log_filename_list)
    return log_filename


def cmd_generator(base_cmd, cmd_option, log_folder, pool_size=2, random=True, max_num=10):
    """

    :param base_cmd:    Base Command
    :param cmd_option:  {cmd -> [opt1, opt2, ..., optn]}
    :param log_folder:  Log Folder Name
    :param pool_size:
    :param random:      random search ot not
    :param max_num:     max exp number
    :return:
    """
    cmd_candidate_list = list()
    if random:
        for i in range(max_num):
            cmd_candidate = list()
            for cmd in cmd_option:
                cmd_candidate += [cmd, py_random.choice(cmd_option[cmd])]
            cmd_candidate_list += [cmd_candidate]
    else:
        cmd_list = []
        for cmd in cmd_option:
            cmd_list += [[]]
            for option in cmd_option[cmd]:
                cmd_list[-1] += [[cmd, option]]
        for cmds in cmd_list:
            if len(cmd_candidate_list) == 0:
                cmd_candidate_list = cmds
            else:
                cmd_candidate_list = [c1 + c2 for c1 in cmds for c2 in cmd_candidate_list]

    cmd_candidate_list = ["%s %s > %s 2>&1" % (base_cmd, ' '.join(cmd_candidate),
                                               get_log_filename(log_folder, cmd_candidate))
                          for cmd_candidate in cmd_candidate_list]

    num_batch = int(math.ceil(len(cmd_candidate_list) / float(pool_size)))
    for i in range(num_batch):
        start, end = i * pool_size, (i + 1) * pool_size
        yield cmd_candidate_list[start: end]


def run_command(command):
    print(os.getpid(), command)
    # status = os.system(command)
    status = subprocess.call([command], shell=True)
    if status > 0:
        print("Run Err:", command)
        return command, 1
    else:
        print("Finished:", command)
        return command, 0


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '-config', dest='config', type=str, help='Run Config')
    parser.add_argument('-n', '-thread', dest='thread', type=int, default=1, help='Thread Num')
    parser.add_argument('-enum', action='store_false', dest='random', help='Enumerate all params')
    parser.add_argument('-random', action='store_true', dest='random', help='Random Search (Default)')
    parser.set_defaults(random=True)
    parser.add_argument('-k', '-max-num', dest='max_num', type=int, default=10, help='Max Random Search Time')
    args = parser.parse_args()

    base_cmd, cmd_option, log_folder = load_config_from_file(args.config)

    for cmd_list in cmd_generator(base_cmd, cmd_option, log_folder,
                                  pool_size=args.thread, random=args.random, max_num=args.max_num):
        pool = mp.Pool(args.thread)
        pool.map(run_command, cmd_list)
        pool.close()
        pool.join()


if __name__ == "__main__":
    main()