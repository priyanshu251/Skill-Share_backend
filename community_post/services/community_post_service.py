from community_post.models import CommunityPost

from community_post.repositories.community_post_repository import (
    CommunityPostRepository,
)


class CommunityPostService:
    def __init__(self, repository: CommunityPostRepository) -> None:
        self.repository = repository

    def create_new_community_post(self, data):
        return self.repository.create_new_community_post(data=data)

    def get_all_community_posts(self, request):
        return self.repository.get_all_community_posts(request=request)

    def get_community_post(self, pk, request):
        return self.repository.get_community_post(pk=pk, request=request)

    # def get_community_post_comments(self, post_pk, request):
    #     return self.repository.get_community_post_comments(
    #         post_pk=post_pk, request=request
    #     )

    def get_community_posts_by_community(self, community_pk, request):
        return self.repository.get_community_posts_by_community(
            community_pk=community_pk, request=request
        )

    def save_post(self, post, user, save=True):
        return self.repository.save_post(post=post, user=user, save=save)

    def vote_post(self, post, user, value):
        return self.repository.vote_post(post=post, user=user, value=value)

    def get_saved_posts(self, request, user):
        return self.repository.get_saved_posts(request=request, user=user)

    def get_post_comments(self, request, post, parent):
        return self.repository.get_comments(request=request, post=post, parent=parent)

    def create_new_comment(self, post, request, parent, content):
        return self.repository.create_new_comment(
            post=post, request=request, parent=parent, content=content
        )
    
    def get_user_posts(self, request):
        return self.repository.get_user_posts(request=request)
