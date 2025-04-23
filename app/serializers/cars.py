from rest_framework import serializers

from app.serializers.branch import BrachNameSerializer
from ..models.cars import Car,CarImages,CarFeatures,CarCategory
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCategory
        fields = "__all__"

class CarImageSeriazlier(serializers.ModelSerializer):

    class Meta:
        model = CarImages
        fields = "__all__"
    
class CarImagesGetSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = CarImages
        fields = "__all__"
    def get_photo(self, obj):
        return obj.photo.url

class CarFarutesSerializer(serializers.ModelSerializer):
    class Meta:
        model=CarFeatures
        fields = "__all__"

class CarGetSerializer(serializers.ModelSerializer):
    images = CarImagesGetSerializer(many=True, required=False)
    features = CarFarutesSerializer(many=True, required=False)
    branch = BrachNameSerializer(required=False)
    category = CategorySerializer()
    # Custom method fields for choice fields
    rental_status = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    fuel_type = serializers.SerializerMethodField()
    engine_size = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = '__all__'
        extra_fields = ["images"]

    # Method to get the display value for rental_status
    def get_rental_status(self, obj):
        return obj.get_rental_status_display()

    # Method to get the display value for color
    def get_color(self, obj):
        return obj.get_color_display()

    # Method to get the display value for fuel_type
    def get_fuel_type(self, obj):
        return obj.get_fuel_type_display()

    # Method to get the display value for engine_size
    def get_engine_size(self, obj):
        return obj.get_engine_size_display()

class CarSerializer(serializers.ModelSerializer):
    images = serializers.FileField(required=False)
    class Meta:
        model = Car
        fields = '__all__'
        extra_fields = ["images"]
