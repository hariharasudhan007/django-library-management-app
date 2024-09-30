from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q
from django.core.exceptions import ValidationError


from .models import Book 
from .serializers import BookSerializer
from .paginations import StandardResultsSetPagination

def index(request):
    return HttpResponse("success")

class BookSingleView(APIView):
    def get(self,request,pk):
        try:
            one_book = Book.objects.get(pk=pk)
            print(one_book)
            serialized = BookSerializer(one_book)
            return Response(serialized.data, status=status.HTTP_200_OK)
            
        except  Book.DoesNotExist:
            return Response("No book with given id", status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        try:
            one_book = Book.objects.get(pk=pk)
        except  Book.DoesNotExist:
            return Response("No book with given id", status=status.HTTP_400_BAD_REQUEST)
        one_book.delete()
        return Response("deleted", status=status.HTTP_200_OK)
    
    def put(self,request, pk):
        try:
            one_book = Book.objects.get(pk=pk)
            serialized = BookSerializer(data=request.data)
            if serialized.is_valid():
                serialized.update(one_book,validated_data=serialized.data)
                return Response(serialized.data,status=status.HTTP_201_CREATED)
            return Response({"msg":"invalid","errors":serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
        except  Book.DoesNotExist:
            return Response("No book with given id", status=status.HTTP_400_BAD_REQUEST)



class BookView(APIView):
    # serializer_classes = BookSerializer
    # pagination_class = StandardResultsSetPagination

    def get(self,request):
        # all_books = [{"title":one_book.title,"author":one_book.author} for one_book in Book.objects.all()]
        books = Book.objects.all()
        books1 = Book.objects.filter(Q(title__icontains='vicics')| Q(author="my") )  #| Q(author="visicissoft")
        print(books1)
        pagesize = request.query_params.get("count")

        paginator = StandardResultsSetPagination()
        if pagesize:
            paginator.page_size=pagesize
        
        if (request.query_params.get("author")):
            books = books.filter(
                author__icontains = request.query_params.get("author")
                )
            print(books)

        if (request.query_params.get("title")):
            books =  books.filter(
                title__icontains = request.query_params.get("title")
                                   )
            print(books)

        if (request.query_params.get("pub_from")):
            print(request.query_params.get("pub_from"))
            books = books.filter(
                published_date__gte=datetime.strptime(
                    request.query_params.get("pub_from"),"%Y-%m-%d"
                )
            )
            
        if (request.query_params.get("pub_upto")):
            print(request.query_params.get("pub_upto"))
            books = books.filter(
                published_date__lte=datetime.strptime(
                    request.query_params.get("pub_upto"),"%Y-%m-%d"
                )
            )

        if (request.query_params.get("price_from")):
            print(request.query_params.get("price_from"))
            books = books.filter(
                price__gte=request.query_params.get("price_from")
            )
            
        if (request.query_params.get("price_upto")):
            print(request.query_params.get("price_upto"))
            books = books.filter(
                price__lte=request.query_params.get("price_upto")
            )
            
        # books = books1.distinct()
        # print((title_books + author_books))
        # page = paginator.paginate_queryset(books)
        # serialized = BookSerializer(page,many=True)
        # pagination_class = StandardResultsSetPagination


        #  def get(self, request, format=None):
        # books = Book.objects.all()
        # paginator = CustomPageNumberPagination()
        paginated_books = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(paginated_books, many=True)
        return paginator.get_paginated_response(serializer.data)
    
        # return Response(serialized.data)
    
    def post(self, request):
        print("post")

        try:
            serialized = BookSerializer(data=request.data)
            if serialized.is_valid():
                try:
                    serialized.save()  # This will call the custom validation
                except ValidationError as e:
                    print(e.message_dict) 
                return Response(serialized.data,status=status.HTTP_201_CREATED)
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error---",e)
            return Response({"errors":str(e)},status=status.HTTP_400_BAD_REQUEST)

    
         
    


class lister(ListAPIView):
        queryset = Book.objects.all()
        serializer_class = BookSerializer

