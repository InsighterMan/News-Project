from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.news_sch import NewsItemBase


# 定义收藏类
class AddFavorite(BaseModel):
    # 通过alias确保在向前端输出时自动转化为前端能够识别的驼峰式写法
    news_id: int = Field(..., alias="newsId")

# 定义检查收藏类
class CheckFavorite(BaseModel):
    is_favorited: bool = Field(..., alias="isFavorite")

    # 开启populate_by_name后，允许在向CheckFavorite传参时同时可以使用别名或原名
    model_config = ConfigDict(populate_by_name=True)

# 定义收藏模型类
class FavoriteItemBase(NewsItemBase):
    fav_id: int = Field(..., alias="favoriteId")
    fav_created_at: datetime = Field(alias="favoriteTime")

    # 开启from_attributes后，保证pydantic能够识别非字典类型数据
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

# 定义列表接口相应类
class FavoriteList(BaseModel):
    # 让Pydantic识别到all_rows字段必须是一个列表，并且列表里的每一个元素都必须严格符合FavoriteItemBase类的结构和校验规则
    all_rows: list[FavoriteItemBase] = Field(alias="list")
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
