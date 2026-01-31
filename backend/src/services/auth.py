from sqlmodel import Session, select
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from src.models.user import User, UserCreate

# Load environment variables
load_dotenv()

# Password hashing context - using argon2 instead of bcrypt to avoid issues
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        # Bcrypt has a 72 byte password length limit
        # Truncate if needed to prevent errors
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            # Take the first 72 bytes and decode back to string
            password = password_bytes[:72].decode('utf-8', errors='ignore')
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if not user or not AuthService.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_current_user_from_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return None
            return payload
        except JWTError:
            return None

    @staticmethod
    def create_user(session: Session, user_create: UserCreate):
        # Hash the password
        hashed_password = AuthService.get_password_hash(user_create.password)

        # Create the user object
        db_user = User(
            email=user_create.email,
            name=user_create.name,
            hashed_password=hashed_password
        )

        # Add to session and commit
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user