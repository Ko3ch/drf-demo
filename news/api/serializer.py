from pydoc import importfile
from pytz import timezone
from rest_framework import serializers
from news.models import Article,Journalist
from rest_framework.serializers import ModelSerializer
from datetime import datetime,timezone
from django.utils.timesince import timesince



class ArticleSerializer(ModelSerializer):
    time_since_published = serializers.SerializerMethodField()
    # author = serializers.StringRelatedField()
    # author = JournalistSerializer()
    class Meta:
        model = Article
        fields = "__all__"
        # fields = ["title","description","published_time"]
        # exclude = ["title"]
        read_only_fields = ["id","created_time","updated_time"]

    def get_time_since_published(self,object):
        now = datetime.now(timezone.utc)
        published_date = object.published_time
        time_delta = timesince(published_date,now)
        return time_delta


    def validate_published_time(self,datevalue):
        today = datetime.now(timezone.utc)
        if datevalue > today:
            raise serializers.ValidationError('This is a date that has not come yet')
        return datevalue   

class JournalistSerializer(ModelSerializer):
    # articles = ArticleSerializer(read_only=True,many=True)

    articles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='article-detail'
    )
    class Meta:
        model = Journalist
        fields = "__all__"

class ArticleSerializerDefault(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    main_text = serializers.CharField()
    published_time = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    created_time = serializers.DateTimeField(read_only=True)
    updated_time = serializers.DateTimeField(read_only=True) 

    def create(self,validated_data):
        return Article.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.author = validated_data.get('author',instance.author)
        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.main_text = validated_data.get('main_text',instance.main_text)
        instance.published_time = validated_data.get('published_time',instance.published_time)
        instance.is_active = validated_data.get('is_active',instance.is_active)
        instance.save()
        return instance

    def validate(self,data):
        if data['title'] == data['description']:
            raise serializers.ValidationError("Title and description cannnot be same")
        return data 

    def validate_title(self,value):
        if len(value) <8:
            raise serializers.ValidationError(f"title must be minimum 8 characters, you entered {len(value)} characters")
        return value