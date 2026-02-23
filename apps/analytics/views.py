from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import get_dashboard_data
from .serializers import DashboardSerializer


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_dashboard_data(request.user)
        serializer = DashboardSerializer(data)
        return Response(serializer.data)