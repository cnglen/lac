#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
对infer.py进行封装，支持file input, file output
"""

import argparse
import os
import glob
import shlex
import subprocess


def main():
    """
    lac 分词
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-if", "--input-file", help="path of input file")
    parser.add_argument("-of", "--output-file", help="path of output file", default=None)
    parser.add_argument("-bs", "--batch-size", help="batch size", default=16, type=int)
    args = parser.parse_args()
    input_file = os.path.abspath(args.input_file)
    output_file = os.path.abspath(args.input_file) + "_lac_output.txt" if args.output_file is None else args.output_file

    # make sure of one file in
    input_data_dir = os.path.dirname(input_file)
    all_files = [e for e in glob.glob(os.path.join(input_data_dir, "*")) if not e.endswith("_lac_output.txt")]

    if len(all_files) > 1:
        raise ValueError("确保input_file所在文件夹只有一个文件")

    os.chdir(os.path.expanduser("~/lac"))  # 假设lac仓库在home目录
    cmd = "python python/infer.py --batch_size {} --test_data_dir {}".format(args.batch_size, input_data_dir)
    with open(output_file, "w") as f_out:
        subprocess.call(shlex.split(cmd), stdout=f_out)

    # 对剩下的尾巴进行分词
    n_doc = sum(1 for _ in open(args.input_file))
    n_doc_remaining = n_doc % args.batch_size
    tmp_remaining_input_file = "/tmp/lac_remaining_input/input.txt"
    tmp_remaining_output_file = "/tmp/lac_remaining_output/output.txt"
    os.makedirs(os.path.dirname(tmp_remaining_input_file))
    os.makedirs(os.path.dirname(tmp_remaining_output_file))

    cmd_tail = "tail -n {} {} > {}".format(args.input_file, n_doc_remaining, tmp_remaining_input_file)
    subprocess.call(shlex.split(cmd_tail))

    cmd2 = "python python/infer.py --batch_size {} --test_data_dir {}".format(1, os.path.dirname(tmp_remaining_input_file))
    with open(tmp_remaining_output_file, "w") as f_out:
        subprocess.call(shlex.split(cmd2), stdout=f_out)

    with open(output_file, "a") as f_output, open(tmp_remaining_output_file, "r") as f:
        f_output.writelines(f.readlines())


if __name__ == '__main__':
    main()
