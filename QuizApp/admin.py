from django.contrib import admin

from .models import *

admin.site.register(Creator)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Candidate)
admin.site.register(Result)
