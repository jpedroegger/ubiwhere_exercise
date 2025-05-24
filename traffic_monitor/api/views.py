import datetime
from django.db.models import OuterRef, Subquery, Count, Q
from rest_framework import generics
from traffic_monitor.models import (
    RoadSegment,
    SpeedReading,
    TrafficClassification,
    TrafficRecord,
)
from rest_framework.response import Response
from traffic_monitor.api.serializers import (
    RoadSegmentSerializer,
    SpeedReadingSerializer,
    TrafficRecordSerializer,
)
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
    OpenApiResponse,
)
from traffic_monitor.utils.api_key_authentication import HasAPIKeyOrReadOnly
from traffic_monitor.utils.traffic_records_helper import get_or_create_car_dict, get_valide_uuids


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
                name="classification",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by: HIGH, MEDIUM, LOW",
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        classification_filter = self.request.query_params.get(
            "classification", ""
        ).upper()
        classification = None
        if classification_filter:
            try:
                classification = TrafficClassification.objects.get(
                    name=classification_filter
                )
            except TrafficClassification.DoesNotExist:
                return RoadSegment.objects.none()

        latest_speed_subquery = (
            SpeedReading.objects.filter(road_segment=OuterRef("pk"))
            .order_by("-created_at")
            .values("speed")[:1]
        )

        queryset = RoadSegment.objects.annotate(
            latest_speed=Subquery(latest_speed_subquery),
            speed_reading_count=Count("speed_readings"),
        ).prefetch_related("speed_readings")

        if classification:
            min_speed = classification.min_speed or 0
            max_speed = classification.max_speed or float("inf")
            queryset = queryset.filter(
                latest_speed__gte=min_speed, latest_speed__lte=max_speed
            )

        return queryset


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
                description="Successfully retrieved road segment details",
            ),
            404: OpenApiResponse(
                description="No RoadSegment matches the given query.",
            ),
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
            ),
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
            ),
        },
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
            ),
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
                description="List of speed readings retrieved successfully",
            ),
            400: OpenApiResponse(
                description="Bad Request",
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response=SpeedReadingSerializer,
                description="Speed reading created successfully",
            ),
            400: OpenApiResponse(
                description="Invalid input data",
            ),
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
                description="Successfully retrieved Speed Reading details",
            ),
            404: OpenApiResponse(
                description="No SpeedReading matches the given query.",
            ),
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
            ),
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
            ),
        },
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
            ),
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class TrafficRecordListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating Traffic Records.

    ### List Traffic Records
    Retrieves a list of traffic records. Optionally filter by car license plate (within the last 24 hours).

    **Query Parameters:**
    - `license_plate`: Filter traffic records by car license plate (only records from the last 24 hours are returned if this is provided).

    ### Create Traffic Records (chunks)
    Accepts a list of traffic records in chunks. Each object must include:
    - `car__license_plate`
    - `sensor__uuid`
    - `road_segment` (ID)
    - `timestamp`

    ### Any attempt to post against this endpoint must include an **API-Key**
    Records missing any of the required related objects will be skipped and returned in the `invalid_inputs` field of the response.
    """

    serializer_class = TrafficRecordSerializer
    permission_classes = [HasAPIKeyOrReadOnly]

    def get_queryset(self):
        license_plate = self.request.query_params.get("license_plate", None)

        traffic_records = TrafficRecord.objects.all().select_related(
            "car", "sensor", "road_segment"
        )

        if license_plate:
            date_range = datetime.datetime.now() - datetime.timedelta(days=1)
            traffic_records = TrafficRecord.objects.filter(
                Q(car__license_plate=license_plate) & Q(timestamp__gte=date_range)
            )
        return traffic_records

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=TrafficRecordSerializer(many=True),
                description="List of traffic records",
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        request=TrafficRecordSerializer(many=True),
        responses={
            201: OpenApiResponse(
                description="Traffic records created successfully. Some inputs may be invalid.",
            ),
            400: OpenApiResponse(
                description="Request payload must be a list of objects."
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            return Response({"error": "Expected a list of objects"}, status=400)

        license_plates = {item.get("car__license_plate") for item in data}
        sensor_uuids = {item.get("sensor__uuid") for item in data}
        segments = {item.get("road_segment") for item in data}

        road_segments = {
            road.id: road for road in RoadSegment.objects.filter(id__in=segments)
        }

        sensors = get_valide_uuids(sensor_uuids)
        cars = get_or_create_car_dict(license_plates)

        prepared_data = []
        errors = []

        for idx, item in enumerate(data):

            car = cars.get(item.get("car__license_plate"))
            sensor = sensors.get(item.get("sensor__uuid"))
            segment = road_segments.get(item.get("road_segment"))
            timestamp = item.get("timestamp", None)

            if not sensor or not segment or not car or not timestamp:
                errors.append(
                    {
                        "index": idx,
                        "error": "Missing related object",
                        "car__license_plate": item.get("car__license_plate"),
                        "sensor__uuid": item.get("sensor__uuid"),
                        "timestamp": item.get("timestamp"),
                        "road_segment": item.get("road_segment"),
                    }
                )
                continue

            prepared_data.append(
                {
                    "car": car.id,
                    "sensor": sensor.id,
                    "road_segment": segment.id,
                    "timestamp": timestamp,
                }
            )

        serializer = self.get_serializer(data=prepared_data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = serializer.data
        if errors:
            response = {"invalid_inputs": errors, "data": serializer.data}
        return Response(response, status=201)
