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
    logger.debug("Creates member %s", body)
    validate("name", body)
    validate("email", body)

    try:
        new_id = MemberDB.create_member(body)
        logger.info("Created member %s successfully", new_id)
        return {"message": "Created a new member successfully", "id": new_id}
    except mysql.connector.Error:
        logger.warning("Email %s already exists", body["email"])
        raise HTTPException(status_code=400, detail=f"Email {body["email"]} already exists")
    


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
    logger.debug("Updates member %s", id)
    if MemberDB.get_member_by_id(id) is None:
        raise HTTPException(status_code=404, detail=f"The member {id} was not found")
    try:
        MemberDB.update_member(id, body)
        logger.info("Created member %s successfully", id)
        return {"message": "Updated member successfully", "id": id}
    except mysql.connector.Error:
        logger.warning("Email %s already exists", body["email"])
        raise HTTPException(status_code=400, detail=f"Email {body["email"]} already exists")


@router.patch("/{id}/deactivate")
def deactivate_member(id: int):
    logger.debug("Deactivates member %s", id)
    if MemberDB.get_member_by_id(id) is None:
        raise HTTPException(status_code=404, detail=f"The member {id} was not found")
    MemberDB.deactivate_member(id)
    logger.info("Deactivated member %s successfully", id)
    return {"message": "Deactivated member successfully", "id": id}


@router.patch("/{id}/activate")
def activate_member(id: int):
    logger.debug("Activates member %s", id)
    if MemberDB.get_member_by_id(id) is None:
        raise HTTPException(status_code=404, detail=f"The member {id} was not found")
    MemberDB.activate_member(id)
    logger.info("Activated member %s successfully", id)
    return {"message": "Activated member successfully", "id": id}