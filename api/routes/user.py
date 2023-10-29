from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy import select
from database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.users import CreateUser
from models import Storage, User, Files


# create an instance of apirouter and call it
router = APIRouter(prefix="/user", tags=["Users"])


## sign up
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, str],
)
async def sign_up(
    user: CreateUser,
    db: AsyncSession = Depends(get_session),
):
    new_user = User()
    new_user.New(user.username, user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    user_storage = Storage()
    user_storage.create(new_user.id, new_user.userspace, new_user.storage_size)
    db.add(user_storage)
    await db.commit()
    await db.refresh(user_storage)
    return {"message": "success"}


@router.post(
    "/files",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, str],
)
async def upload(
    storage_id: int,
    storage_path: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
):
    new_file = Files()
    await new_file.uploads(storage_id, storage_path, file)
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)
    q = await db.execute(select(Storage).filter_by(id=storage_id))
    storage = q.scalar()
    storage.storage_size -= file.size
    await db.commit()
    await db.refresh(storage)
    return {"message": "success"}
