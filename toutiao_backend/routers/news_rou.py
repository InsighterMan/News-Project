from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import news_crud

# 统一路由前缀prefix和分组tags
router = APIRouter(prefix="/api/news", tags=["news"])

# 定义新闻分类的模块化路由
@router.get("/categories")
async def get_news_category(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    category = await news_crud.read_news_category(db, skip, limit)
    return {
        "code": 200,
        "message": "success",
        "data": category,
    }

# 定义新闻列表的模块化路由
@router.get("/list")
async def get_news_list(
        category_id: int = Query(alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", le=100),
        db: AsyncSession = Depends(get_db)
):
    skip = (page - 1) * page_size
    news_list = await news_crud.read_news_list(db, category_id, skip, page_size)
    news_count = await news_crud.read_news_count(db, category_id)
    has_more = skip + page_size < news_count
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": news_list,
            "total": news_count,
            "hasMore": has_more,
        }
    }

# 定义新闻详情的模块化路由
@router.get("/detail")
async def get_news_detail(
        db: AsyncSession = Depends(get_db),
        news_id: int = Query(alias="id"),
):
    # 查询新闻详情
    news_detail = await news_crud.read_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="the news detail does not found")

    # 更新新闻浏览量
    await news_crud.update_news_view(db, news_detail.id)

    # 查询相关新闻
    related_news = await news_crud.read_related_news(db, news_detail.category_id, news_detail.id)

    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news,
        }
    }