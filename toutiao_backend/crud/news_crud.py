from sqlalchemy.ext.asyncio import AsyncSession
from models.toutiao_mod import NewsCategory, News
from sqlalchemy import select, func, update


# 创建NewCategory表的CRUD
# 查询新闻分类
async def read_news_category(db: AsyncSession, skip, limit):
  result = await db.execute(select(NewsCategory).order_by(NewsCategory.sort_order).offset(skip).limit(limit))
  return result.scalars().all()

# 创建News表的CRUD
# 查询指定分类下新闻
async def read_news_list(db: AsyncSession, category_id, skip, limit):
  result = await db.execute(select(News).where(News.category_id == category_id).order_by(News.publish_time.desc()).offset(skip).limit(limit))
  return result.scalars().all()

# 查询指定分类下新闻数量
async def read_news_count(db: AsyncSession, category_id):
  result = await db.execute(select(func.count(News.id)).where(News.category_id == category_id))
  return result.scalar_one()  # 仅返回一个结果，否则报错

# 查询新闻详情
async def read_news_detail(db: AsyncSession, news_id):
  result = await db.execute(select(News).where(News.id == news_id))
  return result.scalar_one_or_none()

# 更新新闻浏览量
async def update_news_view(db : AsyncSession, news_id):
  result = update(News).where(News.id == news_id).values(views=News.views + 1)
  await db.execute(result)

# 查询相关新闻
async def read_related_news(db : AsyncSession, category_id, news_id, limit = 5):
  result = await db.execute(select(News).where(News.category_id == category_id, News.id != news_id).order_by(News.views.desc(), News.publish_time.desc()).limit(limit))
  related_news = result.scalars().all()
  # 列表推导式 只获取需要的相关新闻的数据
  return [
          {
            "id": related_news_format.id,
            "title": related_news_format.title,
            "content": related_news_format.content,
            "image": related_news_format.image,
            "author": related_news_format.author,
            "publishTime": related_news_format.publish_time,
            "categoryId": related_news_format.category_id,
            "views": related_news_format.views,
            }
            for related_news_format in related_news
  ]
