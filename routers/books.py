from fastapi import APIRouter, status, HTTPException

from schemas.books import SBookAdd, SBook

from database import SessionDep

from repository import BookRepository

router = APIRouter()

# Добавление книги
@router.post("/books", status_code=status.HTTP_201_CREATED, response_model=SBook)
async def add_book(book: SBookAdd, db: SessionDep):
    return await BookRepository.add_book(db, book_data=book)


# Получить все книги 
@router.get("/books", response_model=list[SBook])
async def get_all_books(db: SessionDep):
    return await BookRepository.get_all_books(db)



# Получить одну книгу
@router.get("/books/{id}", response_model=SBook)
async def get_by_id(id: int, db: SessionDep):
    book = await BookRepository.get_by_id(id, db)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return book

# Обновит книгу
@router.put("/books/{id}", response_model=SBook)
async def update_book(id: int, update_data: SBookAdd, db: SessionDep):
    update_book = await BookRepository.update_book(id, update_data, db)
    if update_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return update_book

# Удалить книгу
@router.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int, db: SessionDep):
    book = await BookRepository.delete_book(id, db)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)