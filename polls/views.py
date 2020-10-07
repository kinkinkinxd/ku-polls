"""Views for polls."""

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Question, Choice


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
            return HttpResponseRedirect(reverse("polls:index"))
        selected_choice.votes += 1
        selected_choice.save()
        messages.success(request, "Your choice successfully recorded.")
        url = reverse('polls:results', args=(question.id, ))
        return HttpResponseRedirect(url)

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
