#!/usr/bin/env python3
import argparse
import time
from tqdm import trange
from pynput.mouse import Controller

parser = argparse.ArgumentParser()
parser.add_argument('--delay', type=float, required=True)
args = parser.parse_args()

seconds = int(args.delay * 3600)
mouse = Controller()

for i in trange(seconds, desc='Sleeping'):
    time.sleep(1)

    if i % 20 == 0:
        mouse.scroll(0, -1)
