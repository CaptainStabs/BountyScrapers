import argparse
from tqdm import tqdm


def count_lines(filename):
	lines = 0
	with open(filename, 'r') as f:
		for line in tqdm(f):
			lines += 1
	print(lines)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', "--file", type=str)
	args = parser.parse_args()
	count_lines(args.file)