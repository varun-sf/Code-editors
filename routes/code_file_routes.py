from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  # Use AsyncSession instead of Session
from database import get_db
from controllers.code_file import create_code_file, get_code_file, get_code_files_by_owner, update_code_file, delete_code_file
from models.models import CodeFileCreate, CodeFileUpdate, CodeFileResponse
from dependencies.auth import get_current_user  # Assumes JWT-based authentication
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/code-files")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/", response_model=CodeFileResponse)
async def create_code_file_route(
    code_file_data: CodeFileCreate,
    db: AsyncSession = Depends(get_db),  # ✅ Use AsyncSession
    current_user: dict = Depends(get_current_user)
):
    return await create_code_file(db, code_file_data, owner_id=current_user["id"])

@router.get("/{file_id}", response_model=CodeFileResponse)
async def get_code_file_route(
    file_id: int,
    db: AsyncSession = Depends(get_db),  # ✅ Use AsyncSession
    current_user: dict = Depends(get_current_user)
):
    code_file = await get_code_file(db, file_id)
    if not code_file or code_file.owner_id != current_user["id"]:
        raise HTTPException(status_code=404, detail="File not found or unauthorized")
    return code_file

@router.get("/", response_model=list[CodeFileResponse])
async def get_user_code_files_route(
    db: AsyncSession = Depends(get_db),  # ✅ Use AsyncSession
    current_user: dict = Depends(get_current_user)
):
    return await get_code_files_by_owner(db, current_user["id"])

@router.put("/{file_id}", response_model=CodeFileResponse)
async def update_code_file_route(
    file_id: int,
    code_file_data: CodeFileUpdate,
    db: AsyncSession = Depends(get_db),  # ✅ Use AsyncSession
    current_user: dict = Depends(get_current_user)
):
    code_file = await get_code_file(db, file_id)
    if not code_file or code_file.owner_id != current_user["id"]:
        raise HTTPException(status_code=404, detail="File not found or unauthorized")
    
    return await update_code_file(db, file_id, code_file_data)

@router.delete("/{file_id}")
async def delete_code_file_route(
    file_id: int,
    db: AsyncSession = Depends(get_db),  # ✅ Use AsyncSession
    current_user: dict = Depends(get_current_user)
):
    code_file = await get_code_file(db, file_id)
    if not code_file or code_file.owner_id != current_user["id"]:
        raise HTTPException(status_code=404, detail="File not found or unauthorized")
    
    await delete_code_file(db, file_id)
    return {"detail": "File deleted successfully"}
