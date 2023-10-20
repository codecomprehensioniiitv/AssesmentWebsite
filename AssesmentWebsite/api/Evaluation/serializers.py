from rest_framework import serializers
from .models import *


class EvaluationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Evaluation
    fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Score
    fields = "__all__"
    
class TimeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Time
    fields = "__all__"

