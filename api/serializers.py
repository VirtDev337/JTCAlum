from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile, Opportunity # GitAccount
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many = False)
    tags = TagSerializer(many = True)
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
    
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many = True)
        return serializer.data


class AffiliateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class SocialAccountExtraDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ["extra_data"]
        depth = 1
