from sqlalchemy import select, delete

from models.books import Books

from sqlalchemy.ext.asyncio import AsyncSession

from models.books import Books

from schemas.books import SBook, SBookAdd

class BookRepository:
    model = Books

    @classmethod
    async def add_book(cls, db: AsyncSession, book_data: SBookAdd) -> SBook:
        new_book = cls.model(**book_data.model_dump())
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        return new_book
    
    @classmethod
    async def get_all_books(cls, db: AsyncSession) -> list[Books]:
        query = select(cls.model)
        result = await db.execute(query)
    
        return list(result.scalars().all())
    
    @classmethod
    async def get_by_id(cls, id: int, db: AsyncSession) -> SBook:
        query = select(cls.model).where(cls.model.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def update_book(cls, id: int, update_data: SBookAdd, db: AsyncSession) -> SBook:
        query = select(cls.model).where(cls.model.id == id)
        result = await db.execute(query)
        current_book = result.scalar_one_or_none()

        if current_book is None:
            return None

        book_dict = update_data.model_dump()
        for key, value in book_dict.items():
            setattr(current_book, key, value)

        await db.commit()
        await db.refresh(current_book)
        return current_book
    
    @classmethod
    async def delete_book(cls, id: int, db: AsyncSession):
        query = select(cls.model).where(cls.model.id == id)
        result = await db.execute(query)
        book = result.scalar_one_or_none()

        if book is None:
            return None
    
        stmt = delete(cls.model).where(cls.model.id == id)
        await db.execute(stmt)
        await db.commit()
        return book