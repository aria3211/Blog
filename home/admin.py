from django.contrib import admin
from .models import Post,Comment,Like

# admin.site.register(Post,PostAdmin)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user','slug','updated')
    search_fields = ('slug',)
    sortable_by = ('updated',)
    list_filter = ('updated',)
    prepopulated_fields = {'slug':('body',)}
    raw_id_fields = ('user',)

@admin.register(Comment)
class CommnetAdmin(admin.ModelAdmin):
    list_display = ('user','post','created')
    raw_id_fields = ('user','post',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)