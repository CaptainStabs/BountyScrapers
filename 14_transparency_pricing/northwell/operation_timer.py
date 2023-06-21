import os
import timeit

print(timeit.timeit(os.system(f'cd /D F:\\_Bounty\\transparency-in-pricing\\ & dolt gc')))
