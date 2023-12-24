from rest_framework import serializers
from .models import CustomUser, UserManager, Post
from django.contrib.auth import get_user_model

# CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(allow_blank=True)
    password = serializers.CharField(allow_blank=True)
    freeword = serializers.CharField(allow_blank=True)

    def validate_username(self, value):
        if value == '':
            raise serializers.ValidationError('ユーザー名を入力してください')
        elif CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError('このユーザー名は既に使われています')
        return value
    
    
    def validate_email(self, value):
        if value == '':
            raise serializers.ValidationError('メールアドレスを入力してください')
        elif CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('このメールアドレスは既に使われています')
        return value

    def validate_password(self, value):
        if value == '':
            raise serializers.ValidationError('パスワードを入力してください')
        elif len(value) < 6:
            raise serializers.ValidationError('パスワードは6文字以上にしてください')
        return value


    def create(self, validated_data):
        new_user = CustomUser.objects.create_user(**validated_data)
        return new_user

    class Meta:
        model = CustomUser
        fields = [ 'id', 'email', 'username', 'password', 'freeword', 'post_count']

class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'freeword']
    
    username = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(allow_blank=True)
    freeword = serializers.CharField(allow_blank=True)

    def validate_username(self, value):
        if value == '':
            return self.instance.username
        return value
    def validate_email(self, value):
        if value == '':
            return self.instance.email
        return value
    def validate_freeword(self, value):
        if value == '':
            return self.instance.freeword
        return value
        

class PostSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'