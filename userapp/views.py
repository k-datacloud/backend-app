from django.contrib.auth import login, authenticate, logout
from rest_framework import viewsets, generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .models import UserManager, CustomUser, Post, Follow
from .forms import loginForm
from django.http import JsonResponse, request
from django.views import View
import json
from django.db.models import Q



from.serializers import UserSerializer, UserEditSerializer, PostSerializer
# Create your views here.

class CreateUserView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=serializer.instance)
            return JsonResponse({'token': token.key, 'id': user.id}, status=201)
        else:
            print(serializer.errors)
            return JsonResponse(serializer.errors, status=400)


class LoginView(APIView):
    def post(self,request):
        login_data = json.loads(request.body)
        email = login_data.get('email')
        password = login_data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key, 'id': user.id}, status=200)
        else:
            return JsonResponse({'error': 'メールアドレスまたはパスワードが正しくありません'}, status=401)


class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return JsonResponse({'message': 'ログアウトしました'}, status=200)
        else:
            return JsonResponse({'error': 'ログインしていません'}, status=401)

class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({'error': '認証されていません'}, status=401)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = PostSerializer(data=request.data)

            if serializer.is_valid():
               serializer.save()
               return JsonResponse(serializer.data, status=201)
            else:
               return JsonResponse({'error': serializer.errors}, status=400)
               
        else:
            print('認証されていません')
            return JsonResponse({'error': '認証されていません'}, status=401)

class PostDetailView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, pk):
        if request.user.is_authenticated:
            post = Post.objects.get(id=pk)
            serializer = PostSerializer(post)
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse({'error': '認証されていません'}, status=401)

class PostlikesView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, pk):
        if request.user.is_authenticated:
            user = CustomUser.objects.get(id=request.user.id)
            print(user.id)
            post = Post.objects.get(id=pk)

            if post.likes.filter(id=user.id).exists():
                post.likes.remove(user)
                post.like_count -= 1
            else :
                post.likes.add(user)
                post.like_count += 1
            post.save()
            serializer = PostSerializer(post)
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse({'error': '認証されていません'}, status=401)

class UserDetailView(generics.ListAPIView):
    def get(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, status=200)

class UserEditView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserEditSerializer

    def update(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        serializers = UserEditSerializer(request.user, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=200)
        else:
            print(serializers.errors)
            return JsonResponse(serializers.errors, status=400)


class SearchView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request,):
        if request.user.is_authenticated:
            search_key = request.data.get('text')
            print(search_key)
            if search_key:
                search_result = Post.objects.filter(
                    Q(title__icontains=search_key) | Q(person__icontains=search_key) | Q(content__icontains=search_key)
                )

                if search_result:
                    serializers = PostSerializer(search_result, many=True,)
                    return JsonResponse(serializers.data, status=200,  safe=False)
                else:
                    return JsonResponse({'error': 'すみません。見つけられませんでした。'}, status=200)
            else:
                return JsonResponse({'error': '検索キーワードを入力してください'}, status=400)
        else:
            return JsonResponse({'error': '認証されていません'}, status=401)

class FollowUserView(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = UserSerializer

    def get(self, request, pk):
        if request.user.is_authenticated:
            follower = CustomUser.objects.get(id=request.user.id)##フォローする人
            print(request.user.id)
            following = CustomUser.objects.get(id=pk)##フォローされる人
            user = CustomUser.objects.get(id=pk)

            exits = Follow.objects.filter(follower=follower, following=following).exists()

            if not exits:
                Follow.objects.create(follower=follower, following=following)
                follower.follow_count += 1
                follower.save()
                following.follower_count += 1
                following.save()
                serializers = UserSerializer(user)
                return JsonResponse(serializers.data, status=200)
            else:
                return JsonResponse({'error': 'すでにフォローしています'}, status=200)
        else:
            return JsonResponse({'error': 'ログインしていません'}, status=401)