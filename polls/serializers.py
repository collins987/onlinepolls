from rest_framework import serializers
from django.utils import timezone
from .models import Poll, Choice, Vote


# 1. Choice Serializer
class ChoiceSerializer(serializers.ModelSerializer):
    votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Choice
        fields = ('id', 'text', 'votes')


# 2. Poll Serializer (for reads)
class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Poll
        fields = (
            'id',
            'title',
            'description',
            'created_by',
            'created_at',
            'expires_at',
            'is_active',
            'choices',
        )


# 3. Poll Create Serializer (for writes)
class PollCreateSerializer(serializers.ModelSerializer):
    choices = serializers.ListField(
        child=serializers.CharField(max_length=255),
        write_only=True
    )

    class Meta:
        model = Poll
        fields = ('title', 'description', 'expires_at', 'is_active', 'choices')

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        # ⚠️ removed created_by here, it's passed from the view
        poll = Poll.objects.create(**validated_data)
        choices_objs = [Choice(poll=poll, text=text) for text in choices_data]
        Choice.objects.bulk_create(choices_objs)
        return poll


# 4. Vote Serializer (with validation)
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'poll', 'choice')

    def validate(self, data):
        request = self.context['request']
        user = request.user
        poll = data.get('poll')

        if not poll:
            raise serializers.ValidationError('Poll is required.')

        # check user already voted
        if Vote.objects.filter(poll=poll, user=user).exists():
            raise serializers.ValidationError('You have already voted on this poll.')

        # check poll expired
        if poll.expires_at and poll.expires_at < timezone.now():
            raise serializers.ValidationError('Poll has expired.')

        # ensure the choice belongs to the poll
        choice = data.get('choice')
        if choice.poll_id != poll.id:
            raise serializers.ValidationError('Choice does not belong to the given poll.')

        return data

    def create(self, validated_data):
        vote = Vote.objects.create(**validated_data)
        return vote
