from django.contrib import admin
from community_post.models import CommunityPost, Vote, Comment, CommentVote, SavedPost

# Register your models here.

admin.site.register(CommunityPost)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(CommentVote)
admin.site.register(SavedPost)
