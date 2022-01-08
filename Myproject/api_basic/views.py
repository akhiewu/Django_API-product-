from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.

@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        Serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(Serializer.data, safe=False)
    
    elif request.method =='POST':
        data = JSONParser().parse(request)
        Serializer= ArticleSerializer(data=data)
        
        if Serializer.is_valid():
            Serializer.save()
            return JsonResponse(Serializer.data, status=201)
        return JsonResponse(Serializer.error, status=400)
    
    
    
    
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist: 
        return HttpResponse(status=404)
    
    if request.method =='GET':
        Serializer= ArticleSerializer(article)
        return JsonResponse(Serializer.data)
    
    
    elif request.method =='PUT':
        data = JSONParser().parser(request)
        serializer = ArticleSerializer(article, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status= 400)
    
    
    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status = 204)
           


#Funtion Base Api Views
# @api_view(['GET', 'POST'])
# def article_list(request):
#     if request.method =='GET':
#         article = Article.objects.all()
#         serializer = ArticleSerializer(article, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = ArticleSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
# @api_view(['GET', 'POST', 'DELETE'])
# def article_list(request, pk):
#     try:
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist: 
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method =='GET':
#         serializer= ArticleSerializer(article)
#         return Response(serializer.data)
    
    
#     elif request.method =='PUT':
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
#     elif request.method == 'DELETE':
#         article.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)
    
    
    
    
    
    #class Base Api View
    
    
    
class ArticleAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ArticleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class ArticleDetails(APIView):
    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse(status = status.HTTP_404_NOT_FOUND)
        
    def get(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data) 
    
    def put(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data = request.data)       
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response (status = status.HTTP_204_NO_CONTENT)
    
    
    
    
    
    
    
    
    