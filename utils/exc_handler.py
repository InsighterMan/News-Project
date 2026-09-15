from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, \
    general_exception_handler


def register_exception_handlers(app):
    """
    封装全局异常处理
    """
    # 业内原则：子类（integrity_error_handler）在前，父类（sqlalchemy_error_handler）在后；具体在前，抽象（general_exception_handler）在后
    # 处理 HTTPException 异常
    app.add_exception_handler(HTTPException, http_exception_handler)
    # 处理数据库完整性约束错误
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    # 处理 SQLAlchemy 数据库错误
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    # 处理所有未捕获的异常
    app.add_exception_handler(Exception, general_exception_handler)