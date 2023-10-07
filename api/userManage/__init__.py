# -*- encoding: utf-8 -*-
'''
@Date		:2023/10/06 15:57:53
@Author		:zono
@Description:用户管理api库
1、注册
2、登录验证
'''
from fastapi import APIRouter, Depends, Body, HTTPException, status

from .registration import reg
# from .login import login_app
from .oauth_text import app1
from .login import loginUP



userManage_app = APIRouter()

# userManage_app.include_router(login_app,prefix='/login')#"登录模块2.0"
# TODO userManage_app.include_router(app1)#"验证模块（待重构）"
userManage_app.include_router(reg,prefix='/signUp'),#"注册"
userManage_app.include_router(loginUP,prefix='/loginUp'),#"注册"
