from datetime import datetime


import pytz
import requests


from lyceum import settings
from users.models import Profile


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]

    return request.META.get("REMOTE_ADDR")


def get_timezone_from_ip(ip_address):
    if ip_address != "127.0.0.1":
        apis = [
            f"http://ip-api.com/json/{ip_address}",
            f"https://ipapi.co/{ip_address}/json",
        ]
        for api in apis:
            try:
                response = requests.get(api)
                response.raise_for_status()
                response_json = response.json()
                return response_json["timezone"]
            except Exception:
                pass

    return settings.TIME_ZONE


def birthday_context_processor(request):
    ip = get_client_ip(request)

    user_timezone = get_timezone_from_ip(ip)

    user_tz = pytz.timezone(user_timezone)
    current_date = datetime.now(user_tz)

    profiles_with_birthday_today = Profile.objects.filter(
        user__is_active=True,
        birthday__month=current_date.month,
        birthday__day=current_date.day,
    )

    return {"profiles_with_birthday_today": profiles_with_birthday_today}


__all__ = ["birthday_context_processor"]
