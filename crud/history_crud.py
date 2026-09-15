from sqlalchemy.ext.asyncio import AsyncSession

from models.toutiao_mod import News, History
from sqlalchemy import select, delete, func


# 添加历史记录
async def add_history(db: AsyncSession, user_id: int, news_id:  int):

    # 判断该新闻是否已经添加到浏览列表
    query = await db.execute(select(History).where(History.news_id == news_id, History.user_id == user_id))
    existed_history = query.scalar_one_or_none()

    if existed_history:
        return existed_history

    # 添加该新闻到浏览列表
    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history

# 删除历史记录
async def delete_history(db: AsyncSession, user_id: int, news_id: int):
    query = await db.execute(select(History).where(History.user_id == user_id, History.news_id == news_id))
    result = query.scalar_one_or_none()

    # 判断该历史记录是否存在
    if result:
        await db.delete(result)
        await db.commit()

# 获取新闻总量及新闻浏览记录列表
async def get_history_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int =10,
):
    offset = (page - 1) * page_size

    # 获取新闻总量
    count_result = await db.execute(select(func.count(History.id)).where(History.user_id == user_id))
    total: int = count_result.scalar_one()

    # 获取历史记录列表
    # 通过join连接主表News和联表History，可实现根据History.user_id进行where筛选以及根据History.view_time进行倒序展示
    history_list = await db.execute(
                                select(News, History.view_time.label("his_view_time"), History.id.label("his_id"))
                               .join(History, History.news_id == News.id)
                               .where(History.user_id == user_id)
                               .order_by(History.view_time.desc())
                               .offset(offset)
                               .limit(page_size)
                               )

    # 通过all将News和History联表的数据以元组的形式封装到列表中，如[(News.id, News.content, ..., History.view_time, History.id)]
    all_rows = history_list.all()

    return total, all_rows

# 清空历史记录列表
async def remove_all_history(db: AsyncSession, user_id: int):
    query = delete(History).where(History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount or 0
