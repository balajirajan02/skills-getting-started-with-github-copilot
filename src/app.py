"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""


from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import Dict, List
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")
        # Add more activities
        activities.update({
            "Basketball Team": Activity(
                description="Join the school basketball team and compete in local leagues",
                schedule="Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
                max_participants=15,
                participants=["alex@mergington.edu"]
            ),
            "Soccer Club": Activity(
                description="Practice soccer skills and play friendly matches",
                schedule="Wednesdays, 3:30 PM - 5:30 PM",
                max_participants=18,
                participants=["lucas@mergington.edu"]
            ),
            "Art Club": Activity(
                description="Explore painting, drawing, and other visual arts",
                schedule="Mondays, 3:30 PM - 5:00 PM",
                max_participants=16,
                participants=["mia@mergington.edu"]
            ),
            "Drama Society": Activity(
                description="Participate in acting, stage production, and school plays",
                schedule="Fridays, 4:00 PM - 6:00 PM",
                max_participants=20,
                participants=["liam@mergington.edu"]
            ),
            "Math Olympiad": Activity(
                description="Prepare for math competitions and solve challenging problems",
                schedule="Thursdays, 3:30 PM - 5:00 PM",
                max_participants=10,
                participants=["noah@mergington.edu"]
            ),
            "Debate Club": Activity(
                description="Develop public speaking and argumentation skills",
                schedule="Tuesdays, 4:00 PM - 5:30 PM",
                max_participants=14,
                participants=["ava@mergington.edu"]
            ),
        })

# In-memory activity database

# Pydantic models
class Activity(BaseModel):
    description: str
    schedule: str
    max_participants: int
    participants: List[EmailStr]

class ActivityResponse(Activity):
    name: str

class SignupResponse(BaseModel):
    status: str
    message: str

# In-memory activity database
activities: Dict[str, Activity] = {
    "Chess Club": Activity(
        description="Learn strategies and compete in chess tournaments",
        schedule="Fridays, 3:30 PM - 5:00 PM",
        max_participants=12,
        participants=["michael@mergington.edu", "daniel@mergington.edu"]
    ),
    "Programming Class": Activity(
        description="Learn programming fundamentals and build software projects",
        schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        max_participants=20,
        participants=["emma@mergington.edu", "sophia@mergington.edu"]
    ),
    "Gym Class": Activity(
        description="Physical education and sports activities",
        schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        max_participants=30,
        participants=["john@mergington.edu", "olivia@mergington.edu"]
    )
}


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/static/index.html")


@app.get("/activities", response_model=Dict[str, Activity])
def get_activities() -> Dict[str, Activity]:
    return activities


@app.post("/activities/{activity_name}/signup", response_model=SignupResponse)
def signup_for_activity(activity_name: str, email: EmailStr) -> SignupResponse:
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # Check for duplicate signup
    if email in activity.participants:
        return SignupResponse(status="error", message=f"{email} is already signed up for {activity_name}")

    # Check for max participants
    if len(activity.participants) >= activity.max_participants:
        return SignupResponse(status="error", message=f"{activity_name} is already full")

    # Add student
    activity.participants.append(email)
    return SignupResponse(status="success", message=f"Signed up {email} for {activity_name}")
