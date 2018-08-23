#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by Roger on 2018/8/21
import os
import re
import sys

import pandas as pd


def exp_result_to_list(exp_result):
    re_num = re.compile(" \d+[.]?\d*")
    return [float(num) for num in re_num.findall(exp_result)]


def main(result_folder, output_xlsx=None):
    grep_str = "Best Dev  Type"
    grep_shell_str = "grep \"%s\" %s/*" % (grep_str, result_folder)
    result_str = os.popen(grep_shell_str).read().strip()
    results = list()
    for line in result_str.split('\n'):
        split_index = line.index(':')
        exp_file_name = line[:split_index]
        exp_result_list = exp_result_to_list(line[split_index + 1:])
        results += [exp_result_list + [exp_file_name]]
    results.sort(reverse=True, key=lambda x: x[7])
    data_frame = pd.DataFrame(results,
                              columns=["Epoch", "Batch", "Dev P", "Dev R", "Dev F1",
                                       "Tst P", "Tst R", "Tst F1", "Exp Name"])
    if output_xlsx:
        data_frame.to_excel(output_xlsx, header=True, index=True,)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
