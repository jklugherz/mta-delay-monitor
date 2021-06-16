import requests

import gtfs_realtime_pb2
from config import BLUE_LINE_URL, ORANGE_LINE_URL
from mta_key import MTA_API_KEY


def get_blue_line_updates():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url=BLUE_LINE_URL, headers={"x-api-key": MTA_API_KEY})

    feed.ParseFromString(response.content)
    print(len(feed.entity))
    print(sum([1 for ent in feed.entity if ent.HasField('trip_update')]))

    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip_update = entity.trip_update
            if trip_update.HasField('delay'):
                print('has delay')


if __name__ == '__main__':
    get_blue_line_updates()

