from concurrent.futures import ThreadPoolExecutor, as_completed


def do_stuff(arg1, arg2):
    stuff



if __name__ == "__main__":
    threads = []
    with open("names.csv", "r") as f:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for line in f:
                line = line.split(",")
                threads.append(executor.submit(do_stuff, arg1, arg2))
