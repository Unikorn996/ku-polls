from unittest import TestCase
from polls.models import Question
from django.utils import timezone
import datetime


def create_question(question_text, days, ending):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    duration = timezone.now() + datetime.timedelta(days=ending)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=duration)

    
class TestPublishedAndCanVote(TestCase):
    """Class for testing is_published and can_vote."""
    def test_is_published(self):
        """Check normal is_published."""
        time = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=time)
        self.assertTrue(question.is_published())

    def test_can_vote(self):
        """Check normal can_vote."""
        pub_time = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=pub_time)
        self.assertTrue(question.can_vote())

    def test_future_question(self):
        """Check if the future question is published."""
        future_question = create_question(question_text='Future question.', days=5, ending=10)
        self.assertFalse(future_question.is_published())

    def test_can_vote_after_question(self):
        """Check if the question can vote after the end date."""
        pub_time = timezone.now() - datetime.timedelta(days=2)
        end_time = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertFalse(question.can_vote())

    def test_can_vote_before_question(self):
        """Check if the question can vote before the published date."""
        pub_time = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=pub_time)
        self.assertFalse(question.can_vote())
