#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import csv
import math
import os
import random


def make_new_dir(dir_name):
    if os.path.exists(dir_name):
        print('Data Folder Path: %s is existed, overwrite (y/n)?' % dir_name)
        answer = input()
        if answer.strip().lower() == 'y':
            import shutil
            shutil.rmtree(dir_name)
        else:
            exit(1)
    os.makedirs(dir_name, exist_ok=True)


def get_format(filename):
    if filename.endswith('.jsonl'):
        return 'jsonl'
    elif filename.endswith('.csv'):
        return 'csv'
    else:
        raise NotImplementedError


def write_lines_to_file(lines, filename, index_list=None):
    index_list = range(lines) if index_list is None else index_list

    print("save {} instance to {}".format(len(index_list), filename))

    if filename.endswith('.jsonl'):
        with open(filename, 'w') as output:
            for index in index_list:
                output.write(lines[index])
    elif filename.endswith('.csv'):
        with open(filename, 'w') as output_file:
            keys = set(lines[0].keys())
            output = csv.DictWriter(output_file, lines[0].keys())
            output.writeheader()
            for index in index_list:
                assert keys == set(lines[index].keys())
                output.writerow(lines[index])
    else:
        raise NotImplementedError


def load_lines_from_filename(filename):
    if filename.endswith('.csv'):
        return list(csv.DictReader(open(filename)))
    elif filename.endswith('.jsonl'):
        return open(filename).readlines()
    else:
        raise NotImplementedError


def split():
    filename = args.data
    output_folder = args.output
    dev_size = args.dev
    test_size = args.test

    file_format = get_format(filename)
    lines = load_lines_from_filename(filename)
    print("read {} lines from {}".format(len(lines), filename))

    if 1 > test_size > 0:
        test_size = math.floor(len(lines) * test_size)

    if 1 > dev_size > 0:
        dev_size = math.floor(len(lines) * dev_size)

    dev_size, test_size = int(dev_size), int(test_size)

    if test_size + dev_size >= len(lines):
        print(
            "the sum dev and test [{}] should be smaller train [{}]".format(
                dev_size + test_size, len(lines)
            )
        )
        exit(1)

    if args.random:
        print("shuffle ...")
        random.shuffle(lines)

    print("save to {}".format(output_folder))

    test_indexes = list(range(test_size))
    dev_indexes = list(range(test_size, test_size + dev_size))
    train_indexes = list(range(test_size + dev_size, len(lines)))

    make_new_dir(output_folder)

    for indexes, data_type in zip([train_indexes, dev_indexes, test_indexes],
                                  ['train', 'dev', 'test']):
        if len(indexes) == 0:
            continue
        filename = "{}/{}.{}".format(output_folder, data_type, file_format)
        write_lines_to_file(lines, filename, index_list=indexes)


def cv():
    filename = args.data
    output_folder = args.output
    cv_num = args.cv_num

    file_format = get_format(filename)
    lines = load_lines_from_filename(filename)
    print("read {} lines from {}".format(len(lines), filename))
    if args.random:
        print("shuffle ...")
        random.shuffle(lines)

    print("save to {}".format(output_folder))
    for cv_index in range(cv_num):
        cv_index = cv_index + 1
        valid_indexs = list()
        train_indexs = list()

        for instance_index in range(len(lines)):
            if instance_index % cv_num == cv_index - 1:
                valid_indexs += [instance_index]
            else:
                train_indexs += [instance_index]

        make_new_dir("{}/cv{}".format(output_folder, cv_index))
        train_file = "{}/cv{}/train.{}".format(output_folder,
                                               cv_index,
                                               file_format)
        valid_file = "{}/cv{}/dev.{}".format(output_folder,
                                             cv_index,
                                             file_format)

        write_lines_to_file(lines, train_file, index_list=train_indexs)
        write_lines_to_file(lines, valid_file, index_list=valid_indexs)


def add_global_arguments(parser):
    parser.add_argument('-data', type=str, required=True)
    parser.add_argument('-output', type=str, required=True)
    parser.add_argument('-no-random', dest='random', action='store_false')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    parser_cv = subparsers.add_parser('cv')
    add_global_arguments(parser_cv)
    parser_cv.add_argument('-cv-num', dest='cv_num', type=int, default=5)
    parser_cv.set_defaults(func=cv)

    parser_split = subparsers.add_parser('split')
    add_global_arguments(parser_split)
    parser_split.add_argument('-dev', dest='dev', type=float, default=0,
                              help='if dev == 0, do not split dev;\n'
                                   'if dev >= 1, dev means the number of dev;\n'
                                   'if 0 < dev < 1, dev means the ratio of data'
                              )
    parser_split.add_argument('-test', dest='test', type=float, default=0,
                              help='if test == 0, do not split test;\n'
                                   'if test >= 1, test means the number of test;\n'
                                   'if 0 < test < 1, test means the ratio of data'
                              )
    parser_split.set_defaults(func=split)

    args = parser.parse_args()
    args.func()
