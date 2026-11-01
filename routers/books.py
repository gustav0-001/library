from fastapi import APIRouter, Depends, HTTPException, status
from schemas.books import SBookAdd, SBook
from sqlalchemy.ext.asyncio import AsyncSession
from repository import BookRepository
from database import get_db

router = APIRouter(
    prefix="/books",
    tags=["Библиотека"]
)

@router.post("", response_model=SBook, status_code=status.HTTP_201_CREATED)
async def add_book(book_data: SBookAdd, session: AsyncSession = Depends(get_db)):

    book = await BookRepository.add_one_book(book_data, session)

    return book

@router.get("", response_model=list[SBook])
async def get_books(session: AsyncSession = Depends(get_db)):

    books = await BookRepository.get_all_books(session)
    return books

@router.get("/{book_id}", response_model=SBook)
async def get_one_book(book_id: int, session:  AsyncSession = Depends(get_db)):
    book = await BookRepository.get_one_book(session, book_id)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

    return book

@router.put("/{book_id}")
async def put_book(book_id, book_data: SBookAdd, session: AsyncSession = Depends(get_db)):
    book_in = await BookRepository.update_book(book_id, session, book_data)

    if not book_in:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

    return book_in

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, session: AsyncSession = Depends(get_db)):
    result = await BookRepository.delete_book(book_id, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return
