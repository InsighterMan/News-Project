from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.news_sch import NewsItemBase


# 定义添加历史记录类
class AddHistory(BaseModel):
    # 通过alias确保在向前端输出时自动转化为前端能够识别的驼峰式写法
    news_id: int = Field(..., alias="newsId")


# 定义历史记录模型类
class HistoryItemBase(NewsItemBase):
    his_id: int = Field(..., alias="historyId")
    his_view_time: datetime = Field(alias="historyTime")

    # 开启from_attributes后，保证pydantic能够识别非字典类型数据
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

# 定义列表接口相应类
class HistoryList(BaseModel):
    # 让Pydantic识别到all_rows字段必须是一个列表，并且列表里的每一个元素都必须严格符合HistoryItemBase类的结构和校验规则
    all_rows: list[HistoryItemBase] = Field(alias="list")
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
