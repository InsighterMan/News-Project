from fastapi import status
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import users_crud
from config.db_conf import get_db
from crud.users_crud import authenticate_user, update_user_by_token, update_user_password
from models.toutiao_mod import User
from schemas.users_sch import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdate, UserUpdatePassword
from utils.auth import get_current_token
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["users"])

# 注册模块
@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 判断用户是否存在
    exist_user = await users_crud.read_user_by_username(db, user_data.username)
    if exist_user:
        # HTTP_400_BAD_REQUEST通常用于通用的客户端传参校验失败，例如请求体缺少必填字段、JSON格式解析失败、或者常规业务参数不合规
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该用户已存在")

    # 创建用户
    user = await users_crud.create_user(db, user_data)

    # 创建token
    user_token = await users_crud.create_token(db, user.id)

    # 返回数据到前端
    response_data = UserInfoResponse.model_validate(user) # model_validate将普通Python对象（或数据库ORM对象）转换为Pydantic模型实例
    return success_response(data=UserAuthResponse(token=user_token, user_info=response_data), message="注册成功")

# 登录模块
@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    auth_user = await authenticate_user(db, user_data.username, user_data.password)

    # 判断用户名和密码状况
    if not auth_user:
        # HTTP_401_UNAUTHORIZED专用于身份认证和凭证校验失败。例如用户没有登录、缺少或Token已过期，或者修改密码时原密码输入错误
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    token = await users_crud.create_token(db, auth_user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(auth_user))
    return success_response(response_data, "登录成功")

# 获取用户信息模块
@router.get("/info")
# 通过依赖注入调用get_user_by_token函数并拿到其返回值
async def get_user_info(user: User = Depends(get_current_token)):
    return success_response(data=UserInfoResponse.model_validate(user), message="获取用户信息成功")

# 更新用户信息
@router.put("/update")
async def update_user_info(
        # FastAPI通过类型注解判定update_user并非简单URL参数，而是继承Pydantic中BaseModel的一个类，故会将它放到请求体的位置，因此判定为该参数由前端传回
        update_user: UserUpdate,
        user: User = Depends(get_current_token),
        db: AsyncSession = Depends(get_db)
):
    update_info = await update_user_by_token(db, update_user, user)
    return success_response(data=UserInfoResponse.model_validate(update_info), message="更新用户信息成功")

# 更新用户密码
@router.put("/password")
async def update_password(
        password_data: UserUpdatePassword,
        user: User = Depends(get_current_token),
        db: AsyncSession = Depends(get_db)
):
    update_info = await update_user_password(db, password_data.old_password, password_data.new_password, user)

    # 判断原密码是否相同
    if not update_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="原密码错误 请重新输入")

    return success_response(data=UserInfoResponse.model_validate(update_info), message="修改密码成功")