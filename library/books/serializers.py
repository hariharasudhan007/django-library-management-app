from rest_framework import serializers

from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

        
    
    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.author = validated_data.get('author', instance.author)
    #     instance.published_date = validated_data.get('published_date', instance.published_date)
    #     instance.price = validated_data.get('price', instance.price)
    #     instance.stock = validated_data.get('stock', instance.stock)
    #     instance.save()
    #     return instance