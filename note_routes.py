import math

from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User,Note
from schemas import NoteModel,NoteStatusModel, Pagination
from database import Session , engine
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, add_pagination, paginate

note_router=APIRouter(
    prefix="/notes",
    tags=['notes']
)


session=Session(bind=engine)


@note_router.post('/note',status_code=status.HTTP_201_CREATED)
async def place_an_note(note:NoteModel,Authorize:AuthJWT=Depends()):
    """
        ## Placing an Note
        This requires the following
        - quantity : integer
        - note_data: str
    
    """


    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user=Authorize.get_jwt_subject()

    user=session.query(User).filter(User.username==current_user).first()


    new_note=Note(
        note_data=note.note_data,
        quantity=note.quantity
    )

    new_note.user=user

    session.add(new_note)

    session.commit()


    response={
        "note_data":new_note.note_data,
        "quantity":new_note.quantity,
        "id":new_note.id,
        "note_status":new_note.note_status
    }

    return jsonable_encoder(response)



    
@note_router.get('/notes')
async def list_all_notes(Authorize:AuthJWT=Depends()):
    """
        ## List all notes
        This lists all  notes made. It can be accessed by superusers
        
    
    """


    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user=Authorize.get_jwt_subject()

    user=session.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        notes=session.query(Note).all()

        return jsonable_encoder(notes)

    raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        )


@note_router.get('/notes/{id}')
async def get_note_by_id(id:int,Authorize:AuthJWT=Depends()):
    """
        ## Get an note by its ID
        This gets an note by its ID and is only accessed by a superuser
        

    """


    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    user=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        note=session.query(Note).filter(Note.id==id).first()

        return jsonable_encoder(note)

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not alowed to carry out request"
        )

    
@note_router.get('/user/notes')
async def get_user_notes(paginationData:Pagination, Authorize:AuthJWT=Depends()):
    """
        ## Get a current user's notes
        This lists the notes made by the currently logged in users
    
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    user=Authorize.get_jwt_subject()
    page=paginationData.page
    windowSize=paginationData.windowSize
    current_user=session.query(User).filter(User.username==user).first()
    offset_min = int(len(current_user.notes) / windowSize * (page-1))
    offset_max = int(len(current_user.notes)/windowSize*(page-1)) + windowSize
    print("offset_minn = ", offset_min)
    print("offset_max = ", offset_max)

    if len(current_user.notes)<windowSize:
            return {
                "notesOfUser":current_user.notes,
                "allData": current_user.notes,
                "page":page,
                "windowSize":windowSize,
                "total":len(current_user.notes)
            }
    else:
        return {
            "notesOfUser": current_user.notes[offset_min:offset_max],
            "allData": current_user.notes,
            "page": page,
            "windowSize": windowSize,
            "total": len(current_user.notes)
        }



@note_router.get('/user/note/{id}/')
async def get_specific_note(id:int,Authorize:AuthJWT=Depends()):
    """
        ## Get a specific note by the currently logged in user
        This returns an note by ID for the currently logged in user
    
    """


    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    subject=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==subject).first()

    notes=current_user.notes

    for o in notes:
        if o.id == id:
            return jsonable_encoder(o)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="No note with such id"
    )


@note_router.put('/note/update/{id}/')
async def update_note(id:int,note:NoteModel,Authorize:AuthJWT=Depends()):
    """
        ## Updating an note
        This udates an note and requires the following fields
        - quantity : integer
        - note_data: str
    
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")

    note_to_update=session.query(Note).filter(Note.id==id).first()

    note_to_update.quantity=note.quantity
    note_to_update.note_data=note.note_data

    session.commit()


    response={
                "id":note_to_update.id,
                "quantity":note_to_update.quantity,
                "note_data":note_to_update.note_data,
                "note_status":note_to_update.note_status,
            }

    return jsonable_encoder(note_to_update)

    
@note_router.patch('/note/update/{id}/')
async def update_note_status(id:int,
        note:NoteStatusModel,
        Authorize:AuthJWT=Depends()):


    """
        ## Update an note's status
        This is for updating an note's status and requires ` note_status ` in str format
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")

    username=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==username).first()

    if current_user.is_staff:
        note_to_update=session.query(Note).filter(Note.id==id).first()

        note_to_update.note_status=note.note_status

        session.commit()

        response={
                "id":note_to_update.id,
                "quantity":note_to_update.quantity,
                "note_data":note_to_update.note_data,
                "note_status":note_to_update.note_status,
            }

        return jsonable_encoder(response)


@note_router.delete('/note/delete/{id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_note(id:int,Authorize:AuthJWT=Depends()):

    """
        ## Delete an Note
        This deletes an note by its ID
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")


    note_to_delete=session.query(Note).filter(Note.id==id).first()

    session.delete(note_to_delete)

    session.commit()

    return note_to_delete
