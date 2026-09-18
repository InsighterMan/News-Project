from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.favorite_crud import is_favorite_check, add_favorite, delete_favorite, remove_all_favorite, get_favorite_list
from models.toutiao_mod import User
from schemas.favorite_sch import CheckFavorite, AddFavorite, FavoriteList
from utils.auth import get_current_token
from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

# 收藏新闻
@router.post("/add")
async def add_favorite_news(
        data: AddFavorite,
        user: User = Depends(get_current_token),
        db: AsyncSession = Depends(get_db),
):
    add_result = await add_favorite(db, user.id, data.news_id)
    return success_response(data=add_result, message="收藏成功")

# 检查新闻是否收藏
@router.get("/check")
async def check_favorite(
        news_id : int = Query(..., alias="newsId"),
        user: User = Depends(get_current_token),
        db: AsyncSession = Depends(get_db),
):
    is_favorited: bool = await is_favorite_check(db, user.id, news_id)

    # is_favorited是布尔值，无法通过model_validate进行pydantic映射，直接通过CheckFavorite将其传给前端恰好需要的"data":{"isFavorite":Bool}即可
    return success_response(message="检查收藏状态成功", data=CheckFavorite(is_favorited=is_favorited))

# 取消收藏新闻
@router.delete("/remove")
async def remove_favorite(
        news_id : int = Query(..., alias="newsId"),
        user: User = Depends(get_current_token),
        db: AsyncSession = Depends(get_db),
):
    await delete_favorite(db, user.id, news_id)

    return success_response(message="取消收藏成功")

# 获取收藏列表
@router.get("/list")
async def list_favorite(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
        user: User = Depends(get_current_token),
        db: AsyncSession = Depends(get_db),
):
    total, all_rows = await get_favorite_list(db, user.id, page, page_size)

    # 判断是否还有更多新闻
    has_more = total > page * page_size

    # 通过列表推导式将整理好的最终数据结构以字典的形式封装到列表中，准备响应给前端
    favorite_list = [
        {
            "id": news.id,
            "title": news.title,
            "description": news.description,
            "image": news.image,
            "author": news.author,
            "category_id": news.category_id,
            "views": news.views,
            "publish_time": news.publish_time,
            "fav_created_at": favorite_created_at,
            "fav_id": favorite_id,
        }
        for news, favorite_created_at, favorite_id in all_rows
    ]
    data = FavoriteList(total=total, has_more=has_more, all_rows=favorite_list)
    return success_response(data=data, message="获取收藏列表成功")

# 清空收藏列表
@router.delete("/clear")
async def clear_favorite(
        user: User = Depends(get_current_token),
        db: AsyncSession = Depends(get_db),
):
    count = await remove_all_favorite(db, user.id)
    return success_response(message=f"本次清除{count}条新闻成功")