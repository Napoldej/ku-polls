import datetime
from django.db import models
from django.utils import timezone

# Create your models here.


class Question(models.Model):
    """
    Represents a poll question.

    Attributes:
        question_text (str): The text of the question being asked.
        pub_date (datetime): The date and time when the question was published.
        end_date (datetime): The date and time when the question
            will end (optional).
    """
    question_text = models.CharField(max_length=250)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date ended', null=True)
    
    def is_published(self):
        """
        Checks if the question has been published.

        Returns:
            bool: True if the current date and time is after the 
                  publication date.
        """
        now = timezone.now()
        return self.pub_date <= now
    
    def can_vote(self):
        """
        Determines if the question is currently open for voting.

        Returns:
            bool: True if the current date and time is within the
                  publication and end dates, or if there is no end date.
        """
        now = timezone.now()
        if self.end_date is not None:
            return self.pub_date <= now <= self.end_date
        return self.pub_date <= now
    
    def was_published_recently(self):
        """
        Determines if the question was published within the last day.

        Returns:
            bool: True if the question's publication date is within 
                  the last day, False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def __str__(self):
        """
        Returns a string representation of the Question instance.

        Returns:
            str: A formatted string showing the question's ID, text,
                 and publication date.
        """
        return (f"Question ID: {self.id}, Question: {self.question_text}, "
                f"Published on: {self.pub_date}")


class Choice(models.Model):
    """
    Represents a choice for a poll question.

    Attributes:
        question (Question): The question to which this choice belongs.
        choice_text (str): The text of the choice.
        vote (int): The number of votes this choice has received.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=250)
    vote = models.IntegerField(default=0)
    
    def __str__(self):
        """
        Returns a string representation of the Choice instance.

        Returns:
            str: The text of the choice.
        """
        return self.choice_text
