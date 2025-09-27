from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Count
from django.db import IntegrityError
from .models import Poll, Choice, Vote
from .serializers import (
    PollSerializer,
    PollCreateSerializer,
    VoteSerializer,
)


# -------------------------------
# Poll ViewSet
# -------------------------------
class PollViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, creating, updating, and deleting polls.
    - Uses PollCreateSerializer for create
    - Uses PollSerializer for read
    - Provides extra 'results' action
    """
    queryset = Poll.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PollCreateSerializer
        return PollSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["get"], url_path="results")
    def results(self, request, pk=None):
        """
        Custom action to return results of a poll:
        - poll id
        - poll title
        - list of choices with vote counts
        """
        poll = self.get_object()
        choices = (
            poll.choices
            .annotate(votes=Count("votes"))
            .values("id", "text", "votes")
        )
        return Response({
            "id": poll.id,
            "title": poll.title,
            "results": list(choices),
        })


class VoteCreateAPIView(generics.CreateAPIView):
    """
    API endpoint for casting a vote.
    - Requires authentication
    - Validates duplicate votes and poll expiry
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            # In case DB-level uniqueness constraint is triggered
            return Response(
                {"detail": "You have already voted on this poll."},
                status=status.HTTP_400_BAD_REQUEST
            )