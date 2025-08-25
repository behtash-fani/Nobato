from datetime import date, time
from typing import Iterable, List, Tuple

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from .models import Availability, Booking

Minutes = int
Slot = Tuple[time, time]


def _to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute


def _from_minutes(m: int) -> time:
    h, mm = divmod(m, 60)
    return time(h, mm)


def _slice_interval(start: time, end: time, step: int, buffer_minutes: int = 0) -> List[Slot]:
    s = _to_minutes(start)
    e = _to_minutes(end)
    out: List[Slot] = []
    while s + step <= e:
        ss = s
        ee = s + step
        out.append((_from_minutes(ss), _from_minutes(ee)))
        s += step
    return out


def has_any_availability(profile_obj) -> bool:
    ctype = ContentType.objects.get_for_model(profile_obj.__class__)
    return Availability.objects.filter(
        professional_content_type=ctype,
        professional_object_id=profile_obj.pk
    ).exists()


def covering_availabilities_for(profile_obj, day: date) -> Iterable[Availability]:
    py_wd = day.weekday()        # Monday=0
    avail_wd = (py_wd + 1) % 7   # Saturday=0
    ctype = ContentType.objects.get_for_model(profile_obj.__class__)
    return Availability.objects.filter(
        professional_content_type=ctype,
        professional_object_id=profile_obj.pk
    ).filter(
        Q(specific_date=day) | Q(specific_date__isnull=True, weekday=avail_wd)
    ).order_by('start_time')


def busy_slots_for(profile_obj, day: date) -> List[Slot]:
    ctype = ContentType.objects.get_for_model(profile_obj.__class__)
    qs = Booking.objects.filter(
        professional_content_type=ctype,
        professional_object_id=profile_obj.pk,
        date=day
    ).exclude(status=Booking.STATUS_CANCELED)
    return [(b.start_time, b.end_time) for b in qs]


def free_slots_for_date(profile_obj, day: date, step_minutes: int = 30, buffer_minutes: int = 0) -> List[Slot]:
    avs = list(covering_availabilities_for(profile_obj, day))
    if not avs:
        return []
    busy = busy_slots_for(profile_obj, day)
    out: List[Slot] = []
    for av in avs:
        chunks = _slice_interval(av.start_time, av.end_time, step_minutes, buffer_minutes)
        for s, e in chunks:
            if any(s < be and e > bs for bs, be in busy):
                continue
            out.append((s, e))
    return out
