import xxhash
import sys
import os
import time
import requests

print("Welcome to Chainy Miner v1.0")
try:
    os.mkdir(".chainy")
except Exception:
    pass
BASE_URL = "http://45.138.72.87"
try:
    address = open(".chainy/addr").read()
    print(f"Starting mining on {address}")
except Exception:
    address = str(input("Enter your address:"))
    open(".chainy/addr", "w").write(address)
try:
    while True:
        a = requests.post(f"{BASE_URL}/getJob?address={address}").json()
        hashs = a["hash"]
        jobId = a["jobId"]
        print(f"Getted job {jobId} with  {hashs} hash.")
        for nonce in range(7500000 + 1):
            hashk = xxhash.xxh64(f"{hashs}{nonce}").hexdigest()
            if hashk == a["jobEnd"]:
                response = requests.post(
                    f"{BASE_URL}/submitJob?address={address}&jobId={jobId}&nonce={nonce}"
                ).json()
                print(f"Calculated job {jobId}")
                print(response)
                balance = requests.post(f"{BASE_URL}/balance?address={address}").json()
                print(f"Your balance is {balance}")
except Exception as err:
    print(f"Error is {err}")
    os.execv(sys.argv[0], sys.argv)
