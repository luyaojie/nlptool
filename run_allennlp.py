#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Created by Roger on 2019-08-20
import argparse
import math
import os
import random as py_random
import subprocess
from collections import OrderedDict


def load_config_from_file(filename):
    cmd_option = OrderedDict()
    with open(filename) as fin:
        base_cmd = fin.readline().strip()
        log_folder = fin.readline().strip()
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        for line in fin:
            att = line.strip().split('\t')
            cmd_option[att[0].strip()] = [value.strip() for value in att[1:]]
    return base_cmd, cmd_option, log_folder


def get_exp_id():
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    from datetime import datetime
    exp_str = datetime.now().strftime("%y%m%d")
    for i in range(4):
        exp_str += py_random.choice(alpha)
    return exp_str


def cmd_generator(base_cmd, cmd_option, log_folder, pool_size=2, random=True, max_num=10, enum_time=1):
    """

    :param base_cmd:    Base Command
    :param cmd_option:  {cmd -> [opt1, opt2, ..., optn]}
    :param log_folder:  Log Folder Name
    :param pool_size:
    :param random:      random search ot not
    :param max_num:     max exp number
    :param enum_time:   max enum times
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
        cmd_candidate_list *= enum_time

    cmd_candidate_list = [("%s %s " % (base_cmd, ' '.join(cmd_candidate)),  # Command
                           get_log_filename(log_folder, cmd_candidate),  # STDOUT
                           )
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


def get_run_device():
    if len(args.device) == 1:
        return args.device[0]

    return args.device[0]


def run_train_exp(config_path, model_folder, include_package, device):
    device_env = 'CUDA_VISIBLE_DEVICES={device}'.format(device=device)
    run_cmd = "{device} allennlp train -s {model} {config} --include-package {include}".format(device=device_env,
                                                                                               model=model_folder,
                                                                                               config=config_path,
                                                                                               include=include_package)
    run_cmd += " >/dev/null 2>&1"
    run_command(run_cmd)


def run_eval_exp(model_folder, test_data_path, include_package, device):
    run_cmd = "allennlp evaluate {model} {test} --include-package {include} --cuda-device {device}".format(
        device=device,
        model=model_folder,
        test=test_data_path,
        include=include_package)
    run_command(run_cmd)


def add_argument(_parser):
    _parser.add_argument('-c', '--config', dest='config', help='Run Config')
    _parser.add_argument('-m', '--model', dest='model', help='Model Prefix')
    _parser.add_argument('-k', '--run-time-number', dest='run_time_number', help='Run Time')
    _parser.add_argument('-d', '--device', dest='device', help='GPU Device to Run')
    _parser.add_argument('-i', '--include', dest='include_package', help='Include Package')
    _parser.add_argument('-t', '--test', dest='test_data_path', help='Test Data Path')


def main():
    for i in range(args.run_time_number):
        run_train_exp(config_path=args.config,
                      model_folder=args.model,
                      include_package=args.include_package,
                      device=args.device)
        if args.test_data_path is not None:
            run_eval_exp(model_folder=args.model,
                         test_data_path=args.test_data_path,
                         include_package=args.include_package,
                         device=args.device)


if __name__ == "__main__":
    print("This Process: %s" % os.getpid())

    parser = argparse.ArgumentParser()
    add_argument(parser)
    args = parser.parse_args()
    main()
