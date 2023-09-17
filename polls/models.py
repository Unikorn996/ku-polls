from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


class Question(models.Model):
    """
    A question for a poll
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now())
    end_date = models.DateTimeField('date ended', blank=True, null=True)
    
    def was_published_recently(self):
        """
        Return True if the question was published recently.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def is_published(self):
        """
        Return True if the question is in publication time.
        """
        now = timezone.now()
        return self.pub_date <= now
    
    def can_vote(self):
        """
        Check if the poll can be voted or not.
        """
        now = timezone.now()
        if self.end_date is None:
            return self.is_published()
        return self.pub_date <= now <= self.end_date

    def __str__(self):
        """
        Return a string.
        """
        return self.question_text


class Choice(models.Model):
    """
    Choices for polls
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # def votes(self):
    #     """
    #     Count the votes
    #     """
    #     return self.vote_set.count()

    def __str__(self):
        """
        Return a string
        """
        return self.choice_text
    

class Vote(models.Model):
    """
    Votes for polls
    """
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()

    def vote(self):
        """
        One vote for one authenticated user
        """
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    
    def __str__(self):
        """
        Return a string
        """
        return f'Vote for {self.choice_text} from {self.question_text}'
