from databases.mysql.models import User as UserModel

from .responses import UserList, User


def cast_single_user(user: UserModel):
    return User(
        id=user.id,
        username=user.username,
        profile_img=user.profile_img,
        is_admin=user.is_admin,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def cast_users_list(users: list[UserModel]):
    return UserList(
        items=[cast_single_user(user) for user in users],
        total=len(users),
    )
