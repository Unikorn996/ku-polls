from django.db import models
import datetime
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True, default=timezone.localtime())

    def was_published_recently(self):
        now = timezone.localtime()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_publsihed(self):
        now = timezone.localtime()
        return now >= self.pub_date

    def can_vote(self):
        now = timezone.localtime()
        if self.end_date == None:
            return self.is_published()
        return self.pub_date >= now >= self.end_date

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text