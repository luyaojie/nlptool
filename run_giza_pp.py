#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Created by Roger on 2018/1/12
import sys
import os
import subprocess

giza_dir = "~/.tool/giza-pp/GIZA++-v2"


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


def run_giza(src, trg):
    """
    Run Giza Script
    :param src: source file name
    :param trg: trg file name
    :return:
    """

    """
    Step 1: Create files needed for GIZA++
    Files created by plain2snt
        - {src}.vcb
            1. each word from the {src} corpus
            2. corresponding frequency count for each word
            3. an unique id for each word
        - {trg}.vcb
            same as {src}.vcb
        - {src}_{trg}.snt
            each sentence from the parallel {src} and {trg} corpi translated
            into the unique number for each word
        - {trg}_{src}.snt
            same as {src}.vcb
    """
    step1_sh = "%s %s %s" % ("%s/plain2snt.out" % giza_dir, src, trg)
    run_command(step1_sh)

    """
    Step 2: Generate co-occurrence file
    Files created by this step
        - {src}_{trg}.cooc
    """
    src_trg_snt_file = "%s_%s.snt" % (src, trg)
    src_trg_cooc_file = "%s_%s.cooc" % (src, trg)
    src_vocab = "%s.vcb" % src
    trg_vocab = "%s.vcb" % trg
    step2_sh = "%s %s %s %s > %s" % ("%s/snt2cooc.out" % giza_dir, src_vocab, trg_vocab,
                                     src_trg_snt_file, src_trg_cooc_file)
    run_command(step2_sh)

    """
    Step 3: Run GIZA++
    Files created by this step
        - Decoder.config
            file used with the ISI Rewrite Decoder
            http://www.isi.edu/licensed-sw/rewrite-decoder/
        - trn.src.vc
            similar to {src}.vcb
        - trn.trg.vcb
            similar to {trg}.vcb
        - tst.src.vcb
            blank
        - tst.trg.vcb
            blank
        - ti.final
        

    """
    step3_sh = "%s -S %s -T %s -C %s -CoocurrenceFile %s" % ("%s/GIZA++" % giza_dir,
                                                             src_vocab, trg_vocab, src_trg_snt_file, src_trg_cooc_file)
    run_command(step3_sh)


if __name__ == "__main__":
    run_giza(sys.argv[1], sys.argv[2])
