from METAR import metar_get
from METAR import taf_get
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def time_convert(time_zulu):
    local_zone = "America/Chicago"
    # TAF forecast periods use Unix timestamps; METAR/TAF issue times are ISO strings
    if isinstance(time_zulu, (int, float)):
        utc_time = datetime.fromtimestamp(time_zulu, tz=timezone.utc)
    else:
        utc_time = datetime.fromisoformat(time_zulu.replace("Z", "+00:00"))
    changedTime = utc_time.astimezone(ZoneInfo(local_zone))

    return changedTime

def wind_convert(wind_degrees):
    # AWC reports variable winds as the string "VRB"
    if isinstance(wind_degrees, str):
        if wind_degrees.upper() == "VRB":
            return "Variable"
        wind_degrees = int(wind_degrees)

    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = int(((wind_degrees % 360) + 22.5) // 45) % 8
    return directions[index]

def speed_convert(wind_speed, end_measure):
    wind_speed = int(wind_speed)
    mph = wind_speed * 1.15078
    kmh = wind_speed * 1.852

    if end_measure == "mph":
        return (f"{round(mph, 1)}mph")
    if end_measure == "kmh":
        return kmh


TIME_KEYS = {"receiptTime", "reportTime", "obsTime","dbPopTime", "bulletinTime", "issueTime",
             "validTimeFrom", "validTimeTo", "timeFrom", "timeTo", "timeBec"}


def format_field(k, value):
    # Shared formatting for METAR and TAF fields
    if value is None:
        return f"{k}: {value}"
    if k in TIME_KEYS:
        return f"{k}: {time_convert(value)}"
    elif k == "wdir":
        return f"{k}: {wind_convert(value)}, Bearing {value}"
    elif k == "wspd" or k == "wgst":
        return f"{k}: {speed_convert(value, 'mph')}"
    elif (k == "temp" or k == "dewp") and not isinstance(value, list):
        return f"{k}: {value}C"
    elif k == "visib":
        return f"{k}: {value}Miles"
    elif k == "altim":
        return f"{k}: {value}mgM"
    else:
        return f"{k}: {value}"


def main():
    aic = "KOMA"

    metar = metar_get(aic)
    taf = taf_get(aic)

    for k in metar:
        print(format_field(k, metar[k]))

    print("---------------------------------------------------------------------")

    for k in taf:
        if k == "fcsts":
            # Each forecast period has its own wind/visibility/cloud data
            for i, fcst in enumerate(taf[k], start=1):
                print(f"\nForecast {i}:")
                for fk in fcst:
                    # Skip fields the TAF didn't forecast (API sends them as null / empty)
                    if fcst[fk] is None or fcst[fk] == []:
                        continue
                    print(f"    {format_field(fk, fcst[fk])}")
        else:
            print(format_field(k, taf[k]))

main()