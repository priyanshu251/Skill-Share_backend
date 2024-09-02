from community.repositories.community_repository import CommunityRepository


class CommunityService:
    def __init__(self):
        self.community_repository = CommunityRepository()

    def create_new_community(self, data, user):
        community = self.community_repository.create_new_community(data)
        self.community_repository.add_members_to_community(community.name, [user])
        self.community_repository.make_admin(community, user)
        return community
    
    def add_members_to_community(self, community_name, members):
        return self.community_repository.add_members_to_community(community_name, members)
    
    def make_admin(self, community_name, user):
        return self.community_repository.make_admin(community_name, user)
    
    def get_all_communities(self):
        return self.community_repository.get_all_communities()
    
    def create_new_session_for_community(self, data):
        return self.community_repository.create_new_session_for_community(data)
    
    def get_sessions(self, community):
        return self.community_repository.get_sessions(community)
    
    def give_feedback(self, data):
        return self.community_repository.give_feedback(data)
    
    def get_feedback(self, session):
        return self.community_repository.get_feedback(session)
    
