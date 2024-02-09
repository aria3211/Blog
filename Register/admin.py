from django.contrib import admin
from .models import Relation


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    raw_id_fields = ('from_user','to_user',)


