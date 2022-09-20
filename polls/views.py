from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Choice, Question, Vote
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
import logging


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


log = logging.getLogger("polls")
date = datetime.now()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def update_choice_login(request, **kwargs):
    """Update the latest vote when logged in."""
    for question in Question.objects.all():
        try:
            question.previous_vote = str(request.user.vote_set.get(question=question).selected_choice)
            question.save()
        except(Vote.DoesNotExist):
            pass


@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    """Log when user logs in."""
    ip = get_client_ip(request)
    log.info('Login user: %s , IP: %s , Date: %s', user, ip, str(date))


@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    """Log when user logs out."""
    ip = get_client_ip(request)
    log.info('Logout user: %s , IP: %s , Date: %s', user, ip, str(date))


@receiver(user_login_failed)
def log_user_login_failed(sender, request, credentials, **kwargs):
    """Log when user fails to login."""
    ip = get_client_ip(request)
    log.warning('Login user(failed): %s , IP: %s , Date: %s', credentials['username'], ip, str(date))


@login_required()
def vote(request, question_id):
    """Vote the selected poll."""
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        return HttpResponseRedirect(reverse('polls:index'))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'polls/detail.html',
            {'question': question, 'error_message': "You didn't select a choice.", })
    else:
        Vote.objects.update_or_create(user=user, question=question, defaults={'selected_choice': selected_choice})
        for choice in question.choice_set.all():
            choice.votes = Vote.objects.filter(question=question).filter(selected_choice=choice).count()
            choice.save()
        for question in Question.objects.all():
            question.previous_vote = str(request.user.vote_set.get(question=question).selected_choice)
            question.save()
        date = datetime.now()
        log = logging.getLogger("polls")
        log.info("User: %s, Poll's ID: %d, Date: %s.", user, question_id, str(date))
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
