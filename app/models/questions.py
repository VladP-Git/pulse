from app.models import db
from typing import List, Optional, TYPE_CHECKING

# Импортируем зависимости только для проверки типов, избегая циклического импорта
if TYPE_CHECKING:
    from .category import Category
    from .answers import Answer


class Question(db.Model):
    __tablename__ = 'questions'

    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    text: db.Mapped[str] = db.mapped_column(db.String(255), nullable=False)

    # Внешний ключ на категорию (может быть Optional, если категория необязательна)
    category_id: db.Mapped[Optional[int]] = db.mapped_column(db.ForeignKey('categories.id', ondelete='SET NULL'))

    # Связи (Relationships)
    # Все связанные типы берем в кавычки: "Category" и "Answer"
    category: db.Mapped[Optional["Category"]] = db.relationship(back_populates="questions")
    # Исправленная связь с ответами (back_populates теперь совпадает с моделью Answer)
    answers: db.Mapped[List["Answer"]] = db.relationship(
        back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Question {self.id}: {self.text}>"
