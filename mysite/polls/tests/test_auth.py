import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question


def create_question(question_text, days, ending):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    duration = timezone.now() + datetime.timedelta(days=ending)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=duration)


class AuthenticationTest(TestCase):
    """Class for testing the user authentication."""
    def setUp(self):
        """Setting up for testing the authentication."""
        User = get_user_model()
        user = User.objects.create_user("Pazcal", email="sahanon.p@ku.th", password="782543")
        user.first_name = "Sahanon"
        user.last_name = "Phisetpakasit"
        user.save()

    def test_login(self):
        """Test the user login."""
        self.client.login(username="Pazcal", password="782543")
        url = reverse("polls:index")
        respone = self.client.get(url)
        self.assertEqual(respone.status_code, 200)
        self.assertContains(respone, "Sahanon")

    def test_logout(self):
        """Test the user logout."""
        self.client.login(username="Pazcal", password="782543")
        self.client.logout()
        url = reverse("polls:index")
        respone = self.client.get(url)
        self.assertNotContains(respone, "Sahanon")

    def test_authenticate_vote(self):
        """Test the user vote."""
        self.client.login(username="Pazcal", password="782543")
        question = create_question(question_text='This is a question', days=-5)
        response = self.client.get(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(response.status_code, 200)
