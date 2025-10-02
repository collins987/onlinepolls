from rest_framework import serializers
from django.utils import timezone
from .models import Poll, Choice, Vote

# 1. Choice Serializer
class ChoiceSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ('id', 'text', 'votes')

    def get_votes(self, obj):
        return obj.votes.count()  # reverse relation from Vote model

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

# 3. Poll Create Serializer (create poll + choices in one go)
class PollCreateSerializer(serializers.ModelSerializer):
    choices = serializers.ListField(
        child=serializers.CharField(max_length=255),
        write_only=True
    )
    # Show full poll response after creation
    created_by = serializers.ReadOnlyField(source='created_by.username')
    all_choices = ChoiceSerializer(many=True, source='choices', read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'description', 'expires_at', 'is_active', 'choices', 'created_by', 'all_choices')

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        poll = Poll.objects.create(**validated_data)
        choices_objs = [Choice(poll=poll, text=text) for text in choices_data]
        Choice.objects.bulk_create(choices_objs)
        return poll

    def to_representation(self, instance):
        """
        Override response so it looks identical to PollSerializer
        """
        return PollSerializer(instance, context=self.context).data

# 4. Vote Serializer
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

        if Vote.objects.filter(poll=poll, user=user).exists():
            raise serializers.ValidationError('You have already voted on this poll.')

        if poll.expires_at and poll.expires_at < timezone.now():
            raise serializers.ValidationError('Poll has expired.')

        choice = data.get('choice')
        if choice.poll_id != poll.id:
            raise serializers.ValidationError('Choice does not belong to the given poll.')

        return data
