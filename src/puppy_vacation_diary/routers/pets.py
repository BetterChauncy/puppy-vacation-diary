from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from puppy_vacation_diary.core.dependencies import get_db
from puppy_vacation_diary.models.pet import Pet
from puppy_vacation_diary.schemas.pet import PetCreate, PetResponse, PetUpdate

router = APIRouter(prefix="/pets", tags=["pets"])


@router.post("", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
async def create_pet(data: PetCreate, db: AsyncSession = Depends(get_db)) -> Pet:
    pet = Pet(**data.model_dump())
    db.add(pet)
    await db.flush()
    await db.refresh(pet)
    return pet


@router.get("", response_model=list[PetResponse])
async def list_pets(db: AsyncSession = Depends(get_db)) -> list[Pet]:
    result = await db.execute(select(Pet).order_by(Pet.id))
    return list(result.scalars().all())


@router.get("/{pet_id}", response_model=PetResponse)
async def get_pet(pet_id: int, db: AsyncSession = Depends(get_db)) -> Pet:
    pet = await db.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet


@router.put("/{pet_id}", response_model=PetResponse)
async def update_pet(pet_id: int, data: PetUpdate, db: AsyncSession = Depends(get_db)) -> Pet:
    pet = await db.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pet, field, value)
    await db.flush()
    await db.refresh(pet)
    return pet


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(pet_id: int, db: AsyncSession = Depends(get_db)) -> None:
    pet = await db.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    await db.delete(pet)
    await db.flush()
