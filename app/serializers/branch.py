
import re, json
from rest_framework import serializers
from ..models.branch import Branch

class BranchAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

class BrachNameSerializer(serializers.ModelSerializer):
    class Meta:
        model= Branch
        fields =("id","name")


class BranchCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ['name', 'address', 'status', 'year_of_construction', 'total_area', 'latitude','longitude']
