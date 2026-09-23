from app.models import db
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .category import Category
    from .answers import Answer


class Question(db.Model):
    __tablename__ = 'questions'

    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    text: db.Mapped[str] = db.mapped_column(db.String(255))

    # Поле внешнего ключа (ForeignKey) для категорий
    category_id: db.Mapped[Optional[int]] = db.mapped_column(
        db.ForeignKey('categories.id', ondelete='SET NULL')
    )

    # Связь с моделью Category
    category: db.Mapped[Optional["Category"]] = db.relationship(back_populates="questions")

    answers: db.Mapped[list["Answer"]] = db.relationship(
        back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Question {self.id}: {self.text}>"
