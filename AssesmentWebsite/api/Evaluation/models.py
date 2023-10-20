from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField

from  ..Demographic.models import Demographic
from  ..Questions.models import QuestionBank, Question, Code


decision_choices =(
    ("1", "Correct"),
    ("2", "Incorrect")
)


class Evaluation(models.Model):
    evid = models.AutoField(primary_key=True)
    ffuid = models.ForeignKey(Demographic, on_delete=models.CASCADE, null= True)
    ffqbid = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, null= True)
 


class Score(models.Model):
    sid = models.AutoField(primary_key=True)
    fevid = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null= True)
    fqid = models.ForeignKey(Question, on_delete=models.CASCADE, null= True)
    selected_answer = models.CharField(max_length=500, null=True)
    decision = models.CharField(choices=decision_choices, max_length=100, null=True)
    marks = models.FloatField(null=True)



class Time(models.Model):
    tid = models.AutoField(primary_key=True)
    ffevid = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null= True)
    fcfid = models.ForeignKey(Code, on_delete=models.CASCADE, null= True)
    question_read_time = models.FloatField(null=True)
    code_read_time = models.FloatField(null=True)