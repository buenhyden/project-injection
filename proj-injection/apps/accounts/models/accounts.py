"""app(accounts)와 관련된 Django의 model을 정의."""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class AccountManager(BaseUserManager):
    """auth user 모델에서 사용할 custom manager."""

    def create_user(self, username, password=None, **extra_fields):
        """사용자 계정 생성.

        Args:
            username (str): 사용자 계정
            password (str, optional): 비밀번호. Defaults to None.
            extra_fields (dict): 기타

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if not username:
            raise ValueError("username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """관리자 계정 생성.

        Args:
            username (str): 사용자 계정
            password (str, optional): 비밀번호. Defaults to None.
            extra_fields (dict): 기타

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class Accounts(AbstractBaseUser, PermissionsMixin):
    """Accounts : 사용자 계정.

    custom auth user model.
    """

    username = models.CharField(max_length=150, unique=True)  # 사용자 이름
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # 활성 비활성 - 탈퇴시 비활성 (core)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    class Meta:
        """Account metadata."""

        db_table = "accounts"
