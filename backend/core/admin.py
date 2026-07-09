from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Dataset)
admin.site.register(MLModel)
admin.site.register(TrainingJob)
admin.site.register(ChatHistory)
admin.site.register(Export)