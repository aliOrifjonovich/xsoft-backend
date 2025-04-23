from rest_framework import viewsets

from ..serializers.branch import BrachNameSerializer,BranchAllSerializer,BranchCreateSerializer
from ..models.branch import Branch
from ..pagination .paginations import DefaultLimitOffSetPagination
from rest_framework.permissions import IsAuthenticated

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.filter().order_by("-updated_at")
    serializer_class = BranchAllSerializer
    pagination_class = DefaultLimitOffSetPagination
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action=='update':
            return BranchCreateSerializer
        return BranchAllSerializer
