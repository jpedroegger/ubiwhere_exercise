from django.contrib import admin
from traffic_monitor.models import RoadSegment, SpeedReading, TrafficClassification, Car, Sensor, TrafficRecord


class SpeedReadingInline(admin.TabularInline):
    model = SpeedReading
    extra = 1 

class RoadSegmentAdmin(admin.ModelAdmin):
    fields = ('coordinate', 'road_length')
    inlines = [SpeedReadingInline]
    list_display = ["id", "__str__" ]
    
class SpeedReadingAdmin(admin.ModelAdmin):
    pass

class TrafficClassificationAdmin(admin.ModelAdmin):
    pass

class CarAdmin(admin.ModelAdmin):
    list_display = ["id", 'license_plate']

class SensorAdmin(admin.ModelAdmin):
    pass

class TrafficRecordAdmin(admin.ModelAdmin):
    pass


admin.site.register(RoadSegment, RoadSegmentAdmin)
admin.site.register(SpeedReading, SpeedReadingAdmin)
admin.site.register(TrafficClassification, TrafficClassificationAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(TrafficRecord, TrafficRecordAdmin)