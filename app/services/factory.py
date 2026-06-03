from __future__ import annotations

from datetime import datetime, timezone


def get_factory_storage_status() -> dict[str, int | str]:
    return {
        "facility": "java-main-plant",
        "available_tons": 180,
        "reserved_tons": 45,
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }


def get_active_logistics_tracking() -> dict[str, int | str]:
    return {
        "on_the_way": 12,
        "anonymous_tracking_id": "fleet-java-region",
    }
