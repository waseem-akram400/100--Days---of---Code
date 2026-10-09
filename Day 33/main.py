from sunrise import get_sunrise_sunset
from iss import iss_is_overhead
import datetime

sunrise, sunset = get_sunrise_sunset()
now = datetime.datetime.now(datetime.timezone.utc)

print(f"Sunrise: {sunrise}")
print(f"Sunset: {sunset}")
print(f"Now UTC: {now}")

if iss_is_overhead() and (now < sunrise or now > sunset):
    print("UPAR DEKHO! ISS nazar aa raha hai!")
else:
    print("ISS abhi upar nahi hai.")