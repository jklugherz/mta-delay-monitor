import os
import re
import requests

from shared.db import upsert_active_alert_duration, set_is_delayed, end_active_alert
from shared.models import FeedResponse


SUBWAY_ALERT_JSON_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts.json"


def get_alerts():
    response = requests.get(url=SUBWAY_ALERT_JSON_URL, headers={"x-api-key": os.environ.get('MTA_API_KEY')})
    feed_response = FeedResponse.from_json(response.content)

    for entity in feed_response.entity:
        alert = entity.alert

        if alert.transit_realtime_mercury_alert.alert_type == "Delays":
            alert_id = entity.id  # lmm:alert:79937
            alert_text = alert.description_text.get('translation')[0].get('text')  # [E][F] and [R] trains are delayed in both directions while we work to correct a signal malfunction between Forest Hills-71 Av and Queens Plaza.
            lines = [line[1:len(line)-1] for line in re.findall(r'\[.*?\]', alert_text)]  # ['E', 'F', 'R']

            # TODO: refactor so we don't create 1 new db connection for each line - use openjson
            if not alert.active_period:
                # Delay is still active, create or update new alert record and make line delayed
                alert_start = alert.transit_realtime_mercury_alert.created_at
                for line_id in lines:
                    print(f"Line {line_id} is experiencing delays.")
                    upsert_active_alert_duration(line_id, alert_id, alert_start)
                    set_is_delayed(line_id, is_delayed=True)
            else:
                # Delay is over, update alert record and make line not delayed
                alert_end = alert.active_period[0].end
                for line_id in lines:
                    print(f"Line {line_id} is now recovered.")
                    end_active_alert(line_id, alert_id, alert_end)
                    set_is_delayed(line_id, is_delayed=False)


if __name__ == '__main__':
    get_alerts()

