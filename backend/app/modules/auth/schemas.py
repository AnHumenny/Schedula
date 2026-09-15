from pydantic import BaseModel, EmailStr, Field, model_validator


class LoginRequest(BaseModel):
    """Request schema for user login by username or email and password."""
    username: str | None = Field(None, description="Username of the user")
    email: EmailStr | None = Field(None, description="Email address of the user")
    password: str = Field(..., description="Password for the user account")

    @model_validator(mode="after")
    def check_identifier(self):
        """Ensure at least one of username or email is provided."""
        if not self.username and not self.email:
            raise ValueError("username or email is required")
        return self


class TokenResponse(BaseModel):
    """Response schema containing the access token."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Type of the authentication token")
