from django.db import models
import datetime
from django.utils import timezone


class Question(models.Model):
    """Class of the questions"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True, default=timezone.localtime())

    def was_published_recently(self):
        """Check if the poll is recently published or not."""
        now = timezone.localtime()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check if the poll is published or not."""
        now = timezone.localtime()
        return now >= self.pub_date

    def can_vote(self):
        """Check if the poll can be voted or not."""
        now = timezone.localtime()
        if self.end_date == None:
            return self.is_published()
        return self.pub_date >= now >= self.end_date

    def __str__(self):
        """String method"""
        return self.question_text


class Choice(models.Model):
    """Class of choices"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """String method"""
        return self.choice_text