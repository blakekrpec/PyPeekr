
import json
import requests
import time


def requester(hw, val, i):
    data = {}
    params = dict(id="/" + hw + "/0/"+val+"/"+str(i), action="Get")

    # TODO:  get IP from settings.yaml
    resp = requests.get(url="http://192.168.1.137:8080" +
                        "/Sensor", params=params, timeout=10)
    print(resp.url)
    if resp.status_code == 200:
        data = json.loads(resp.text)
        print(data)
    else:
        print("Request returned non 200 status code.")
    return


def main():
    hw = ["intelcpu", "gpu-nvidia"]
    val = ["temperature", "load"]
    i = 0
    while True:
        for h in hw:
            for v in val:
                requester(h, v, i)
        time.sleep(1.0)


if __name__ == '__main__':
    main()
