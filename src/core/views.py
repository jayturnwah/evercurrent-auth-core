from django.http import JsonResponse
from django.views import View

from rest_framework import viewsets, permissions, pagination, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resource
from .serializers import ResourceSerializer
from .permissions import HasRole, IsOwnerOrAdmin


class HealthView(View):
    """
    Plain Django view, no DRF, no auth, always returns 200.
    """
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "ok"})


class DefaultPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ResourceViewSet(viewsets.ModelViewSet):
    """
    A generic, role-gated, owner-aware CRUD.
    """
    queryset = Resource.objects.select_related("owner").all()
    serializer_class = ResourceSerializer
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["created_at", "title"]

    required_roles = ["creator", "admin"]

    def get_permissions(self):
        if self.action in ["list", "create"]:
            return [permissions.IsAuthenticated(), HasRole()]
        else:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Resource.objects.none()
        if user.roles.filter(name="admin").exists():
            return self.queryset
        return self.queryset.filter(owner=user)
