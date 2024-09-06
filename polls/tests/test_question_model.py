import datetime
from django.utils import timezone
from polls.models import Question
from django.test import TestCase
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_question_with_default(self):
        """Test that a question with the default pub_date
        is considered published.
        """
        question = Question(question_text="Question_with_default_time")
        self.assertIs(question.is_published(), True)

    def test_question_pub_date_in_past(self):
        """Test that a question with a pub_date in the past
        is considered published.
        """
        past_time = timezone.now() - timezone.timedelta(days=30)
        past_question = Question(question_text="Past question", pub_date=past_time)
        self.assertIs(past_question.is_published(), True)

    def test_question_future_date(self):
        """Test that a question with a future pub_date is not considered published."""
        future_time = timezone.now() + timezone.timedelta(days=1)
        future_question = Question(question_text="Future question", pub_date=future_time)
        self.assertIs(future_question.is_published(), False)

    def test_cannot_vote_after_end_date(self):
        """Cannot vote if the end_date is in the past"""
        end_date = timezone.now() - timezone.timedelta(days=1)
        end_question = Question(question_text="Ended question", end_date=end_date)
        self.assertIs(end_question.can_vote(), False)

    def test_can_vote_with_end_date_is_null(self):
        """Test that voting is allowed if the end_date is None."""
        ended_none_question = Question(question_text="test_if_ended_is_null", end_date=None)
        self.assertIs(ended_none_question.can_vote(), True)

    def test_with_future_pub_date_and_future_end_date(self):
        """Test that a question with future pub_date and end_date does not allow voting."""
        future_pub_time = timezone.now() + timezone.timedelta(days=5)
        future_end_time = timezone.now() + timezone.timedelta(days=6)
        future_question = Question(question_text="future question", pub_date=future_pub_time, end_date=future_end_time)
        self.assertIs(future_question.can_vote(), False)

    def test_with_past_pub_date_and_past_end_date(self):
        """Test that a question with past pub_date and end_date does not allow voting."""
        past_pub_time = timezone.now() + timezone.timedelta(days=-5)
        past_end_time = timezone.now() + timezone.timedelta(days=-4)
        past_question = Question(question_text="Past question", pub_date=past_pub_time, end_date=past_end_time)
        self.assertIs(past_question.can_vote(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

