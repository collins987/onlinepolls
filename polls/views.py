from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
    queryset = Poll.objects.all()

    def get_serializer_class(self):
        # Use PollCreateSerializer for POST (create), PollSerializer otherwise
        if self.action in ["create", "update", "partial_update"]:
            return PollCreateSerializer
        return PollSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # results endpoint → /polls/<id>/results/
    @action(detail=True, methods=["get"], url_path="results")
    def results(self, request, pk=None):
        poll = self.get_object()
        choices = poll.choices.annotate(votes=Count("votes")).values(
            "id", "text", "votes"
        )
        return Response(
            {
                "id": poll.id,
                "question": poll.question,
                "results": list(choices),
            }
        )


# -------------------------------
# Vote API (dedicated endpoint)
# -------------------------------
class VoteCreateAPIView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            return Response(
                {"error": "You have already voted on this poll"},
                status=status.HTTP_400_BAD_REQUEST,
            )


