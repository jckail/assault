#!/usr/bin/env python
from assault import cli as c

config = {
    'domain':'google',
    'url':"https://google.com",
    'concurrency':3,
    'inital_requests':100
}


append_json = 1
if __name__ == "__main__":
    requests = config['inital_requests']
    for x in range(1,5):
        requests *= 10
        print('Requests: ',requests)
        print('Url: ',f"""{config['url']}""")
        print('File: ',f"""{config['domain']}.json""")
        c.cli(
        requests=requests,
        concurrency=config['concurrency'],
        json_file=f"""{config['domain']}.json""",
        append_json=append_json,
        url=f"""{config['url']}""")

