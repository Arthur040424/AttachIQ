import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import EvidenceSubmission, Placement, CompetencyUnit
from dependencies import get_current_user, User

router = APIRouter(prefix="/evidence", tags=["evidence"])

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"

@router.post("/submit")
async def submit_evidence(
  placement_id: uuid.UUID = Form(...),
  competency_unit_id: uuid.UUID = Form(...),
  description: str = Form(""),
  file: UploadFile = File(...),
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user)
):

  # Generate a unique file name to avoid collisions and preserve the original file extension
  suffix = Path(file.filename).suffix
  unique_filename = f"{uuid.uuid4()}{suffix}"
  file_path = UPLOAD_DIR / unique_filename

  # Write the file to disk
  with file_path.open("wb") as buffer:
      shutil.copyfileobj(file.file, buffer)

  # Build the URL path. What the frontend will use to retrieve it.
  file_url = f"/uploads/{unique_filename}"

  # Save the record to the database
  submission = EvidenceSubmission(
     placement_id=placement_id,
      competency_unit_id=competency_unit_id,
      description=description,
      file_url=file_url,
  )
  db.add(submission)
  await db.commit()
  await db.refresh(submission)

  return {"success": True, "data": {"submission_id": str(submission.id), "file_url": file_url}}