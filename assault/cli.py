import click
import sys
import json
from datetime import datetime
from io import StringIO

from .http import assault
from .stats import Results

# un comment out to use on command line
@click.command()
@click.option("--requests", "-r", default=500, help="Number of requests")
@click.option("--concurrency", "-c", default=1, help="Number of concurrent requests")
@click.option("--json-file", "-j", default=None, help="Path to output JSON file")
@click.option("--append-json", "-a", default=0, help="Path to output JSON file")
@click.argument("url")


def cli(requests=500,concurrency=1,json_file='test.json',append_json=0,url="https://google.com"):
    total_time, request_dicts = assault(url, requests, concurrency)
    results = Results(total_time, request_dicts)
    display(results, url, requests, concurrency,json_file, append_json)


def display(results, url, requests,concurrency, json_file, append_json):
    output_file = None
    dump_dict = {
        "completed_time": str(datetime.now()),
        "url": url,
        "concurrency": concurrency,
        "total_requests": requests,
        "successful_requests": results.successful_requests(),
        "slowest": results.slowest(),
        "fastest": results.fastest(),
        "total_time": results.total_time,
        "requests_per_minute": results.requests_per_minute(),
        "requests_per_second": results.requests_per_second(),
    }
    if json_file:
        data = [dump_dict]
        try:
            old_data = json.load(open(json_file))
        except:
            old_data = []
            print("No old data")
        try:
            with open(json_file, "w+") as output_file:
                if append_json == 1:
                    try:
                        data = data + old_data
                    except Exception as e:
                        print(e)
                print(f"saving: {json_file}")
                json.dump(data, output_file)
        except:
            print("unable to open file")

    else:
        # Print to screen
        print(".... Done!")
        print("--- Results ---")
        print(f"Successful Requests\t{results.successful_requests()}")
        print(f"Slowest            \t{results.slowest()}s")
        print(f"Fastest            \t{results.fastest()}s")
        print(f"Total time         \t{results.total_time}s")
        print(f"Requests Per Minute\t{results.requests_per_minute()}")
        print(f"Requests Per Second\t{results.requests_per_second()}")
