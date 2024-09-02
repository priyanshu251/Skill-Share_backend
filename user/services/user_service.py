from user.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.respository = repository

    def create_new_user(self, data):
        return self.respository.create_new_user(data=data)

    def get_user_from_firebase_uid(self, uid: str):
        return self.respository.get_user_from_firebase_uid(uid=uid)

    def search_user_by_name_and_email(self, search_query, user):
        return self.respository.search_user_by_name_and_email(
            search_query=search_query, user=user
        )
