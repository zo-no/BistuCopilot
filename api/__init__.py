# -*- coding:utf-8 -*-
"""
@Created on : 2022/4/22 22:02
@Author: binkuolo
@Des: api路由导出区
"""
from fastapi import APIRouter

from .api import api_test

from .backgroundTasks import Back_app
from .userManage import userManage_app
api_router = APIRouter(prefix="/api/v1",
                    # dependencies=[Depends(***)]#该路由下所有接口的依赖
                    # response={200,{"msg":"good"}}#作用到所有接口的响应
                       )


# api_router.include_router(api_test,prefix='/test',tags=["学习测试模块"])    
api_router.include_router(Back_app,tags=["后台测试模块"])
api_router.include_router(userManage_app,prefix='/userManage',tags=["用户管理模块"])

# cookie和Cookie 、Path 、Query是兄弟类，
# 你可以使用定义 Query, Path 和 Cookie 参数一样的方法定义 Header 参数。
# 响应模型类response_model用list https://fastapi.tiangolo.com/zh/tutorial/response-model/
