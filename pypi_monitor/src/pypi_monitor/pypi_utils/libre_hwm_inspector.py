import json
import requests


# TODO: get IP for this from settings.yaml
def requester():
    resp = requests.get(url="http://192.168.1.137:8080" +
                        "/data.json", timeout=10)
    data = json.loads(resp.text)
    return data


def write_to_file(data):
    with open("data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


def main():
    data = requester()
    write_to_file(data)


if __name__ == '__main__':
    main()
