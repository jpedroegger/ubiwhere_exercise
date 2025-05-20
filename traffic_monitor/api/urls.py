from django.urls import path
from traffic_monitor.api.views import RoadSegmentListView, RoadSegmentDetailView


urlpatterns = [
    path('road_segments/', RoadSegmentListView.as_view(), name='road-segment-list'),
    path('road_segments/<int:pk>/', RoadSegmentDetailView.as_view(), name='road-segment-detail'),
]