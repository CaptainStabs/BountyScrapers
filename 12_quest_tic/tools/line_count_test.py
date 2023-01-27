import subprocess

import time

def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b

def function_timer():
	return time.perf_counter()


# This function simply calculates and prints the difference between the end and start times.
def time_dif(string, start, end):
	print(f"{string}: {end - start} seconds")

start = function_timer()
with open("F:\\_Bounty\\anthem_files.txt", "r",encoding="utf-8",errors='ignore') as f:
   print(sum(bl.count("\n") for bl in blocks(f)))
stop = function_timer()

time_dif("Time:", start, stop) 

with open("F:\\_Bounty\\anthem_files.txt", "r",encoding="utf-8",errors='ignore') as f:
	start = function_timer()
	print(len(f.readlines()))
	stop = function_timer()
	time_dif("readlines:", start, stop)