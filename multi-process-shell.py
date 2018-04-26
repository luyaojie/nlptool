import multiprocessing as mp
import os
import subprocess
import sys

index_lock = mp.Lock()


def read_shell(filename):
    temp_list = list()
    with open(filename, 'r') as fin:
        for line in fin:
            temp_list.append(line.strip())
    return temp_list


def run_command(command):
    print(os.getpid(), command)
    # status = os.system(command)
    status = subprocess.call([command], shell=True)
    if status > 0:
        print("Run Err:", command)
        return 1
    else:
        print("Finished:", command)
        return 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser('Multi Process Run Shell')
    parser.add_argument('-s', dest='shell', help='Shell File Name')
    parser.add_argument('-n', dest='number', help='Process Number')
    args = parser.parse_args()

    shell_file = args.shell
    shell_list = read_shell(shell_file)
    pool = mp.Pool(args.number)
    print(pool.map(run_command, [path for path in shell_list]))
    pool.close()
    pool.join()
