"""
Firebase Authentication Router
Handles login and token verification
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from services.firebase_auth import verify_firebase_token, get_user_role, set_user_role

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer(auto_error=False)


class LoginRequest(BaseModel):
    """Login request - client sends Firebase ID token"""
    id_token: str


class SetRoleRequest(BaseModel):
    """Set user role request"""
    id_token: str
    role: str  # 'department' or 'institution'


class LoginResponse(BaseModel):
    """Login response"""
    success: bool
    user: Dict[str, Any]
    role: str
    message: str


class VerifyResponse(BaseModel):
    """Token verification response"""
    valid: bool
    user: Optional[Dict[str, Any]] = None
    role: Optional[str] = None
    error: Optional[str] = None


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Login endpoint - verifies Firebase ID token and returns user info.
    
    Client should:
    1. Authenticate with Firebase Auth (Email or Google Sign-In)
    2. Get Firebase ID token
    3. Send token to this endpoint
    
    Returns user info and role.
    """
    try:
        # Verify Firebase token
        user_info = verify_firebase_token(request.id_token)
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        
        # Get user role
        role = get_user_role(user_info)

        # Persist user in local DB if not already present
        uid = user_info.get("uid")
        email = user_info.get("email")
        if uid and email:
            try:
                from config.database import get_db, close_db, User as DBUser
                db = get_db()
                try:
                    db_user = db.query(DBUser).filter(DBUser.id == uid).first()
                    if db_user:
                        if db_user.role:
                            role = db_user.role
                        db_user.email = email
                        if user_info.get("name"):
                            db_user.name = user_info.get("name")
                        db.commit()
                    else:
                        db_user = DBUser(
                            id=uid,
                            email=email,
                            name=user_info.get("name"),
                            role=role
                        )
                        db.add(db_user)
                        db.commit()
                finally:
                    close_db(db)
            except Exception as dbe:
                logger.warning(f"Failed to upsert user in DB: {dbe}")
        
        logger.info(f"User logged in: {user_info.get('email')} (role: {role})")
        
        return LoginResponse(
            success=True,
            user={
                "uid": user_info.get("uid"),
                "email": user_info.get("email"),
                "name": user_info.get("name"),
                "picture": user_info.get("picture"),
                "email_verified": user_info.get("email_verified", False),
            },
            role=role,
            message="Login successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.get("/verify", response_model=VerifyResponse)
async def verify_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """
    Verify Firebase ID token.
    
    Returns user info if token is valid.
    """
    if not credentials:
        return VerifyResponse(
            valid=False,
            error="No authentication token provided"
        )
    
    try:
        user_info = verify_firebase_token(credentials.credentials)
        
        if not user_info:
            return VerifyResponse(
                valid=False,
                error="Invalid token"
            )
        
        role = get_user_role(user_info)
        
        return VerifyResponse(
            valid=True,
            user={
                "uid": user_info.get("uid"),
                "email": user_info.get("email"),
                "name": user_info.get("name"),
                "picture": user_info.get("picture"),
            },
            role=role
        )
        
    except HTTPException as e:
        return VerifyResponse(
            valid=False,
            error=e.detail
        )
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        return VerifyResponse(
            valid=False,
            error="Token verification failed"
        )


@router.post("/set-role")
async def set_role(request: SetRoleRequest):
    """
    Set user role via Firebase custom claims.
    This endpoint should be called after user sign up to set their role.
    """
    try:
        # Verify Firebase token
        user_info = verify_firebase_token(request.id_token)
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        
        # Validate role
        if request.role not in ['department', 'college']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role. Must be 'department' or 'college'"
            )
        
        # Set custom claims and persist in DB
        uid = user_info.get("uid")
        set_user_role(uid, request.role)
        
        logger.info(f"Role '{request.role}' set for user {uid} ({user_info.get('email')})")
        
        return {
            "success": True,
            "message": f"Role set to {request.role}",
            "role": request.role
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Set role error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set user role"
        )


@router.get("/me")
async def get_current_user_info(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """
    Get current authenticated user info.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    try:
        user_info = verify_firebase_token(credentials.credentials)
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        role = get_user_role(user_info)
        
        return {
            "user": {
                "uid": user_info.get("uid"),
                "email": user_info.get("email"),
                "name": user_info.get("name"),
                "picture": user_info.get("picture"),
                "email_verified": user_info.get("email_verified", False),
            },
            "role": role
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user info error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user info"
        )

