
import json
import requests
import time

def requester(hw, val, i):
    data = {}
    params = dict(id="/" + hw + "/0/"+val+"/"+str(i), action="Get")
    print(val + " " + str(i))
    resp = requests.get(url="http://192.168.1.149:8085" + "/Sensor", params=params, timeout=10)
    print(resp.url)
    if resp.status_code == 200:
        data = json.loads(resp.text)
        print(data)
    return data

def main():
    hw = ["intelcpu", "gpu-nvidia"]
    val = ["temperature", "load"]
    i = 0
    while True:
        for h in hw:
            for v in val:
                data = requester(h, v, i)
        time.sleep(1.0)

if __name__ == '__main__':
    main()