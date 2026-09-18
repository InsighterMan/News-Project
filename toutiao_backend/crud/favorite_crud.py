from sqlalchemy.ext.asyncio import AsyncSession

from models.toutiao_mod import Favorite, News
from sqlalchemy import select, delete, func


# 添加收藏
async def add_favorite(db: AsyncSession, user_id: int, news_id: int):
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

# 查询是否收藏
async def is_favorite_check(db: AsyncSession, user_id, news_id: int) -> bool:
    result = await db.execute(select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id))
    return result.scalar_one_or_none() is not None

# 取消收藏
async def delete_favorite(db: AsyncSession, user_id: int, news_id: int):
    query = await db.execute(select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id))
    result = query.scalar_one_or_none()

    # 判断是否收藏
    if result:
        await db.delete(result)
        await db.commit()

    return True

# 获取新闻总量及收藏新闻列表
async def get_favorite_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int =10,
):
    offset = (page - 1) * page_size

    # 获取新闻总量
    count_result = await db.execute(select(func.count(Favorite.id)).where(Favorite.user_id == user_id))
    total: int = count_result.scalar_one()

    # 获取收藏新闻列表
    # 通过join连接主表News和联表Favorite，可实现根据Favorite.user_id进行where筛选以及根据Favorite.created_at进行倒序展示
    favorite_list = await db.execute(
                                select(News, Favorite.created_at.label("fav_created_at"), Favorite.id.label("fav_id"))
                               .join(Favorite, Favorite.news_id == News.id)
                               .where(Favorite.user_id == user_id)
                               .order_by(Favorite.created_at.desc())
                               .offset(offset)
                               .limit(page_size)
                               )

    # 通过all将News和Favorite联表的数据以元组的形式封装到列表中，如[(News.id, News.content, ..., Favorite.created_at, Favorite.id)]
    all_rows = favorite_list.all()

    return total, all_rows

# 清空收藏列表
async def remove_all_favorite(db: AsyncSession, user_id: int):
    query = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount or 0
