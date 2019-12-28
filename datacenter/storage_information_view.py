from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone
from datetime import time, timedelta

def format_duration(duration):
  seconds_in_day = 3600 * 24
  duration_in_seconds = int(duration.total_seconds())
  if duration_in_seconds <= seconds_in_day:
    hours, minutes = duration_in_seconds // 3600, duration_in_seconds // 60 % 60
    seconds = duration_in_seconds - hours*3600 - minutes*60
  else:
    hours, minutes = duration_in_seconds // 3600, duration_in_seconds // 60 % 60
    seconds = duration_in_seconds - hours*3600 - minutes*60

  return '{:%H:%M:%S}'.format(time(hours, minutes, seconds))

def storage_information_view(request):
    non_closed_users = Visit.objects.filter(leaved_at=None)
    now = timezone.now()

    non_closed_visits = [{"who_entered": user.passcard.owner_name, 
                          "date": user.entered_at, 
                          "duration": format_duration(now - user.entered_at)} for user in non_closed_users]
    
    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
