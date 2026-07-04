from database import Model
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional


class Books(Model):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[Optional[int]]
    pages: Mapped[Optional[int]]
    is_read: Mapped[bool] = mapped_column(default=False)
    