"""Views for polls."""
import logging.config

from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Question, Choice, Vote
from .setting import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('polls')


def get_client_ip(request):
    """Return client ip address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """Log the username and ip address when user logged in."""
    logger.info(f'User {user.username} logged in from {get_client_ip(request)}')


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """Log the username and ip address when user logged out."""
    logger.info(f'User {user.username} logged out from {get_client_ip(request)}')


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    """Log the username and ip address when user login failed."""
    logger.warning(f'User {request.POST["username"]} login failed from {get_client_ip(request)}')


class IndexView(generic.ListView):
    """View for index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Get the query.

        Return the last five published questions (not including those set to
        be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    """View for detail page."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """View for results page."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Check vote and count vote."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't make a choice.")
        return render(request, 'polls/detail.html', {'question': question, })
    else:
        if not (question.can_vote()):
            messages.warning(request, "This polls are not allowed.")
        elif Vote.objects.filter(user=request.user, question=question).exists():
            previous_vote = Vote.objects.get(user=request.user, question=question)
            previous_vote.choice = selected_choice
            previous_vote.save()
        else:
            question.vote_set.create(choice=selected_choice, user=request.user)
            messages.success(request, "Your choice successfully recorded.")
        request.session['choice'] = selected_choice.id
        logger.info(f'User {request.user.username} voted on polls id: {question.id}')
        url = reverse('polls:results', args=(question.id,))
        return HttpResponseRedirect(url)
