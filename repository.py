from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.books import SBookAdd
from models.books import BooksModel


class BookRepository:
    @classmethod
    async def add_one_book(cls, data_book: SBookAdd, session: AsyncSession) -> BooksModel:

        book_dict = data_book.model_dump()
        book = BooksModel(**book_dict)

        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    @classmethod
    async def get_all_books(cls, session: AsyncSession):

        query = select(BooksModel)
        result = await session.execute(query)
        books_models = result.scalars().all()

        return books_models

    @classmethod
    async def get_one_book(cls, session: AsyncSession, book_id: int) -> BooksModel | None:

        query = select(BooksModel).where(BooksModel.id == book_id)
        result = await session.execute(query)
        book_model = result.scalar_one_or_none()

        return book_model

    @classmethod
    async def update_book(cls, book_id: int, session: AsyncSession, data_book: SBookAdd):

        book = await cls.get_one_book(session, book_id)

        if book is None:
            return None

        book.title = data_book.title
        book.author = data_book.author
        book.year = data_book.year
        book.pages = data_book.pages
        book.is_read = data_book.is_read

        await session.commit()

        return book

    @classmethod
    async def delete_book(cls, book_id, session: AsyncSession):

        book = await cls.get_one_book(session, book_id)
        if book is None:
            return False

        await session.delete(book)
        await session.commit()
        return True
