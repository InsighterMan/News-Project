from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import users_crud


# 根据token查询用户，返回用户
async def get_current_token(
        db: AsyncSession = Depends(get_db),
        authorization: str = Header(..., alias="Authorization")
):
    # 前端请求头的认证格式为Authorization:Bearer <Token>，因此不光要起别名，而且这里仅要拿Token，不需要Bearer
    token = authorization.replace("Bearer ", "")
    user = await users_crud.get_user_by_token(db, token)

    # 防御型代码，防止出现get_user_by_token对数据库操作时，由于数据库中没有添加外键约束或脏写造成UserToken存在内容但User中已删除该用户的现象
    if not user:
        # 无论是get_user_by_token中token不存在或过期，还是token有效但返回的用户为none，都能够在此抛出异常
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="请检查用户是否存在或令牌是否无效")

    return user