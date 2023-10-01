import os, psutil

a = 10**1000000000000
process = psutil.Process(a)
print(process.memory_info().rss) 