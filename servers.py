from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import User
from schemas import RegisterRequest, LoginRequest, UserResponse, MessageResponse
from auth import hash_password, verify_password

# Create tables (for first run). After using Alembic, you can comment this out.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Authentication API",
    description="Register & Login APIs with SQLite + mobile field",
    version="1.0.0",
)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Authentication API is running"}


# ============================================================
# Registration
# ============================================================
@app.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    # DEBUG
    print("================================")
    print("REGISTER DATA:", request.model_dump())
    print("MOBILE RECEIVED:", request.mobile)
    print("================================")

    # Check if email already exists
    statement = select(User).where(User.email == request.email)
    existing_user = db.scalars(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        name=request.name,
        email=request.email,
        password=hash_password(request.password),
        mobile=request.mobile,
    )

    print("MOBILE BEFORE SAVE:", user.mobile)

    db.add(user)
    db.commit()
    db.refresh(user)

    print("MOBILE AFTER SAVE:", user.mobile)

    return user


# ============================================================
# Login
# ============================================================
@app.post(
    "/login",
    response_model=MessageResponse,
    tags=["Authentication"],
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    statement = select(User).where(User.email == request.email)
    user = db.scalars(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return {"message": "Login successful"}