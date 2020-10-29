"""Polls date unit test for ku-polls."""

import datetime
from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):
    """Test for model."""

    def test_was_published_recently_with_old_question(self):
        """Test was published recently with old question.

        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Test was published recently with recent question.

        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_future_question(self):
        """Test was published recently with future question.

        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_is_published_with_past_question(self):
        """is_published returns True for questions whose pub_date is in the past."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """is_published returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_can_vote_with_past_question(self):
        """can_vote returns False for question whose pub_date is in the past."""
        pub_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end_time = timezone.now() - datetime.timedelta(hours=22)
        older_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(older_question.can_vote(), False)

    def test_can_vote_with_recent_question(self):
        """can_vote returns True for questions that have not been closed."""
        pub_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end_time = timezone.now() + datetime.timedelta(days=1)
        recent_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(recent_question.can_vote(), True)

    def test_can_vote_with_future_question(self):
        """can_vote returns False for question whose pub_date is in the future."""
        pub_time = timezone.now() + datetime.timedelta(days=30)
        end_time = timezone.now() + datetime.timedelta(days=31)
        future_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(future_question.can_vote(), False)
