import googlesearch as google
from tqdm import tqdm

ignored_domains = ["google"]
remove_words = ["?mode=create"]
print("   [*] Loop start")

with open("ardent_hospitals.csv", "r") as f:
    with open("homepages.csv", "a") as output_csv:
        for line in tqdm(f):
            search_query = line.split(",")[0]

            for results in google.search(search_query, tld="com", lang="en", num=10, start=0, stop=10, pause=0.3):
                # print("All result: " + results
                # print("   All result: " + results)

                if not any(ignored_domain in results for ignored_domain in ignored_domains):
                    output_csv.write(",".join([search_query,results + "cost-care"]) + "\n")
