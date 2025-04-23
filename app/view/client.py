from rest_framework import viewsets
from app.models.client import Client
from app.serializers.client import CleintSerializer,ClientCreateSerializer
from ..pagination .paginations import DefaultLimitOffSetPagination
from rest_framework.permissions import IsAuthenticated

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter().order_by('-updated_at')
    serializer_class = CleintSerializer
    pagination_class = DefaultLimitOffSetPagination
    permission_classes = [IsAuthenticated]


    def get_serializer_class(self):
        if self.request.method == "POST":
            return ClientCreateSerializer  
        return CleintSerializer