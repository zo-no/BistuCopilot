# -*- encoding: utf-8 -*-
'''
@Date		:2023/09/26 19:15:11
@Author		:zono
@Description:主文件，程序于这里运行
'''
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from config import settings
from core import  events,Router

#TODO暂时的调用办法


application = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    authorization=settings.PROJECT_AUTHOR,
    email=settings.PROJECT_EMAIL,
    swagger_ui_oauth2_redirect_url=settings.SWAGGER_UI_OAUTH2_REDIRECT_URL,
)


# ----------------------------事件监听-----------------------------------
application.add_event_handler("startup", events.startup(application))
application.add_event_handler("shutdown", events.stopping(application))



# --------------------------静态文件-------------------------------------
# application.mount(path='/home', app=StaticFiles(directory="static/templates"), name="static")#TODO 与config.py联动
# ---------------------------------------------------------------
from fastapi.templating import Jinja2Templates
from fastapi import Request
templates = Jinja2Templates(directory="static/templates")#QUER 这个路径配置很奇怪，好像python文件的配置路径是以app未主，一切都是以app为基准

@application.get("/",tags=['模板引擎'])
def index(request: Request):
    """
    @description  :
    前后端不分离的模板引擎
    @param  :
    -------
    @Returns  :
    -------
    """
    return templates.TemplateResponse("index.html", {"request": request})


# --------------------------中间件-------------------------------------
import time
from fastapi import Request



@application.middleware("http")#QUER这样写的话中间件会作用到该app的所有接口中
async def add_process_time_header(request: Request, call_next):
    """
    @description  :
    计算响应时间
    @param  :
    -------
    @Returns  :
    -------
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# ------------------------路由---------------------------------------
application.include_router(Router.router)# 导入路由


# -------------------------跨域设置--------------------------------------
# TODO 导入配置项中
#bug  这个有问题
# from fastapi.middleware.cors import CORSMiddleware
# application.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"#想加哪个加哪个
#                    ],
#     allow_credentials=True,#允许使用证书
#     allow_method=["*"],#允许跨域方法
#     allow_headers=["*"]#允许的请求头
# )


# -------------------------其他--------------------------------------


if __name__ == '__main__':
    uvicorn.run('app:application',host="0.0.0.0", port=5000,reload=True)