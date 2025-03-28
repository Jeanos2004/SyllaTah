from rest_framework import serializers
from .models import Transport, TransportCategory, TransportReview

class TransportCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportCategory
        fields = '__all__'

class TransportReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = TransportReview
        fields = ['id', 'transport', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']

class TransportSerializer(serializers.ModelSerializer):
    category = TransportCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=TransportCategory.objects.all(),
        write_only=True,
        source='category'
    )
    reviews = TransportReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Transport
        fields = '__all__'
        read_only_fields = ['rating', 'total_reviews', 'created_at', 'updated_at']