from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .filters import *
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination


#making custom page number pagination
class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 8



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

# Create your views here.

@api_view(['GET','POST'])
def book_list(request):
    if request.method == "GET":
        filterset_backends = [DjangoFilterBackend]
        filterset_class = BookFilter
        # user = request.user
        # author = Author.objects.get(user = user)
        book = Book.objects.all()
        filterset = filterset_class(request.GET, queryset=book)
        if filterset.is_valid():
            book = filterset.qs

        #applying pagination
        pagination = CustomPagination()
        page = pagination.paginate_queryset(book, request)
        serializer = BookSerializer(page, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Success"}, status = status.HTTP_200_OK)
        else:
            return Response({"error":"Failed"}, status = status.HTTP_404_NOT_FOUND)
        

@api_view(['GET', 'PUT', 'PATCH','DELETE'])
def book_details(request, id):
    if request.method == "GET":
        book = get_object_or_404(Book, id = id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        book = get_object_or_404(Book, id = id)
        serializer = BookSerializer(book, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Success"}, status = status.HTTP_200_OK)
        else:
            return Response({"error":"Failed"}, status = status.HTTP_404_NOT_FOUND)
        
    elif request.method == "PATCH":
        book = get_object_or_404(Book, id = id)
        serializer = BookSerializer(book, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Success"}, status = status.HTTP_200_OK)
        else:
            return Response({"error":"Failed"}, status = status.HTTP_404_NOT_FOUND)
        

    elif request.method == "DELETE":
        book = get_object_or_404(Book, id = id)
        book.delete()
        return Response({"msg":"Deleted"}, status = status.HTTP_404_NOT_FOUND)
    

#author register

@api_view(['POST'])
def author_register_view(request):
    if request.method == "POST":
        serializer = AuthorRegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Register Successful"}, status = status.HTTP_200_OK)
        else:
            return Response({"error":"Failed to register"}, status = status.HTTP_404_NOT_FOUND)
        

@api_view(['GET'])
def author_list_view(request):
    if request.method == "GET":
        authors = Author.objects.all()
        serializer = AuthorListSerializer(authors, many=True)
        return Response(serializer.data)
    

@api_view(['POST'])
def author_login_view(request):
    if request.method == "POST":
        serializer = AuthorLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username = username, password=password)
            if user:
                tokens = get_tokens_for_user(user)
                return Response(tokens, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def author_profile(request):
    if request.method == "GET":
        serializer = AuthorProfileSerializer(request.user)
        return Response(serializer.data, status = status.HTTP_200_OK)
    


#author password reset serializers
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def author_password_reset_view(request):
    if request.method == "POST":
        serializer = AuthorPasswordResetSerializer(data = request.data, context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        return Response({"msg":"Password Change Successful"}, status = status.HTTP_200_OK)