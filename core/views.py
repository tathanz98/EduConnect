from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, StudyGroup, AcademicEvent
from .serializers import PostSerializer, StudyGroupSerializer, AcademicEventSerializer

class IsTeacherOrResearcherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ['TEACHER', 'RESEARCHER', 'ADMIN']

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['put'])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return Response({'status': 'like actualizado', 'likes_count': post.likes.count()})

class StudyGroupViewSet(viewsets.ModelViewSet):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrResearcherOrAdmin]

    def perform_create(self, serializer):
        group = serializer.save(creator=self.request.user)
        group.members.add(self.request.user)

    @action(detail=True, methods=['put'])
    def membership(self, request, pk=None):
        group = self.get_object()
        if request.user in group.members.all():
            group.members.remove(request.user)
        else:
            group.members.add(request.user)
        return Response({'status': 'membresía actualizada'})

class AcademicEventViewSet(viewsets.ModelViewSet):
    queryset = AcademicEvent.objects.all()
    serializer_class = AcademicEventSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrResearcherOrAdmin]

    def perform_create(self, serializer):
        event = serializer.save(organizer=self.request.user)
        event.attendees.add(self.request.user)

    @action(detail=True, methods=['put'])
    def register(self, request, pk=None):
        event = self.get_object()
        if request.user in event.attendees.all():
            event.attendees.remove(request.user)
        else:
            event.attendees.add(request.user)
        return Response({'status': 'inscripción actualizada'})