from django.contrib import admin

from . import models


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'description')
    list_filter = ('category',)
    search_fields = ('name', 'year', 'description')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'score', 'author', 'pub_date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author', 'text', 'pub_date')
    search_fields = ('text',)


admin.site.register(models.Title, TitleAdmin)
admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Category, CategoriesAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.User)
