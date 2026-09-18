from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

# 用于接收前端发来的请求体
class UserRequest(BaseModel):
    username: str
    password: str

# user_info对应的类 = 基础类UserInfoBase + Info类UserInfoResponse
# 定义了用户的基础字段（昵称、头像、性别、简介）
class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

# 定义了用户的业务属性字段
class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # model_config必须写在Pydantic模型类内部，控制当前这个模型类行为的全局开关，而不干扰其他模型类
    # Pydantic模型类负责API接口的数据格式，决定请求体该传什么、响应给前端该长什么样，与SQLAlchemy模型类不能混为一谈
    model_config = ConfigDict(
        # 开启后Pydantic能直接从数据库ORM对象（实例）中读取属性，并进行转换和校验
        from_attributes=True,
    )

# 完整的data数据类型 + 校验
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(alias="userInfo")

    model_config = ConfigDict(
        # 开启后允许在后端使用下划线式进行传参，无需因为要跟前端对齐，而在后端使用驼峰式别名传参
        populate_by_name=True,
        from_attributes=True,
    )

# 定义更新用户信息的模型类
class UserUpdate(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None

# 定义修改密码的模型类
class UserUpdatePassword(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(..., min_length=6, alias="newPassword", description="新密码")

    model_config = ConfigDict(populate_by_name=True)


