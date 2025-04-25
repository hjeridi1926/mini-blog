from django.contrib import admin
from .models import userDetail,Post,Comment
# Register your models here.
admin.site.register(userDetail)
admin.site.register(Post)
admin.site.register(Comment)
