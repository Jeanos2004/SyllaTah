from rest_framework import serializers
from .models import Activity, ActivityCategory, ActivityReview

class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = '__all__'

class ActivityReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = ActivityReview
        fields = ['id', 'activity', 'user', 'rating', 'comment', 'created_at', 'photos']
        read_only_fields = ['created_at']

class ActivitySerializer(serializers.ModelSerializer):
    category = ActivityCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ActivityCategory.objects.all(),
        write_only=True,
        source='category'
    )
    reviews = ActivityReviewSerializer(many=True, read_only=True)
    average_rating = serializers.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        source='rating',
        read_only=True
    )

    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['rating', 'total_reviews', 'created_at', 'updated_at']