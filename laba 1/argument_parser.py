import argparse
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, required=False)

    parsed = parser.parse_args()

    port = parsed.port

    if port is None:
        port = 8080

    return {"port": port}
