# api/admin.py
from django.contrib import admin
from .models import (
    Demographic,
    Expertise,
    Code,
    Evaluation,
    Score,
    Time,
    QuestionBank,
    QuestionsBankLevel,
    Question,
    Language,
)  # Import all your models

# Create a list of models
models_to_register = [
    Demographic,
    Expertise,
    Code,
    Evaluation,
    Score,
    Time,
    QuestionBank,
    QuestionsBankLevel,
    Question,
    Language,
]  # Import all your models

# Register all models in the admin
for model in models_to_register:
    admin.site.register(model)
