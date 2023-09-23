from django.db import models


class PollData(models.Model):
    store_id = models.CharField(max_length=255)
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=10)  # Assuming 'active' or 'inactive'

    def __str__(self):
        return f"{self.store_id} - {self.timestamp_utc}"


class BusinessHours(models.Model):
    store_id = models.CharField(max_length=255)
    day_of_week = models.PositiveIntegerField()  # 0=Monday, 1=Tuesday, ..., 6=Sunday
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    def __str__(self):
        return f"{self.store_id} - {self.get_day_of_week_display()}"


class Timezone(models.Model):
    store_id = models.CharField(max_length=255)
    timezone_str = models.CharField(max_length=255, default='America/Chicago')

    def __str__(self):
        return f"{self.store_id} - {self.timezone_str}"

