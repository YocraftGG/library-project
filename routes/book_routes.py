from fastapi import APIRouter, HTTPException

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

    BookDB.create_book(body)
    logger.info("Created a new book: %s", body)


@router.get("")
def get_books():
    logger.info("Returns all books")
    return BookDB.get_all_books()


@router.get("/{id}")
def get_book(id: int):
    logger.info("Returns book %s", id)
    return BookDB.get_book_by_id(id)


@router.patch("/{id}")
def update_book(body: int):
    logger.info("Updates book %s", id)
    return BookDB.update_book(id, body)


@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    logger.debug("Member %s tries to borrows book %s", member_id, id)
    if not BookDB.is_available(id):
        return {"message": f"Book {id} is not available"}
    if not MemberDB.is_active(id):
        return {"message": f"Member {member_id} is not active"}
    if BookDB.count_active_borrows_by_member(member_id) >= 3:
        return {"message": f"Member {member_id} can not borrow more than 3 books"}
    BookDB.set_available(id, False, member_id)
    MemberDB.increment_borrows(member_id)


@router.patch("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    logger.debug("Member %s tries to return book %s", member_id, id)
    BookDB.set_available(id, True, None)
    MemberDB.unincrement_borrows(member_id)