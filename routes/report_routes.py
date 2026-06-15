from fastapi import APIRouter, HTTPException

from logs.setup_logger import logger
from database.book_db import BookDB
from database.member_db import MemberDB


genres = ["Fiction", "Non-Fiction", "Science", "History", "Other"]

router = APIRouter()

@router.get("/summary")
def get_summary():
    logger.info("Returns smummary report")
    return {
        "total_books": BookDB.count_total_books(),
        "available_books": BookDB.count_available_books(),
        "currently_borrowed": BookDB.count_borrowed_books(),
        "active_members": MemberDB.count_active_members()
    }


@router.get("/books-by-genre")
def get_books_by_genre ():
    logger.info("Returns count of books by genres")
    books_by_genre = []
    for genre in genres:
        count = BookDB.count_by_genre(genre)
        books_by_genre.append({"Genre": genre, "COUNT": count})
    return books_by_genre


@router.get("/top-member")
def get_top_member ():
    top = MemberDB.get_top_member()
    logger.info("Returns the top borrowed member")
    return {
        "member_id": top["id"],
        "borrowed": top["total_borrows"]
    }