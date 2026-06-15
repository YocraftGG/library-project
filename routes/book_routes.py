from fastapi import APIRouter, HTTPException
import mysql.connector

from logs.setup_logger import logger
from database.book_db import BookDB
from database.member_db import MemberDB


def validate(field: str, body: dict):
    if field not in body:
        logger.warning("Field %s is missing", field)
        raise HTTPException(status_code=400, detail=f"Field {field} is required") 

router = APIRouter()

@router.post("", status_code=201)
def create_book(body: dict):
    logger.debug("Creates book %s", body)
    validate("title", body)
    validate("author", body)
    validate("genre", body)

    try:
        new_id = BookDB.create_book(body)
        logger.info("Created book %s successfully", new_id)
        return {"message": "Created a new book successfully", "id": new_id}
    except mysql.connector.Error as e:
        if e.errno == 1265:
            logger.warning("Got invalid genre: %s", body.get("genre", ""))
            raise HTTPException(status_code=400, detail="Ganre can only be 'Fiction' | 'Non-Fiction' | 'Science' | 'History' | 'Other'")
        else:
            raise HTTPException(status_code=400, detail=str(e))


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
    logger.debug("Updates book %s", id)
    if BookDB.get_book_by_id(id) is None:
        raise HTTPException(status_code=404, detail=f"The book {id} was not found")
    if not body:
        raise HTTPException(status_code=400, detail="No fields provided")
    try:
        BookDB.update_book(id, body)
        logger.info("Created book %s successfully", id)
        return {"message": "Updated book successfully", "id": id}
    except mysql.connector.Error as e:
        if e.errno == 1265:
            logger.warning("Got invalid genre: %s", body.get("genre", ""))
            raise HTTPException(status_code=400, detail="Ganre can only be 'Fiction' | 'Non-Fiction' | 'Science' | 'History' | 'Other'")
        else:
            raise HTTPException(status_code=500, detail=str(e))
        


@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    logger.debug("Member %s borrows book %s", member_id, id)
    if BookDB.get_book_by_id(id) is None:
        logger.warning("The book %s was not found", id)
        raise HTTPException(status_code=404, detail=f"The book {id} was not found")
    if MemberDB.get_member_by_id(member_id) is None:
        logger.warning("The member %s was not found", member_id)
        raise HTTPException(status_code=404, detail=f"The member {member_id} was not found")
    if not BookDB.is_available(id):
        logger.warning("The book %s is not available", id)
        raise HTTPException(status_code=400, detail=f"Book {id} is not available")
    if not MemberDB.is_active(member_id):
        logger.warning("The member %s is not active", member_id)
        raise HTTPException(status_code=400, detail=f"Member {member_id} is not active")
    if BookDB.count_active_borrows_by_member(member_id) >= 3:
        logger.warning("The member %s has already borrowed 3 books, he cannot borrow any more", member_id)
        raise HTTPException(status_code=400, detail=f"Member {member_id} can not borrow more than 3 books")
    BookDB.set_available(id, False, member_id)
    MemberDB.increment_borrows(member_id)
    logger.info("Member %s borrowed book %s successfully", member_id, id)
    return {
        "message": "Member borrowed book successfully",
        "member_id": member_id,
        "book_id": id
    }


@router.patch("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    logger.debug("Member %s returns book %s", member_id, id)
    book = BookDB.get_book_by_id(id)
    if book is None:
        logger.warning("The book %s was not found", id)
        raise HTTPException(status_code=404, detail=f"The book {id} was not found")
    if MemberDB.get_member_by_id(member_id) is None:
        logger.warning("The member %s was not found", member_id)
        raise HTTPException(status_code=404, detail=f"The member {member_id} was not found")
    if BookDB.is_available(id):
        logger.warning("The book %s is not borrowed")
        raise HTTPException(status_code=400, detail=f"The book {id} is not borrowed")
    if book["borrowed_by_member_id"] != member_id:
        logger.warning("The book %s is not borrowed by member %s", id, member_id)
        raise HTTPException(status_code=400, detail=f"The book {id} is not borrowed by member {member_id}")
    BookDB.set_available(id, True, None)
    logger.debug("Member %s returned book %s successfully", member_id, id)
    return {
        "message": "Member returned book successfully",
        "member_id": member_id,
        "book_id": id
    }