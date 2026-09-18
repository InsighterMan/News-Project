import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Boolean
from models.toutiao_mod import User, UserToken
from schemas.users_sch import UserRequest, UserUpdate, UserUpdatePassword
from utils import security
from datetime import datetime, timedelta, timezone

# 根据用户名查询数据库
async def read_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 密码加密处理
    hashed_pwd = security.get_password_hash(user_data.password)

    user = User(username=user_data.username, password=hashed_pwd)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# 创建token
async def create_token(db: AsyncSession, user_id: int):
    # 生成token转为字符串
    token = str(uuid.uuid4())
    # 设置过期时间（当前时间（hours=8代表东八区，即北京时间） + 令牌存在时间）
    expire_time = datetime.now(timezone(timedelta(hours=8))) + timedelta(days=1)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    # 判断用户是否有token，有则更新，无则添加，
    if user_token:
        user_token.token = token
        user_token.expires_at = expire_time
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expire_time)
        db.add(user_token)

    await db.commit()
    await db.refresh(user_token)

    return token

# 验证用户
async def authenticate_user(db: AsyncSession, user_name: str, password: str):
    result = await db.execute(select(User).where(User.username == user_name))
    user = result.scalar_one_or_none()

    if not user:
        return None

    verify_pwd = security.verify_password(password, user.password)
    if not verify_pwd:
        return None

    return user

# 根据token查询用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    # 判断token是否存在和过期
    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 更新用户
async def update_user_by_token(db: AsyncSession, update_user: UserUpdate, user_data):
    # 通过model_dump将用户更新的内容转化为字典形式，利用exclude_unset只保留前端显式修改的字段，且利用exclude_none过滤掉所有值为None的字段
    update_data = update_user.model_dump(exclude_unset=True, exclude_none=True)

    # 对字典进行解包并通过setattr将更新后的值重新对应键，即user_data.key = value
    for key, value in update_data.items():
        setattr(user_data, key, value)

    await db.commit()
    await db.refresh(user_data)
    return user_data

# 修改用户密码
async def update_user_password(db: AsyncSession, old_pwd, new_pwd, user_data):
    auth_old_pwd: bool = security.verify_password(old_pwd, user_data.password)
    if not auth_old_pwd:
        return None
    hashed_new_pwd = security.get_password_hash(new_pwd)
    user_data.password = hashed_new_pwd
    await db.commit()
    await db.refresh(user_data)
    return user_data
