from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import MemoryEntry
from .serializers import MemoryEntrySerializer


class MemoryListView(ListAPIView):
    serializer_class = MemoryEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = MemoryEntry.objects.filter(user=self.request.user)
        if mt := self.request.query_params.get('memory_type'):
            qs = qs.filter(memory_type=mt)
        return qs


class MemoryDeleteView(DestroyAPIView):
    serializer_class = MemoryEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MemoryEntry.objects.filter(user=self.request.user)
