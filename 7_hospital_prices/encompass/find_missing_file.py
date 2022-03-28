import os

directory = "./output_files/"

with open("hospitals.csv", "r") as f:
    nums = []
    for lines in f:
        nums.append(lines.split(",")[0])

    print(len(nums))

    for file in os.listdir(directory):
        if file.strip(".csv") not in nums:
            print(file)
