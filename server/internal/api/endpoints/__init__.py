# from internal.app.users import auth_backend, fastapi_users
# from internal.schemas.user import UserCreate, UserRead, UserUpdate
from . import example, metricks
from fastapi import APIRouter


router = APIRouter()
router.include_router(
    example.router,
    prefix="/root",
    tags=["root"],
)
router.include_router(
    metricks.router,
    prefix="/chat",
    tags=["chat"],
)
# router.include_router(
#     user.router,
#     prefix="/auth",
#     tags=["auth"],
# )
# router.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth/jwt",
#     tags=["auth"]
# )
# router.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )
# router.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )
# router.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
    
# )
# router.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"],
# )