from django.contrib import admin
from .models import User,Services,Techno,Package,Blog,Blog_comment,Work,Cart,Transaction

# Register your models here.

admin.site.register(User)
admin.site.register(Services)
admin.site.register(Techno)
admin.site.register(Package)
admin.site.register(Blog)
admin.site.register(Blog_comment)
admin.site.register(Work)
admin.site.register(Cart)
admin.site.register(Transaction)