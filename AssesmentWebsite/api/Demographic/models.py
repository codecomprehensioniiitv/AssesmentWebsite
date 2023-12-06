from django.db import models

gender_choices = (("1", "Female"), ("2", "Male"), ("3", "NaN"))

profession_choices = (("1", "Student"), ("2", "Industrialist"), ("3", "Professor"))

language_choices = (("1", "Python"), ("2", "C++"), ("3", "Javascript"))

level_choices = (("1", "Beginner"), ("2", "Intermediate"), ("3", "Expert"))
duration_choices = (("1", "<1 year"), ("2", "1-3 years"), ("3", ">3 years"))


# Demographic : User profile
class Demographic(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    dob = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(choices=gender_choices, max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    profession = models.CharField(choices=profession_choices, max_length=100)

    def __str__(self):
        return f"{self.uid}"


# Expertise model for getting the programming language.
class Expertise(models.Model):
    eid = models.AutoField(primary_key=True)
    fuid = models.ForeignKey(
        Demographic, related_name="demographic_id", on_delete=models.CASCADE, null=True
    )
    selectedLanguage = models.CharField(choices=language_choices, max_length=100)
    level = models.CharField(choices=level_choices, max_length=100)
    duration = models.CharField(choices=duration_choices, max_length=100)
    time = models.IntegerField()


class Language(models.Model):
    lid = models.AutoField(primary_key=True)
    fuid = models.ForeignKey(
        Demographic, related_name="expertise_id", null=True, on_delete=models.PROTECT
    )
    selectedLanguage = models.CharField(choices=language_choices, max_length=100)
    level = models.CharField(choices=level_choices, max_length=100)
    duration = models.CharField(choices=duration_choices, max_length=100)
    time = models.IntegerField()
