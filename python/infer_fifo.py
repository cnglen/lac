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
    args = parser.parse_args()
    input_file = os.path.abspath(args.input_file)
    output_file = os.path.abspath(args.input_file) + "_lac_output.txt" if args.output_file is None else args.output_file

    # make sure of one file in
    input_data_dir = os.path.dirname(input_file)
    all_files = [e for e in glob.glob(os.path.join(input_data_dir, "*")) if not e.endswith("_lac_output.txt")]

    if len(all_files) > 1:
        raise ValueError("确保input_file所在文件夹只有一个文件")

    os.chdir(os.path.expanduser("~/lac"))  # 假设lac仓库在home目录
    cmd = "python python/infer.py --batch_size 1 --test_data_dir {}".format(input_data_dir)
    # print(cmd)
    # print(output_file)
    with open(output_file, "w") as f_out:
        subprocess.call(shlex.split(cmd), stdout=f_out)


if __name__ == '__main__':
    main()
