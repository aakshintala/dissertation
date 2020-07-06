#!/usr/bin/env python

import re
import sys

worker_log = open(sys.argv[1])

# grep timestamp lines
worker_ts = []
for line in worker_log:
    if re.search("icp_sal_DcPollInstance", line) or re.search("cpaDcCompressData2", line):
        worker_ts.append(line)

# grep DcPollInstance and DcCompressData2
dc_poll = []
cp_data = []
for line in worker_ts:
    if re.search("icp_sal_DcPollInstance", line) and (re.search("after_unmarshal", line) or re.search("after_execution", line)):
        dc_poll.append(line)
    if re.search("cpaDcCompressData2", line) and (re.search("after_unmarshal", line) or re.search("after_execution", line)):
        cp_data.append(line)

def get_ts(log):
    ts = []
    for line in log:
        result = re.search('.*at\s:\s(\d*)\ss,\s(\d*)', line)
        ts.append((result.group(1), result.group(2)))
    return ts

def subtime(ts_start, ts_end):
    delta = (int(ts_end[0]) - int(ts_start[0])) * 1000.0 + (int(ts_end[1]) - int(ts_start[1])) / 1000.0
    return delta

dc_poll = get_ts(dc_poll)
cp_data = get_ts(cp_data)
i = 0
j = 0
total = 0

while i < len(dc_poll) and j < len(cp_data):
    if subtime(dc_poll[i], cp_data[j]) > 0: # dc_poll is earlier
        if subtime(dc_poll[i+1], cp_data[j]) >= 0: # no overlap
            pass
        else:
            if subtime(dc_poll[i+1], cp_data[j+1]) > 0: # has overlap
                cp_data[j] = dc_poll[i+1]
            else: # dc_poll contains cp_data
                j = j + 2
        total += subtime(dc_poll[i], dc_poll[i+1])
        i = i + 2

    else:
        if subtime(cp_data[j+1], dc_poll[i]) >= 0: # no overlap
            pass
        else:
            if subtime(cp_data[j+1], dc_poll[i+1]) > 0: # has overlap
                dc_poll[j] = cp_data[j+1]
            else: # dc_poll contains cp_data
                i = i + 2
        total += subtime(cp_data[j], cp_data[j+1])
        j = j + 2

print(total)
