#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Created by Roger on 2019-08-20
import argparse
import os
import random as py_random
import subprocess


def get_exp_id():
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    from datetime import datetime
    exp_str = datetime.now().strftime("%y_%m_%d")
    exp_str += '_'
    for i in range(4):
        exp_str += py_random.choice(alpha)
    return exp_str


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
    _parser.add_argument('-k', '--run-time-number', dest='run_time_number', help='Run Time', type=int, default=1)
    _parser.add_argument('-d', '--device', dest='device', help='GPU Device to Run')
    _parser.add_argument('-i', '--include', dest='include_package', help='Include Package')
    _parser.add_argument('-t', '--test', dest='test_data_path', help='Test Data Path')


def main():
    for i in range(args.run_time_number):
        model_path = '_'.join([args.model, get_exp_id()])
        run_train_exp(config_path=args.config,
                      model_folder=model_path,
                      include_package=args.include_package,
                      device=args.device)
        if args.test_data_path is not None:
            run_eval_exp(model_folder=model_path,
                         test_data_path=args.test_data_path,
                         include_package=args.include_package,
                         device=args.device)


if __name__ == "__main__":
    print("This Process: %s" % os.getpid())

    parser = argparse.ArgumentParser()
    add_argument(parser)
    args = parser.parse_args()
    main()
