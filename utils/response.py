from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(data = None, message: str = "success"):
    content = {"code": 200, "message": message, "data": data}
    # jsonable_encoder将除基础数据以外的复杂对象如ORM对象、日期和时间、Pydantic模型实例等转化为python能够识别的内容
    # JSONResponse将处理过的数据包装成FastAPI标准的HTTP响应对象返回给客户端
    return JSONResponse(content=jsonable_encoder(content))