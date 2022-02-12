import os
from loguru import logger
import requests
import xxhash
import threading
import time
from cpuinfo import get_cpu_info_json
import json

# Настройка майнера

debug = False
BASE_URL = "http://mc.eremenkod.ru"
DIFF = 7500000


# Настройка майнера


logger.info("Welcome to Chainy Miner v2.0")

# PARSING START

try:
    os.mkdir(".chainy")
except Exception:
    pass


try:
    address = open(".chainy/addr").read()
    logger.info(f"Starting mining on {address}")
except Exception:
    address = str(input("Enter your address:"))
    open(".chainy/addr", "w").write(address)

cpu = get_cpu_info_json()
threads = json.loads(cpu)
threads = threads["count"]

# PARSING STOP

# JOB PARSER START


def parseJob(job, type):
    return job[f"{type}"]


# JOB PARSER STOP


# MINER START
def miner(address, job):
    global lockPool
    jobId = parseJob(job, "jobId")
    _hash = parseJob(job, "hash")
    taskhash = parseJob(job, "jobEnd")
    for nonce in range(DIFF + 1):
        curhash = xxhash.xxh64(f"{_hash}{nonce}").hexdigest()
        if licvid:
            if debug:
                logger.debug("licvid work")
            break
        if curhash == taskhash:
            logger.info(f"Calculated job {jobId} with {nonce} nonce. ")
            if debug:
                logger.debug("Sending request to server")
            response = requests.post(
                f"{BASE_URL}/submitJob?address={address}&jobId={jobId}&nonce={nonce}"
            ).json()
            if debug:
                logger.debug(response)
            lockPool = False
        if licvid:
            if debug:
                logger.debug("licvid work")
            break


# MINER STOP

# POOLER START
lockPool = False
while True:
    if not lockPool:
        licvid = True
        time.sleep(1)
        licvid = False
        for i in range(threads):
            job = requests.post(f"{BASE_URL}/getJob?address={address}").json()
            x = threading.Thread(target=miner, args=(address, job))
            jobId = parseJob(job, "jobId")
            x.name = f"Jobber-{jobId}"

            x.start()
            lockPool = True
            _jobId = jobId + threads
        _hash = parseJob(job, "hash")
        logger.info(
            f"Getted {threads} jobs from {jobId} to {_jobId}  with  {_hash} hash."
        )
    time.sleep(0.5)


# POOLER STOP
