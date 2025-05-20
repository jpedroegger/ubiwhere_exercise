from django.urls import path
from traffic_monitor.api.views import RoadSegmentListView, RoadSegmentDetailView, SpeedReadingListView, SpeedReadingDetailView


urlpatterns = [
    path('road_segments/', RoadSegmentListView.as_view(), name='road-segment-list'),
    path('road_segments/<int:pk>/', RoadSegmentDetailView.as_view(), name='road-segment-detail'),
    path('speed_readings/', SpeedReadingListView.as_view(), name='speed-reading-list'),
    path('speed_readings/<int:pk>/', SpeedReadingDetailView.as_view(), name='speed-reading-detail'),
]