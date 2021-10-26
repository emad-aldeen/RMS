from django.db import models
from users.models import User


class Point(models.Model):
    PRIZES = {
        ('RESUBMIT', 'RESUBMIT'),
        ('+1_MARK', '+1_MARK'),
        ('WAIVE_LATE_ATTENDANCE', 'WAIVE_LATE_ATTENDANCE'),
        ('WAIVE_LATE_SUBMISSION', 'WAIVE_LATE_SUBMISSION'),
        ('RANDOM_3D_ITEM', 'RANDOM_3D_ITEM'),
        ('DONATE', 'DONATE'),
    }
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    prize = models.CharField(max_length=80, choices=PRIZES, blank=True)
    is_confirmed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_donated = models.BooleanField(default=False) 
    donated_from = models.CharField(max_length=50, blank=True)
    donated_to = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.owner.username