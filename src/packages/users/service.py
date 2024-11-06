from databases.mysql import DatabaseSession, User

from .utils import cast_single_user, cast_users_list


def get_all_users_controller():
    with DatabaseSession() as db:
        users = db.query(User).all()
        return cast_users_list(users)


def get_user_controller(user_id: str):
    with DatabaseSession() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        return cast_single_user(user)


def create_user_controller(user: dict):
    with DatabaseSession() as db:
        user_exists = (
            db.query(User).filter(User.username == user.username).first()
        )
        if user_exists:
            return False
        new_user = User(
            username=user.username,
            password=user.password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return cast_single_user(new_user)


def change_user_status_controller(
    user_id: str, is_active: bool = None, is_admin: bool = None
):
    with DatabaseSession() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        if is_active is not None:
            user.is_active = is_active
        if is_admin is not None:
            user.is_admin = is_admin
        db.commit()
        db.refresh(user)
        return cast_single_user(user)


def delete_user_controller(user_id: str):
    with DatabaseSession() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True
