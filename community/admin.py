from django.contrib import admin
from community.models import (
    Community,
    Skill,
    Membership,
    Session,
    Badge,
    Feedback,
    TimeBank,
    Project,
)

# Register your models here.

admin.site.register(Community)
admin.site.register(Skill)
admin.site.register(Membership)
admin.site.register(Session)
admin.site.register(Badge)
admin.site.register(Feedback)
admin.site.register(TimeBank)
admin.site.register(Project)
