from scraper_func import scraper
from multiprocessing import Pool
import sys
import traceback as tb

def run_parallel():
    arguments = []
    end_id = 3333333 #45899
    # start_num is supplemental for first run and is only used if the files don't exist
    for i in range(3):
        if i == 0:
            start_num = 0
        else:
            # Use end_id before it is added to
            start_num = end_id - 3333333
        print("Startnum: " + str(start_num))
        arguments.append([f"./files/extracted_data{i}.csv", start_num, end_id])
        end_id = end_id + 3333333
    print(arguments)

    try:
        pool = Pool(processes=len(arguments))
        pool.starmap(scraper, arguments)
        # for _ in tqdm(pool.istarmap(scraper, arguments), total=len(arguments)):
        #     pass
        pool.close()
        # pool.starmap(scraper, arguments), total=len(arguments)
    except KeyboardInterrupt:
        print("Quitting")
        pool.terminate()
        sys.exit()
    except Exception:
        tb.print_exc()
        pool.terminate()
        raise
    finally:
        print("   [*] Joining pool...")
        pool.join()
        sys.exit()
        print("   [*] Finished joining...")
        sys.exit(1)

if __name__ == "__main__":
    run_parallel()
