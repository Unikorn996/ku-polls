from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import Choice, Question


class IndexView(generic.ListView):
    """View of the index page"""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return all questions sorted by published date."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """View of the detail page"""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Return all questions sorted by published date."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def page_redirection(self, request, **kwargs):
        """Redirect the not-allowed page to the index page."""
        try:
            question = Question.objects.get(pk=kwargs['pk'])
            if not question.can_vote():
                return HttpResponseRedirect(reverse('polls:index'), messages.error(request, "This poll is already closed. Can't vote!!!"))
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('polls:index'), messages.error(request, "This poll is not exist."))


class ResultsView(generic.DetailView):
    """View of the result page"""
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Vote the selected poll."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.", })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
