from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.code_file import CodeFile
from models.models import CodeFileCreate, CodeFileUpdate

async def create_code_file(db: AsyncSession, code_file_data: CodeFileCreate, owner_id: int):
    code_file = CodeFile(
        filename=code_file_data.filename,
        content=code_file_data.content,
        owner_id=owner_id
    )
    db.add(code_file)
    await db.commit()
    await db.refresh(code_file)
    return code_file

async def get_code_file(db: AsyncSession, file_id: int):
    result = await db.execute(select(CodeFile).where(CodeFile.id == file_id))
    return result.scalars().first()

async def get_code_files_by_owner(db: AsyncSession, owner_id: int):
    result = await db.execute(select(CodeFile).where(CodeFile.owner_id == owner_id))
    return result.scalars().all()

async def update_code_file(db: AsyncSession, file_id: int, code_file_data: CodeFileUpdate):
    result = await db.execute(select(CodeFile).where(CodeFile.id == file_id))
    code_file = result.scalars().first()
    if code_file:
        code_file.content = code_file_data.content
        await db.commit()
        await db.refresh(code_file)
    return code_file

async def delete_code_file(db: AsyncSession, file_id: int):
    result = await db.execute(select(CodeFile).where(CodeFile.id == file_id))
    code_file = result.scalars().first()
    if code_file:
        await db.delete(code_file)
        await db.commit()
    return code_file
