from rest_framework import generics


class RoadSegmentListView(generics.ListCreateAPIView):
    """
    API view to retrieve and create road segments.
    """
    pass 

class RoadSegmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a roada segment.
    """
    pass 
