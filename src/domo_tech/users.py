"""Persistent users and authentication for Domo Tech."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import NotRequired, TypedDict

import bcrypt


class UserRecord(TypedDict):
    id: int
    username: str
    password_hash: str
    role: str
    active: bool
    created_at: str
    updated_at: NotRequired[str]


BASE_USERS = [
    {"username": "admin", "password": "1234", "role": "admin"},
    {"username": "cyber", "password": "punk", "role": "client"},
    {"username": "user", "password": "pass", "role": "client"},
]


class UserStore:
    """JSON-backed user store with soft migration for base users."""

    def __init__(self, path: Path | str = "data/users.json"):
        self.path = Path(path)
        self._users: list[UserRecord] = []
        self.load()

    def load(self) -> list[UserRecord]:
        if not self.path.exists():
            self._users = [self._base_user_record(index + 1, user) for index, user in enumerate(BASE_USERS)]
            self.save()
            return self.list_users()

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self._users = [self._normalize_user(user) for user in data]
        changed = self._merge_base_users()
        if changed or self._users != data:
            self.save()
        return self.list_users()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(self._users, file, indent=2, ensure_ascii=False)
            file.write("\n")

    def list_users(self) -> list[UserRecord]:
        return [dict(user) for user in self._users]

    def update_user(
        self,
        user_id: int,
        *,
        username: str | None = None,
        password: str | None = None,
        role: str | None = None,
        active: bool | None = None,
    ) -> tuple[bool, str, UserRecord | None]:
        user = self.get_by_id(user_id)
        if user is None:
            return False, "USUARIO NO ENCONTRADO", None

        new_username = username.strip() if username is not None else user["username"]
        if username is not None and len(new_username) < 3:
            return False, "EL USUARIO DEBE TENER AL MENOS 3 CARACTERES", None

        if username is not None:
            conflict = self.get_by_username(new_username)
            if conflict is not None and conflict["id"] != user_id:
                return False, "EL USUARIO YA EXISTE", None

        if password is not None and len(password) < 4:
            return False, "LA CONTRASEÑA DEBE TENER AL MENOS 4 CARACTERES", None

        user["username"] = new_username
        if password is not None:
            user["password_hash"] = self._hash_password(password)
        if role is not None:
            user["role"] = role
        if active is not None:
            user["active"] = bool(active)
        user["updated_at"] = self._timestamp()

        self.save()
        return True, "USUARIO ACTUALIZADO", dict(user)

    def promote_to_admin(self, user_id: int) -> tuple[bool, str, UserRecord | None]:
        return self.update_user(user_id, role="admin")

    def authenticate(self, username: str, password: str) -> UserRecord | None:
        user = self.get_by_username(username)
        if user is None or not user["active"]:
            return None
        if bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            return dict(user)
        return None

    def register_client(self, username: str, password: str) -> tuple[bool, str, UserRecord | None]:
        clean_username = username.strip()
        if len(clean_username) < 3:
            return False, "EL USUARIO DEBE TENER AL MENOS 3 CARACTERES", None
        if len(password) < 4:
            return False, "LA CONTRASEÑA DEBE TENER AL MENOS 4 CARACTERES", None
        if self.get_by_username(clean_username) is not None:
            return False, "EL USUARIO YA EXISTE", None

        user = {
            "id": self._next_id(),
            "username": clean_username,
            "password_hash": self._hash_password(password),
            "role": "client",
            "active": True,
            "created_at": self._timestamp(),
        }
        self._users.append(user)
        self.save()
        return True, "USUARIO REGISTRADO", dict(user)

    def get_by_username(self, username: str) -> UserRecord | None:
        normalized_username = username.strip().lower()
        for user in self._users:
            if user["username"].lower() == normalized_username:
                return user
        return None

    def get_by_id(self, user_id: int) -> UserRecord | None:
        for user in self._users:
            if user["id"] == user_id:
                return user
        return None

    def _merge_base_users(self) -> bool:
        changed = False
        existing_usernames = {user["username"].lower() for user in self._users}

        for base_user in BASE_USERS:
            if base_user["username"].lower() not in existing_usernames:
                self._users.append(self._base_user_record(self._next_id(), base_user))
                existing_usernames.add(base_user["username"].lower())
                changed = True

        return changed

    def _base_user_record(self, user_id: int, user: dict[str, str]) -> UserRecord:
        return {
            "id": user_id,
            "username": user["username"],
            "password_hash": self._hash_password(user["password"]),
            "role": user["role"],
            "active": True,
            "created_at": self._timestamp(),
        }

    def _normalize_user(self, user: dict) -> UserRecord:
        normalized: UserRecord = {
            "id": int(user["id"]),
            "username": str(user["username"]),
            "password_hash": str(user["password_hash"]),
            "role": str(user.get("role") or "client"),
            "active": bool(user.get("active", True)),
            "created_at": str(user.get("created_at") or self._timestamp()),
        }
        if user.get("updated_at"):
            normalized["updated_at"] = str(user["updated_at"])
        return normalized

    def _next_id(self) -> int:
        if not self._users:
            return 1
        return max(user["id"] for user in self._users) + 1

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()
