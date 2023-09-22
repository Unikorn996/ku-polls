from typing import Any
from django import http
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Question, Choice, Vote


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    def dispatch(self, request, *args: Any, **kwargs: Any):
        """
        Return to index page if the poll's not in the publication time.
        """
        user = request.user
        question_text = Question.objects.get(id=kwargs["pk"])

        # Initialize voted_choice with None (default value)
        voted_choice = None

        if not question_text.can_vote():
            messages.warning(request, f'''The question "{question_text}" is not in the publication time.''')
            return redirect('polls:index')
        if user.is_authenticated:
            try:
                voted_choice = question_text.choice_set.get(vote__user=user)
            except (Vote.DoesNotExist, TypeError):
                pass
        if voted_choice is not None:
            # User has already voted
            return render(request, self.template_name, {"question": question_text, "voted": voted_choice})
        else:
            # User is eligible to vote
            return super().dispatch(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def dispatch(self, request, *args: Any, **kwargs: Any):
        """
        Return to index page if the poll's not in the publication time.
        """
        question_text = Question.objects.get(id=kwargs["pk"])
        if not self.get_object().can_vote():
            messages.warning(request, f'''The question "{question_text}" is not in the publication time.''')
            return redirect('polls:index')
        # messages.success(request, "Your vote has been recorded.")
        return super().dispatch(request, *args, **kwargs)


@login_required
def vote(request, question_id):
    """
    User's vote for a choice in a poll.
    """
    question = get_object_or_404(Question, pk=question_id)
    this_user = request.user
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    try:
        # find a vote for this user and this question
        vote = Vote.objects.get(user=this_user, choice__question=question)
        # update the vote after a user has changed their vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        # no matching vote - create a new vote object
        vote = Vote.objects.create(user=this_user, choice=selected_choice)
    vote.save()
    messages.success(request, f"Your vote has been recorded successfully.")

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
