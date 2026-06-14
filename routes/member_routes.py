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
def create_member(body: dict):
    logger.debug("Got post request for member: %s", body)
    validate("name", body)
    validate("email", body)

    try:
        MemberDB.create_member(body)
    except mysql.connector.Error:
        logger.warning("Email %s already exists", body["email"])
        raise HTTPException(status_code=400, detail=f"Email {body["email"]} already exists")
    
    logger.info("Created a new member: %s", body)


@router.get("")
def get_members():
    logger.info("Returns all members")
    return MemberDB.get_all_members()


@router.get("/{id}")
def get_member(id: int):
    logger.info("Returns member %s", id)
    member = MemberDB.get_member_by_id(id)
    if member is None:
        logger.warning("The member %s was not found", id)
        raise HTTPException(status_code=404, detail=f"The member {id} was not found")
    return member


@router.patch("/{id}")
def update_member(id: int, body: dict):
    logger.info("Updates member %s", id)
    if MemberDB.get_member_by_id(id) is None:
        raise HTTPException(status_code=404, detail=f"The member {id} was not found")
    try:
        MemberDB.update_member(id, body)
    except mysql.connector.Error:
        logger.warning("Email %s already exists", body["email"])
        raise HTTPException(status_code=400, detail=f"Email {body["email"]} already exists")


@router.patch("/{id}/deactivate")
def deactivate_member(id: int):
    if MemberDB.get_member_by_id(id) is None:
        raise HTTPException(status_code=404, detail=f"The member {id} was not found")
    logger.debug("activates member %s", id)
    MemberDB.deactivate_member(id)


@router.patch("/{id}/activate")
def activate_member(id: int):
    if MemberDB.get_member_by_id(id) is None:
        raise HTTPException(status_code=404, detail=f"The member {id} was not found")
    logger.debug("deactivates member %s", id)
    MemberDB.activate_member(id)