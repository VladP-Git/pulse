from app.models import db
from typing import List, TYPE_CHECKING

# Импортируем Question только для проверки типов, это уберет ошибку линтера
if TYPE_CHECKING:
    from .questions import Question

class Category(db.Model):
    __tablename__ = 'categories'

    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    name: db.Mapped[str] = db.mapped_column(db.String(100), unique=True, nullable=False)

    # Связь: у одной категории может быть много вопросов
    # Важно: указываем тип как СТРОКУ "Question" внутри list[...]
    questions: db.Mapped[List["Question"]] = db.relationship(
        back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category {self.id}: {self.name}>"
