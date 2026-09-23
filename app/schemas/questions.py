from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, StringConstraints, TypeAdapter

# Валидация текстов
QuestionText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=100)]
CategoryName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=50)]

# --- 1. Схемы Категорий ---
class CategoryBase(BaseModel):
    name: CategoryName

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# --- 2. Схемы Вопросов ---
class QuestionBase(BaseModel):
    text: QuestionText

class QuestionCreate(QuestionBase):
    # Разрешаем указывать категорию при создании вопроса
    category_id: Optional[int] = None

class QuestionUpdate(QuestionBase):
    text: QuestionText | None = None
    category_id: Optional[int] = None

class QuestionRead(QuestionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    # Интеграция данных о категории
    category: Optional[CategoryRead] = None

# Соответствие требованию задания по имени схемы ответа
QuestionResponse = QuestionRead

# --- 3. Адаптеры списков ---
QuestionsList = TypeAdapter(list[QuestionResponse])
CategoriesList = TypeAdapter(list[CategoryRead])
