import os

import psutil as psutil

# Create your views here.

memory_usage_dict = dict(psutil.virtual_memory()._asdict())
memory_usage_percent = memory_usage_dict["percent"]
print(f"BEFORE CODE: memory_usage_percent: {memory_usage_percent}%")
# current process RAM usage
pid = os.getpid()
current_process = psutil.Process(pid)
current_process_memory_usage_as_KB = current_process.memory_info()[0] / 2.0**20
print(f"BEFORE CODE: Current memory KB   : {current_process_memory_usage_as_KB: 9.3f} KB")

X = [i for i in range(0, 9000000)]
# AFTER  code
memory_usage_dict = dict(psutil.virtual_memory()._asdict())
memory_usage_percent = memory_usage_dict["percent"]
print(f"AFTER  CODE: memory_usage_percent: {memory_usage_percent}%")
