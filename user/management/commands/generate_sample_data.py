import random
from faker import Faker
from django.core.management.base import BaseCommand
from user.models import User
from community.models import Skill, Community, Membership, Badge, Session, Feedback, TimeBank, Project
from community_post.models import CommunityPost, Vote, SavedPost, Comment, CommentVote

class Command(BaseCommand):
    help = 'Generate sample data for the application'

    def handle(self, *args, **kwargs):
        fake = Faker()

        def valid_image_url():
            return f"https://picsum.photos/seed/{fake.uuid4()}/200/300"

        # Create Skills
        skills = []
        for _ in range(10):
            skill = Skill.objects.create(name=fake.word())
            skills.append(skill)

        # Create Users
        users = []
        for _ in range(50):
            user = User.objects.create(
                uid=fake.uuid4(),
                name=fake.name(),
                email=fake.email(),
                picture=valid_image_url()
            )
            users.append(user)

        # Create Communities
        communities = []
        for skill in skills:
            for _ in range(2):
                community = Community.objects.create(
                    name=f"{skill.name} Community {fake.word()}",
                    skill=skill,
                    description=fake.text(),
                    banner=valid_image_url(),
                    profile_image=valid_image_url()
                )
                communities.append(community)

        # Create Memberships
        for user in users:
            for community in random.sample(communities, 3):
                Membership.objects.create(user=user, community=community, is_admin=fake.boolean())

        # Create Badges
        for user in users:
            for skill in random.sample(skills, 3):
                Badge.objects.create(user=user, skill=skill, level=random.randint(1, 5))

        # Create Sessions
        sessions = []
        for community in communities:
            for _ in range(5):
                session = Session.objects.create(
                    community=community,
                    time=fake.date_time_this_year(),
                    description=fake.text(),
                    duration=random.randint(30, 120)
                )
                sessions.append(session)

        # Create Feedbacks
        for session in sessions:
            for _ in range(5):
                Feedback.objects.create(
                    user=random.choice(users),
                    session=session,
                    rating=random.randint(1, 5),
                    comments=fake.text()
                )

        # Create TimeBanks
        for user in users:
            TimeBank.objects.create(user=user, hours_spent=random.randint(1, 100))

        # Create Projects
        for community in communities:
            for _ in range(2):
                project = Project.objects.create(
                    community=community,
                    description=fake.text()
                )
                project.members.set(random.sample(users, 5))

        # Create Community Posts
        posts = []
        for community in communities:
            for _ in range(10):
                post = CommunityPost.objects.create(
                    title=fake.sentence(),
                    user=random.choice(users),
                    community=community,
                    content=fake.text(),
                    image=valid_image_url()
                )
                posts.append(post)

        # Create Votes
        for post in posts:
            for _ in range(10):
                Vote.objects.create(
                    user=random.choice(users),
                    post=post,
                    value=random.choice([Vote.UPVOTE, Vote.DOWNVOTE])
                )

        # Create Saved Posts
        for user in users:
            for post in random.sample(posts, 5):
                SavedPost.objects.create(user=user, post=post)

        # Create Comments and Comment Votes
        comments = []
        for post in posts:
            for _ in range(5):
                comment = Comment.objects.create(
                    content=fake.text(),
                    user=random.choice(users),
                    post=post
                )
                comments.append(comment)

        for comment in comments:
            users_voted = set()
            for _ in range(5):
                user = random.choice(users)
                while user in users_voted:
                    user = random.choice(users)
                users_voted.add(user)
                CommentVote.objects.create(
                    user=user,
                    comment=comment,
                    value=random.choice([CommentVote.UPVOTE, CommentVote.DOWNVOTE])
                )

        self.stdout.write(self.style.SUCCESS('Successfully generated sample data'))
