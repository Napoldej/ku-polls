import datetime
from django.db import models
from django.utils import timezone



# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=250)
    pub_date = models.DateTimeField('date published')
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def __str__(self):
        return (f"{str(self.id)}, Question:{self.question_text}, Pub_date:{self.pub_date}")
    
class Choice(models.Model):
    question_text = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=250)
    vote = models.IntegerField(default=0)
    
    def __str__(self):
        return (f"{self.choice_text}")
    
    
    
    