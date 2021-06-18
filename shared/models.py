from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import config, dataclass_json


@dataclass_json
@dataclass
class ActivePeriod:
    start: datetime = field(metadata=config(
        encoder=datetime.timestamp,
        decoder=datetime.fromtimestamp,
    ))
    end: Optional[datetime] = field(
        metadata=config(
            encoder=datetime.timestamp,
            decoder=datetime.fromtimestamp,
        ),
        default=None
    )


@dataclass_json
@dataclass
class Trip:
    route_id: str
    direction_id: int


@dataclass_json
@dataclass
class InformedEntity:
    agency_id: str
    trip: Optional[Trip] = None


@dataclass_json
@dataclass
class TransitRealtimeMercuryAlert:
    alert_type: str
    created_at: datetime = field(metadata=config(
        encoder=datetime.timestamp,
        decoder=datetime.fromtimestamp,
    ))
    display_before_active: int
    updated_at: datetime = field(metadata=config(
        encoder=datetime.timestamp,
        decoder=datetime.fromtimestamp,
    ))


@dataclass_json
@dataclass
class Alert:
    active_period: list[ActivePeriod]
    description_text: dict
    header_text: dict
    informed_entity: list[InformedEntity]
    transit_realtime_mercury_alert: TransitRealtimeMercuryAlert = field(
        metadata=config(field_name="transit_realtime.mercury_alert"))


@dataclass_json
@dataclass
class FeedEntity:
    id: str
    alert: Alert


@dataclass_json
@dataclass
class FeedResponse:
    header: dict
    entity: list[FeedEntity]
