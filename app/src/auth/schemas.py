from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """Schema base para usuário"""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)


class UserCreate(UserBase):
    """Schema para criação de usuário"""

    password: str = Field(..., min_length=6, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validar força da senha"""
        if len(v) < 6:
            raise ValueError("Senha deve ter no mínimo 6 caracteres")
        if not any(char.isdigit() for char in v):
            raise ValueError("Senha deve conter pelo menos um número")
        if not any(char.isalpha() for char in v):
            raise ValueError("Senha deve conter pelo menos uma letra")
        return v


class UserUpdate(BaseModel):
    """Schema para atualização de usuário"""

    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """Schema de usuário no banco de dados"""

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """Schema de resposta de usuário"""

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema de token de autenticação"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema de dados do token"""

    user_id: Optional[int] = None
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema de requisição de login"""

    username: str = Field(..., description="Username ou email do usuário")
    password: str = Field(..., min_length=6)


class PasswordChange(BaseModel):
    """Schema para alteração de senha"""

    current_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str, values) -> str:
        """Validar nova senha"""
        if len(v) < 6:
            raise ValueError("Nova senha deve ter no mínimo 6 caracteres")
        if not any(char.isdigit() for char in v):
            raise ValueError("Nova senha deve conter pelo menos um número")
        if not any(char.isalpha() for char in v):
            raise ValueError("Nova senha deve conter pelo menos uma letra")
        return v
