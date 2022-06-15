import time
import uuid
from typing import Optional

from flask import session


class MemSession(dict):
    sid: str = None

    def __init__(self) -> None:
        super().__init__()
        self.sid = str(uuid.uuid4())
        if self.sid in mem_storage:
            raise RuntimeError("uuid session conflict")
        self["login-timestamp"] = str(time.time())
        mem_storage[self.sid] = self

    def get_data(self):
        return self.__dict__


def __get_sid() -> Optional[str]:
    if "sid" in session:
        return session["sid"]


def start_session() -> MemSession:
    sess = MemSession()
    session["sid"] = sess.sid
    return sess


def load_session() -> MemSession:
    return mem_storage[__get_sid()]


def drop_session() -> None:
    del mem_storage[__get_sid()]
    session["sid"] = None


def session_exists() -> bool:
    return __get_sid() in mem_storage


mem_storage: dict[str, MemSession] = {}
