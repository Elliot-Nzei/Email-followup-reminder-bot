from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import followups, users, auth
from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduler import check_due_followups

# Initialize DB tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Email Follow-Up Reminder Bot", version="1.0")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(followups.router)

# Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_due_followups, "interval", hours=1)
scheduler.start()