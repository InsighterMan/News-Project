from typing import Optional
import datetime
import enum
from sqlalchemy import Enum
from sqlalchemy import ForeignKeyConstraint, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class UserGender(str, enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'


class NewsCategory(Base):
    __tablename__ = 'news_category'
    __table_args__ = (
        Index('name_UNIQUE', 'name', unique=True),
        {'comment': '新闻分类表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, comment='分类ID')
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='分类名称')
    sort_order: Mapped[int] = mapped_column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='排序顺序')
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间')

    news: Mapped[list['News']] = relationship('News', back_populates='category')


class News(Base):
    __tablename__ = 'news'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['news_category.id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_news_category'),
        Index('fk_news_category_idx', 'category_id'),
        Index('idx_publish_time', 'publish_time'),
        {'comment': '新闻表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, comment='新闻ID')
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment='新闻标题')
    content: Mapped[str] = mapped_column(Text, nullable=False, comment='新闻内容')
    category_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, comment='分类ID')
    views: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, server_default=text("'0'"), comment='浏览量')
    publish_time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='发布时间')
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间')
    description: Mapped[Optional[str]] = mapped_column(String(500), comment='新闻简介')
    image: Mapped[Optional[str]] = mapped_column(String(255), comment='封面图片URL')
    author: Mapped[Optional[str]] = mapped_column(String(50), comment='作者')

    category: Mapped['NewsCategory'] = relationship('NewsCategory', back_populates='news')
    favorite: Mapped[list['Favorite']] = relationship('Favorite', back_populates='news')
    history: Mapped[list['History']] = relationship('History', back_populates='news')
    related_news_news: Mapped[list['RelatedNews']] = relationship('RelatedNews', foreign_keys='[RelatedNews.news_id]', back_populates='news')
    related_news_related_news: Mapped[list['RelatedNews']] = relationship('RelatedNews', foreign_keys='[RelatedNews.related_news_id]', back_populates='related_news')


class RelatedNews(Base):
    __tablename__ = 'related_news'
    __table_args__ = (
        ForeignKeyConstraint(['news_id'], ['news.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_related_news_news'),
        ForeignKeyConstraint(['related_news_id'], ['news.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_related_news_related'),
        Index('fk_related_news_news_idx', 'news_id'),
        Index('fk_related_news_related_idx', 'related_news_id'),
        Index('news_related_unique', 'news_id', 'related_news_id', unique=True),
        {'comment': '相关新闻关联表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, comment='关联ID')
    news_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, comment='新闻ID')
    related_news_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, comment='相关新闻ID')
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')

    news: Mapped['News'] = relationship('News', foreign_keys=[news_id], back_populates='related_news_news')
    related_news: Mapped['News'] = relationship('News', foreign_keys=[related_news_id], back_populates='related_news_related_news')


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        Index('phone_UNIQUE', 'phone', unique=True),
        Index('username_UNIQUE', 'username', unique=True),
        {'comment': '用户信息表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, comment='用户ID')
    username: Mapped[str] = mapped_column(String(50), nullable=False, comment='用户名')
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment='密码（加密存储）')
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False,
                                                          server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间')
    nickname: Mapped[Optional[str]] = mapped_column(String(50), comment='昵称')
    avatar: Mapped[Optional[str]] = mapped_column(String(255), comment='头像URL')
    gender: Mapped[Optional[UserGender]] = mapped_column(
        Enum(UserGender, values_callable=lambda cls: [member.value for member in cls]),
        server_default=text("'unknown'"), comment='性别')
    bio: Mapped[Optional[str]] = mapped_column(String(500), comment='个人简介')
    phone: Mapped[Optional[str]] = mapped_column(String(20), comment='手机号')

    ai_chat: Mapped[list['AiChat']] = relationship('AiChat', back_populates='user')
    user_token: Mapped[list['UserToken']] = relationship('UserToken', back_populates='user')
    favorite: Mapped[list['Favorite']] = relationship('Favorite', back_populates='user')
    history: Mapped[list['History']] = relationship('History', back_populates='user')


class UserToken(Base):
    __tablename__ = 'user_token'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE', onupdate='CASCADE',
                             name='fk_user_token_user'),
        Index('fk_user_token_user_idx', 'user_id'),
        Index('token_UNIQUE', 'token', unique=True),
        {'comment': '用户令牌表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, comment='令牌ID')
    user_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, comment='用户ID')
    token: Mapped[str] = mapped_column(String(255), nullable=False, comment='令牌值')
    expires_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, comment='过期时间')
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False,
                                                          server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')

    user: Mapped['User'] = relationship('User', back_populates='user_token')


class AiChat(Base):
    __tablename__ = 'ai_chat'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_ai_chat_user'),
        Index('fk_ai_chat_user_idx', 'user_id'),
        Index('idx_created_at', 'created_at'),
        {'comment': 'AI聊天记录表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True,
                                    comment='聊天记录ID')
    user_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, comment='用户ID')
    message: Mapped[str] = mapped_column(Text, nullable=False, comment='用户消息')
    response: Mapped[str] = mapped_column(Text, nullable=False, comment='AI回复')
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False,
                                                          server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')

    user: Mapped['User'] = relationship('User', back_populates='ai_chat')


class Favorite(Base):
    __tablename__ = 'favorite'
    __table_args__ = (
        ForeignKeyConstraint(['news_id'], ['news.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_favorite_news'),
        ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_favorite_user'),
        Index('fk_favorite_news_idx', 'news_id'),
        Index('fk_favorite_user_idx', 'user_id'),
        Index('user_news_unique', 'user_id', 'news_id', unique=True),
        {'comment': '收藏表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, comment='收藏ID')
    user_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, comment='用户ID')
    news_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, comment='新闻ID')
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False,
                                                          server_default=text('CURRENT_TIMESTAMP'), comment='收藏时间')

    news: Mapped['News'] = relationship('News', back_populates='favorite')
    user: Mapped['User'] = relationship('User', back_populates='favorite')


class History(Base):
    __tablename__ = 'history'
    __table_args__ = (
        ForeignKeyConstraint(['news_id'], ['news.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_history_news'),
        ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_history_user'),
        Index('fk_history_news_idx', 'news_id'),
        Index('fk_history_user_idx', 'user_id'),
        Index('idx_view_time', 'view_time'),
        {'comment': '浏览历史表'}
    )

    id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), primary_key=True, autoincrement=True, comment='历史ID')
    user_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, comment='用户ID')
    news_id: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), nullable=False, comment='新闻ID')
    view_time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False,
                                                         server_default=text('CURRENT_TIMESTAMP'), comment='浏览时间')

    news: Mapped['News'] = relationship('News', back_populates='history')
    user: Mapped['User'] = relationship('User', back_populates='history')