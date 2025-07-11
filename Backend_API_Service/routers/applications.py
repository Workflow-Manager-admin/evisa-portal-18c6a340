from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)

class ApplicationBase(BaseModel):
    """Common visa application fields."""
    applicant_id: int = Field(..., description="User ID of the applicant")
    passport_number: str = Field(..., description="Passport number")
    nationality: str = Field(..., description="Country of citizenship")
    application_status: str = Field("draft", description="Current status of application")

class ApplicationCreate(ApplicationBase):
    passport_scan_url: str = Field(..., description="Document upload: URL of passport scan")
    purpose_of_travel: str = Field(..., description="Purpose stated in the application")
    intended_travel_date: str = Field(..., description="Intended date of travel (YYYY-MM-DD)")

class ApplicationResponse(ApplicationBase):
    id: int = Field(..., description="Application unique identifier")

# Simulated application storage for scaffolding (replace with real DB layer)
_fake_applications_db = {}

# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new visa application",
    description="Create a new visa application for the given applicant.",
    responses={400: {"description": "Invalid data or duplicate application."}},
)
def create_application(data: ApplicationCreate):
    """
    Create a new visa application.
    """
    app_id = len(_fake_applications_db) + 1
    _fake_applications_db[app_id] = data.dict() | {"id": app_id}
    return ApplicationResponse(id=app_id, **data.dict())

# PUBLIC_INTERFACE
@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
    summary="Get application by ID",
    description="Fetch a visa application's details by unique identifier.",
    responses={404: {"description": "Application not found."}},
)
def get_application(application_id: int):
    """
    Get application details by ID.
    """
    app = _fake_applications_db.get(application_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")
    return ApplicationResponse(**app)
