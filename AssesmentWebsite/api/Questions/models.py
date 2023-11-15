from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField

level_choices = (("1", "Beginner"), ("2", "Intermediate"), ("3", "Expert"))
language_choices = (("1", "Python"), ("2", "C++"), ("3", "Javascript"))


class QuestionBank(models.Model):
    qbid = models.AutoField(primary_key=True)
    # aid = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    admin_programming_language = models.CharField(
        choices=language_choices, max_length=100
    )
    # level = models.CharField(choices=level_choices, max_length=100)


class QuestionsBankLevel(models.Model):
    qblid = models.AutoField(primary_key=True)
    fqbid = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, null=True)
    qlevel = models.CharField(choices=level_choices, max_length=100)


class Code(models.Model):
    cid = models.AutoField(primary_key=True)
    fqblid = models.ForeignKey(QuestionsBankLevel, on_delete=models.CASCADE, null=True)
    code_image = models.ImageField()
    code_text = models.CharField(max_length=500, null=True)
    code_time = models.FloatField(null=True)
    # code_read_time = models.IntegerField(null=True)
    question_time = models.FloatField(null=True)

    # question_read_time = models.IntegerField(null=True)
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Question(models.Model):
    qid = models.AutoField(primary_key=True)
    fcid = models.ForeignKey(Code, on_delete=models.CASCADE, null=True)
    question_text = models.CharField(max_length=500, null=True)
    option1 = models.CharField(max_length=500, null=True)
    option2 = models.CharField(max_length=500, null=True)
    option3 = models.CharField(max_length=500, null=True)
    option4 = models.CharField(max_length=500, null=True)
    correct_option = models.CharField(max_length=500, null=True)
    marks = models.FloatField(null=True)
    question_time = models.IntegerField(null=True)
