from django.contrib import admin
from traffic_monitor.models import RoadSegment, SpeedReading


class RoadSegmentAdmin(admin.ModelAdmin):
    pass

class SpeedReadingAdmin(admin.ModelAdmin):
    pass


admin.site.register(RoadSegment, RoadSegmentAdmin)
admin.site.register(SpeedReading, SpeedReadingAdmin)