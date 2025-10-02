from django.db import models
from django.conf import settings

class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='polls')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.title

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)

    class Meta:
        indexes = [models.Index(fields=['poll'])]

    def __str__(self):
        return f"{self.text} ({self.poll_id})"

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'user')
        indexes = [models.Index(fields=['poll', 'user'])]

    def __str__(self):
        return f"{self.user_id} -> {self.choice_id} (poll {self.poll_id})"
