from django.contrib import admin
from .models import User, NormalChatHistory, SchedChatHistory, TutorChatHistory, College, CollegeList

# Register your models here.
admin.site.register(User)
admin.site.register(NormalChatHistory)
admin.site.register(SchedChatHistory)
admin.site.register(TutorChatHistory)
admin.site.register(College)
admin.site.register(CollegeList)