from datetime import datetime
import os
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TIMESTAMP, BigInteger, text, ForeignKey

PATH = "./storage/"


class User(Base):
    """user table."""

    __tablename__: str = "user"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    userspace: Mapped[str] = mapped_column(nullable=False, unique=True)
    storage_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP, nullable=False, server_default=text("now()")
    )
    storage: Mapped["Storage"] = relationship("Storage", back_populates="user")

    def New(self, username: str, password: str) -> None:
        self.username: str = username
        self.password: str = password
        self.userspace: str = username + "-space"
        self.storage_size: int = 1024 * 1024 * 100


class Storage(Base):
    """storage table."""

    __tablename__: str = "storage"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE"), nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)
    storage_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP, nullable=False, server_default=text("now()")
    )
    user: Mapped["User"] = relationship("User", back_populates="storage")
    files: Mapped[list["Files"]] = relationship("Files", back_populates="storage")

    def create(self, user_id, name, size) -> None:
        self.user_id: int = user_id
        self.name: str = name
        self.path: str = f"{PATH}{self.name}"
        self.storage_size: int = size
        try:
            os.makedirs(PATH + self.name)
            print("folder created successfully")
        except Exception as e:
            print(e)

    def delete(self) -> None:
        try:
            os.rmdir(PATH + self.userspace)
            print("folder deleted successfully")
        except Exception as e:
            print(e)


class Files(Base):
    """File table."""

    __tablename__: str = "file"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    storage_id: Mapped[int] = mapped_column(
        ForeignKey(Storage.id, ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP, nullable=False, server_default=text("now()")
    )
    storage: Mapped["Storage"] = relationship("Storage", back_populates="files")

    async def uploads(self, id, path, file=None):
        self.storage_id: int = id
        self.name: str = file.filename
        self.size: int = file.size
        self.path: str = f"{path}{self.name}"
        self.type: str = file.headers.get("content-type")

        if file is not None:
            with open(f"{self.path}", "wb") as file_out:
                file_out.write(await file.read())
