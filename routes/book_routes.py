from fastapi import APIRouter, HTTPException
import mysql.connector

from logs.setup_logger import logger
from database.book_db import BookDB
from database.member_db import MemberDB


def validate(field: str, body: dict):
    if field not in body:
        logger.warning()
        HTTPException(status_code=400, detail=f"Field {field} is require") 

router = APIRouter()

@router.post("", status_code=201)
def create_book(body: dict):
    logger.debug("Got post request for book: %s", body)
    validate("title", body)
    validate("author", body)
    validate("genre", body)

    try:
        BookDB.create_book(body)
    except mysql.connector.Error as e:
        if e.errno == 1265:
            logger.warning("Got unvalid genre: %s", body.get("genre", ""))
            raise HTTPException(status_code=400, detail="Ganre can only be 'Fiction' | 'Non-Fiction' | 'Science' | 'History' | 'Other'")
        else:
            raise HTTPException(status_code=400, detail=str(e))

    logger.info("Created a new book: %s", body)


@router.get("")
def get_books():
    logger.info("Returns all books")
    return BookDB.get_all_books()


@router.get("/{id}")
def get_book(id: int):
    logger.info("Returns book %s", id)
    book = BookDB.get_book_by_id(id)
    if book is None:
        logger.warning("The book %s was not found", id)
        raise HTTPException(status_code=404, detail=f"The book {id} was not found")
    return book


@router.patch("/{id}")
def update_book(id: int, body: dict):
    logger.info("Updates book %s", id)
    if BookDB.get_book_by_id(id) is None:
        raise HTTPException(status_code=404, detail=f"The book {id} was not found")
    try:
        BookDB.update_book(id, body)
    except mysql.connector.Error as e:
        if e.errno == 1265:
            logger.warning("Got unvalid genre: %s", body.get("genre", ""))
            raise HTTPException(status_code=400, detail="Ganre can only be 'Fiction' | 'Non-Fiction' | 'Science' | 'History' | 'Other'")
        else:
            raise HTTPException(status_code=500, detail=str(e))
        


@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    logger.debug("Member %s tries to borrows book %s", member_id, id)
    if BookDB.get_book_by_id(id) is None:
        raise HTTPException(status_code=404, detail=f"The book {id} was not found")
    if MemberDB.get_member_by_id(member_id) is None:
        raise HTTPException(status_code=404, detail=f"The member {member_id} was not found")
    if not BookDB.is_available(id):
        return {"message": f"Book {id} is not available"}
    if not MemberDB.is_active(member_id):
        return {"message": f"Member {member_id} is not active"}
    if BookDB.count_active_borrows_by_member(member_id) >= 3:
        return {"message": f"Member {member_id} can not borrow more than 3 books"}
    BookDB.set_available(id, False, member_id)
    MemberDB.increment_borrows(member_id)


@router.patch("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    book = BookDB.get_book_by_id(id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"The book {id} was not found")
    if MemberDB.get_member_by_id(member_id) is None:
        raise HTTPException(status_code=404, detail=f"The member {member_id} was not found")
    if book["borrowed_by_member_id"] != member_id:
        raise HTTPException(status_code=400, detail=f"The book {id} is not borrowes by member {member_id}")
    logger.debug("Member %s tries to return book %s", member_id, id)
    BookDB.set_available(id, True, None)
    MemberDB.unincrement_borrows(member_id)