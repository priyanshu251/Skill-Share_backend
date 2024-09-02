from django.db import models


class CommunityPost(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    community = models.ForeignKey("community.Community", on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    # image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_image = self.image

    def save(self, *args, **kwargs):
        old_image = self.__original_image
        super().save(*args, **kwargs)
        if old_image != self.image:
            old_image.delete(save=False)
        self.__original_image = self.image

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)  # delete image file from S3
        super().delete(*args, **kwargs)  # delete Post object

    def __str__(self):
        return self.content

    def upvotes(self) -> int:
        return self.votes.filter(value=Vote.UPVOTE).count()

    def downvotes(self):
        return self.votes.filter(value=Vote.DOWNVOTE).count()

    def score(self):
        upvotes = self.votes.filter(value=Vote.UPVOTE).count()
        downvotes = self.votes.filter(value=Vote.DOWNVOTE).count()
        return upvotes - downvotes


class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = (
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote"),
    )
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="votes"
    )
    post = models.ForeignKey(
        "community_post.CommunityPost", on_delete=models.CASCADE, related_name="votes"
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    def __str__(self):
        return f"{self.user}  {self.post}"


class SavedPost(models.Model):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="saved_posts"
    )
    post = models.ForeignKey(
        "community_post.CommunityPost",
        on_delete=models.CASCADE,
        related_name="saved",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} - {self.post}"


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        "community_post.CommunityPost",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
    )
    depth = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} commented {self.content[:50]} on {self.post}"

    def upvotes(self):
        return self.votes.filter(value=CommentVote.UPVOTE).count()

    def downvotes(self):
        return self.votes.filter(value=CommentVote.DOWNVOTE).count()

    def score(self):
        upvotes = self.votes.filter(value=CommentVote.UPVOTE).count()
        downvotes = self.votes.filter(value=CommentVote.DOWNVOTE).count()
        return upvotes - downvotes

    def save(self, *args, **kwargs):
        if self.parent is not None:
            self.depth = self.parent.depth + 1
        super().save(*args, **kwargs)


class CommentVote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = (
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote"),
    )

    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="comment_votes"
    )
    comment = models.ForeignKey(
        "community_post.Comment", on_delete=models.CASCADE, related_name="votes"
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ("user", "comment")

    def __str__(self):
        return f"{self.user} - {self.comment}"
