from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.history_crud import add_history, get_history_list, remove_all_history, delete_history
from models.toutiao_mod import User
from schemas.history_sch import AddHistory, HistoryList
from utils.auth import get_current_token
from utils.response import success_response

router = APIRouter(prefix="/api/history", tags=["history"])

# 添加历史记录
@router.post("/add")
async def add_history_news(
        data: AddHistory,
        user: User = Depends(get_current_token),
        db: AsyncSession = Depends(get_db),
):
    add_result = await add_history(db, user.id, data.news_id)
    return success_response(data=add_result, message="添加历史记录成功")

# 删除历史记录
@router.delete("/delete/{history_id}")
async def remove_history(
        history_id : int,
        user: User = Depends(get_current_token),
        db: AsyncSession = Depends(get_db),
):
    await delete_history(db, user.id, history_id)

    return success_response(message="取消收藏成功")

# 获取历史记录列表
@router.get("/list")
async def list_history(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
        user: User = Depends(get_current_token),
        db: AsyncSession = Depends(get_db),
):
    total, all_rows = await get_history_list(db, user.id, page, page_size)

    # 判断是否还有更多新闻
    has_more = total > page * page_size

    # 通过列表推导式将整理好的最终数据结构以字典的形式封装到列表中，准备响应给前端
    history_list = [
        {
            "id": news.id,
            "title": news.title,
            "description": news.description,
            "image": news.image,
            "author": news.author,
            "category_id": news.category_id,
            "views": news.views,
            "publish_time": news.publish_time,
            "his_view_time": history_view_time,
            "his_id": history_id,
        }
        for news, history_view_time, history_id in all_rows
    ]
    data = HistoryList(total=total, has_more=has_more, all_rows=history_list)
    return success_response(data=data, message="获取收藏列表成功")

# 清空历史记录列表
@router.delete("/clear")
async def clear_history(
        user: User = Depends(get_current_token),
        db: AsyncSession = Depends(get_db),
):
    count = await remove_all_history(db, user.id)
    return success_response(message=f"本次清除{count}条新闻成功")