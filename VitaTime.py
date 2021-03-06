import datetime
import random
import time

import psvtrophyisgoodRandomTime


def utc_to_local(dt):
    if time.localtime().tm_isdst:
        return dt - datetime.timedelta(seconds = time.altzone)
    else:
        return dt - datetime.timedelta(seconds = time.timezone)

def local_to_utc(dt):
    if time.localtime().tm_isdst:
        return dt + datetime.timedelta(seconds = time.altzone)
    else:
        return dt + datetime.timedelta(seconds = time.timezone)

def decodeTimestamp(timestamp):
    timestamp = int(timestamp,16)
    dt = datetime.datetime.fromordinal(1) + datetime.timedelta(microseconds=timestamp)
    dt = dt.replace(microsecond=0)
    return utc_to_local(dt)



def encodeTimestamp(dateandtime):
    dt = datetime.datetime.strptime(dateandtime, "%Y-%m-%d %H:%M:%S.%f")
    dt = local_to_utc(dt)
    timestamp = (dt - datetime.datetime(1, 1, 1)).total_seconds() * 1000000
    timestamp = hex(int(timestamp))[2:]
    if timestamp.endswith("L"):
        timestamp = timestamp[:-1]
    return timestamp


def genRandomTime(min,max):
    min = int(min,16)
    max = int(max,16)
    timestamp = random.randrange(min,max,1)
    timestamp = hex(timestamp)
    if timestamp.startswith("0x"):
        timestamp = timestamp[2:]
    if timestamp.endswith("L"):
        timestamp = timestamp[:-1]
    print timestamp
    return timestamp