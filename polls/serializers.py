from rest_framework import serializers
from django.utils import timezone
from .models import Poll, Choice, Vote


# 1. Choice Serializer
class ChoiceSerializer(serializers.ModelSerializer):
    votes = serializers.IntegerField(source="vote_set.count", read_only=True)

    class Meta:
        model = Choice
        fields = ["id", "text", "votes"]


# 2. Poll Serializer (for reads)
class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ["id", "question", "created_at", "expires_at", "choices"]


# 3. Poll Create Serializer (for writes)
class PollCreateSerializer(serializers.ModelSerializer):
    choices = serializers.ListField(
        child=serializers.CharField(max_length=200), write_only=True
    )

    class Meta:
        model = Poll
        fields = ["id", "question", "expires_at", "choices"]

    def create(self, validated_data):
        choices_data = validated_data.pop("choices")
        poll = Poll.objects.create(**validated_data)
        for choice_text in choices_data:
            Choice.objects.create(poll=poll, text=choice_text)
        return poll


# 4. Vote Serializer (with validation)
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "poll", "choice", "user"]

        # user will be set automatically, not passed from client
        extra_kwargs = {"user": {"read_only": True}}

    def validate(self, data):
        user = self.context["request"].user
        poll = data.get("poll")

        # prevent duplicate vote
        if Vote.objects.filter(poll=poll, user=user).exists():
            raise serializers.ValidationError("You have already voted on this poll")

        # prevent expired polls
        if poll.expires_at and poll.expires_at < timezone.now():
            raise serializers.ValidationError("Poll has expired")

        return data

    def create(self, validated_data):
        # attach current user automatically
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
