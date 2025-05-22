from django.db.models import OuterRef, Subquery
from rest_framework import generics
from traffic_monitor.models import RoadSegment, SpeedReading, TrafficClassification
from traffic_monitor.api.serializers import RoadSegmentSerializer, SpeedReadingSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
    OpenApiResponse,
)



class RoadSegmentListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating road segments with optional traffic classification filtering.

    ### List Road Segments
    Returns a list of all road segments. Can be filtered by traffic classification.

    ### Create Road Segment
    Creates a new road segment with the provided data.

    ### Filtering
    You can filter road segments by traffic classification by providing a `classification` query parameter.
    The system will then return only segments where the latest speed reading falls within the
    classification's speed range.

    Available classification names (case-insensitive):
    - HIGH
    - MEDIUM
    - LOW
    """
    queryset = RoadSegment.objects.none()
    serializer_class = RoadSegmentSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='classification',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by: HIGH, MEDIUM, LOW',
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        classification_filter = self.request.query_params.get('classification', None)
        
        if not classification_filter:
            return RoadSegment.objects.all()

        try:
            classification = TrafficClassification.objects.get(name=classification_filter.upper())
        except TrafficClassification.DoesNotExist:
            return RoadSegment.objects.none()
        latest_readings = SpeedReading.objects.filter(
            road_segment=OuterRef('pk')
        ).order_by('-created_at')
        
        return RoadSegment.objects.annotate(
            latest_speed=Subquery(latest_readings.values('speed')[:1])
        ).filter(
            latest_speed__gte=classification.min_speed or 0,
            latest_speed__lte=classification.max_speed or float('inf')
        )


class RoadSegmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating or deleting road segments.

    ### Retrieve Road Segment
    Returns detailed information about a specific road segment.

    ### Update Road Segment
    Fully updates all fields of a road segment with the provided data.

    ### Partial Update
    Partially updates a road segment with the provided fields.

    ### Delete Road Segment
    Removes a road segment from the system.
    """
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer 
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=RoadSegmentSerializer,
                description="Successfully retrieved road segment details"
            ),
            404: OpenApiResponse(
                description="No RoadSegment matches the given query.",
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=RoadSegmentSerializer,
                description="Road segment successfully updated",
            ),
            400: OpenApiResponse(
                description="Invalid input data",
            ),
            404: OpenApiResponse(
                description="No Road Segment matches the given query.",
            )
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @extend_schema(
    request=RoadSegmentSerializer,
    responses={
        200: OpenApiResponse(
            response=RoadSegmentSerializer,
            description="Road Segment partially updated",
        ),
        400: OpenApiResponse(
            description="Invalid input data",
        ),
        404: OpenApiResponse(
            description="No Road Segment matches the given query.",
        )
    }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
    responses={
        204: OpenApiResponse(
            description="Road Segment deleted successfully",
        ),
        404: OpenApiResponse(
            description="No Road Segment matches the given query.",
        )
    }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)



class SpeedReadingListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating speed readings.

    ### List Speed Readings
    Returns a list of all speed readings recorded in the system.

    ### Create Speed Reading
    Records a new speed reading for a specific road segment.
    """
    queryset = SpeedReading.objects.all()
    serializer_class = SpeedReadingSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=SpeedReadingSerializer(many=True),
                description="List of speed readings retrieved successfully"
            ),
            400: OpenApiResponse(
                description="Bad Request",
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=SpeedReadingSerializer,
                description="Speed reading created successfully"
            ),
            400: OpenApiResponse(
                description="Invalid input data",
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SpeedReadingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating or deleting speed readings.

    ### Retrieve Speed Reading
    Returns detailed information about a specific Speed Reading.

    ### Update Speed Reading
    Fully updates all fields of a Speed Reading with the provided data.

    ### Partial Update
    Partially updates a Speed Reading with the provided fields.

    ### Delete Speed Reading
    Removes a Speed Reading from the system.
    """
    queryset = SpeedReading.objects.all()
    serializer_class = SpeedReadingSerializer 
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=SpeedReadingSerializer,
                description="Successfully retrieved Speed Reading details"
            ),
            404: OpenApiResponse(
                description="No SpeedReading matches the given query.",
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=SpeedReadingSerializer,
                description="Speed Reading successfully updated",
            ),
            400: OpenApiResponse(
                description="Invalid input data",
            ),
            404: OpenApiResponse(
                description="No SpeedReading matches the given query.",
            )
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @extend_schema(
    request=SpeedReadingSerializer,
    responses={
        200: OpenApiResponse(
            response=SpeedReadingSerializer,
            description="Speed Reading partially updated",
        ),
        400: OpenApiResponse(
            description="Invalid input data",
        ),
        404: OpenApiResponse(
            description="No SpeedReading matches the given query.",
        )
    }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
    responses={
        204: OpenApiResponse(
            description="Speed Reading deleted successfully",
        ),
        404: OpenApiResponse(
            description="No SpeedReading matches the given query.",
        )
    }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
