from django.contrib import admin
from traffic_monitor.models import RoadSegment, SpeedReading, TrafficClassification


class SpeedReadingInline(admin.TabularInline):
    model = SpeedReading
    extra = 1 

class RoadSegmentAdmin(admin.ModelAdmin):
    fields = ('coordinate', 'road_length')
    inlines = [SpeedReadingInline]
    
class SpeedReadingAdmin(admin.ModelAdmin):
    pass

class TrafficClassificationAdmin(admin.ModelAdmin):
    pass


admin.site.register(RoadSegment, RoadSegmentAdmin)
admin.site.register(SpeedReading, SpeedReadingAdmin)
admin.site.register(TrafficClassification, TrafficClassificationAdmin)