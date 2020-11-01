"""Unit test for ku-polls."""

import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from polls.models import Question


def create_question(question_text, days):
    """Create a question.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    end_time = time + datetime.timedelta(days=30)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=end_time)


class VotingTest(TestCase):
    """Test fot voting."""

    def setUp(self):
        """Set up for authenticated."""
        self.question = create_question("test", -5)
        self.question.choice_set.create(choice_text='test1')
        self.question.choice_set.create(choice_text='test2')
        self.user = {
            'username': 'test',
            'password': 'password'
        }
        User.objects.create_user(**self.user)
        self.client.post(reverse('login'), self.user)

    def test_authenticated_voting(self):
        """Test voting when the user is authenticated."""
        response = self.client.get(reverse('polls:index'))
        self.assertIs(response.context['user'].is_authenticated, True)
        self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': 1})
        self.assertIs(self.question.vote_set.filter(question=self.question).exists(), True)

    def test_not_authenticated_voting(self):
        """Test voting when user is not authenticated."""
        self.client.post(reverse('logout'))
        response = self.client.get(reverse('polls:index'))
        self.assertIs(response.context['user'].is_authenticated, False)
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': 1})
        self.assertEqual(response.status_code, 302)
