from rest_framework import serializers
from .models import *


class DemographicSerializer(serializers.ModelSerializer):
  class Meta:
    model = Demographic
    fields = '__all__'

class ExpertiseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Expertise
    fields = '__all__'

    