import csv
import multiprocessing as mp
from idxutils import gen_in_network_links, JSONOpen
from tqdm import tqdm
import traceback as tb

'''
Not entirely sure why I wrote this, 
I think I just fed it a csv file with a few urls as a test
'''

def process_row(row):
    try:
        files = [file for file in gen_in_network_links(row["url"])]
    except:
        try:
            files = [file for file in gen_in_network_links(row["url"])]
        except Exception:
            tb.print_exc()
            return None
    return files


def write_output(output_file, output):
    with open(output_file, 'a', newline='') as f:
        if output is not None:
            for row in output:
                f.write(row + "\n")

def process_csv(input_file, output_file):
        try:
            with open(input_file, 'r') as f:
                total = len(f.readlines())
                f.seek(0)
            # Use a pool of 4 worker processes
                reader = csv.DictReader(f)
                with mp.Pool(10) as pool:
                    for output in tqdm(pool.imap(process_row, reader), total=total, position=0, leave=False):
                        write_output(output_file, output)
                    pool.close()

        except KeyboardInterrupt:
            print("Quitting")
            pool.terminate()
            sys.exit()
        
        except Exception:
            pool.terminate()
            raise

        finally:
            pool.join()
            


if __name__ == '__main__':
    try:
        process_csv('UHC_indexes.csv', 'output2.csv')
    except KeyboardInterrupt:
        import sys; sys.exit(1)