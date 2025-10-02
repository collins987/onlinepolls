from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, PollCreateSerializer, VoteSerializer
from django.shortcuts import render

def landing(request):
    return render(request, 'landing.html')

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().select_related('created_by').prefetch_related('choices')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return PollCreateSerializer
        return PollSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        active = self.request.query_params.get('active')
        if active is not None:
            if active.lower() in ['1','true','yes']:
                qs = qs.filter(is_active=True)
            elif active.lower() in ['0','false','no']:
                qs = qs.filter(is_active=False)
        return qs

    @action(detail=True, methods=['get'], url_path='results')
    def results(self, request, pk=None):
        """
        Custom endpoint: GET /api/polls/{id}/results/
        """
        poll = self.get_object()
        choices = Choice.objects.filter(poll=poll).annotate(vote_count=Count('votes'))
        results = [
            {"id": c.id, "choice": c.text, "votes": c.vote_count}
            for c in choices
        ]
        return Response(
            {"poll": poll.title, "results": results},
            status=status.HTTP_200_OK
        )

class VoteCreateAPIView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError('You have already voted on this poll.')
