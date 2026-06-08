from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueStatus, IssueUpdate, IssueOut
from app.storage import load_data, save_data
from uuid import uuid4

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])


@router.get("/", response_model=list[IssueOut])
async def get_issues():
    """Retrieve all issues."""
    return load_data()


@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
async def create_issue(issue: IssueCreate):
    """Create a new issue."""
    data = load_data()
    new_issue = {
        "id": str(uuid4()),
        "title": issue.title,
        "description": issue.description,
        "priority": issue.priority,
        "status": IssueStatus.OPEN
    }
    data.append(new_issue)
    save_data(data)
    return new_issue


@router.get("/{issue_id}", response_model=IssueOut)
async def get_issue(issue_id: str):
    """Retrieve a specific issue by ID."""
    data = load_data()
    for issue in data:
        if issue["id"] == issue_id:
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Issue not found")


@router.put("/{issue_id}", response_model=IssueOut)
async def update_issue(issue_id: str, issue_update: IssueUpdate):
    """Update an existing issue."""
    data = load_data()
    for issue in data:
        if issue["id"] == issue_id:
            updated_issue = issue.copy()
            if issue_update.title is not None:
                updated_issue["title"] = issue_update.title
            if issue_update.description is not None:
                updated_issue["description"] = issue_update.description
            if issue_update.priority is not None:
                updated_issue["priority"] = issue_update.priority
            if issue_update.status is not None:
                updated_issue["status"] = issue_update.status
            save_data(data)
            return updated_issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Issue not found")


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(issue_id: str):
    """Delete an issue by ID."""
    data = load_data()
    for i, issue in enumerate(data):
        if issue["id"] == issue_id:
            del data[i]
            save_data(data)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Issue not found")
