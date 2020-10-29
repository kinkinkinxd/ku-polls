"""Model for KU-polls."""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Model class for Question."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('ending date')

    def __str__(self):
        """Show text for question."""
        return self.question_text

    def is_published(self):
        """Return True if the question is published, Otherwise return False."""
        return timezone.now() >= self.pub_date

    def can_vote(self):
        """Return True if the poll allowed user to vote, Otherwise return False."""
        return self.end_date >= timezone.now() >= self.pub_date

    def was_published_recently(self):
        """Check if the polls already published."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Model class for chioce."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        """Show text for choice."""
        return self.choice_text

    @property
    def votes(self):
        """Count vote."""
        return self.question.vote_set.filter(choice=self).count()


class Vote(models.Model):
    """Model class for Vote."""

    vote_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Show text for vote."""
        return self.vote_text
