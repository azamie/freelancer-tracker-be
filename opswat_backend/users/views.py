from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from .serializers import UserSerializer
from .serializers import UserSummarySerializer


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request):
        serializer = self.serializer_class(request.user, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSummarySerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
