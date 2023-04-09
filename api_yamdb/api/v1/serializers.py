from re import match

from django.db.models import Avg

from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions, serializers

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
    User
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('__all__')


class TitleSerializerRead(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('__all__')
        read_only_fields = ('id',)

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if not rating:
            return rating
        return round(rating, 1)


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        author = self.context.get('request').user
        title = self.context.get('view').kwargs.get('title_id')
        request = self.context['request']
        if request.method == 'POST':
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError('Повторно оценить нельзя')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=254,
        allow_blank=False
    )
    username = serializers.CharField(
        max_length=150,
        allow_blank=False
    )

    def validate_username(self, value):
        if not match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'Имя содержит недопустимые символы'
            )
        if value == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя'
            )
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if (
            User.objects.filter(username=username).exists()
            and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError(
                'Пользователь с таким именем сущестует'
            )
        if (
            User.objects.filter(email=email).exists()
            and User.objects.get(email=email).username != username
        ):
            raise serializers.ValidationError(
                'Пользователь с такой почтой сущестует'
            )
        return data


class GetJWTSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        allow_blank=False,
    )
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'confirmation_code', 'token')

    def validate(self, data):
        existing = User.objects.filter(
            username=data['username'],
        ).exists()
        if not existing:
            raise exceptions.NotFound('Пользователь не найден')
        user = User.objects.get(username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise exceptions.ParseError('Неверный код подтверждения.')
        return data

    def get_token(self, obj):
        username = list(obj.items())[0][1]
        confirmation_code = list(obj.items())[1][1]
        user = User.objects.get(
            username=username,
            confirmation_code=confirmation_code
        )
        refresh = RefreshToken.for_user(user).access_token
        return str(refresh)

    def get_id(self, obj):
        username = list(obj.items())[0][1]
        user = User.objects.get(username=username)
        return user.id


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
