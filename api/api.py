# -*- encoding: utf-8 -*-
'''
@Date		:2023/10/03 16:08:12
@Author		:zono
@Description:实验文件
'''

from fastapi import APIRouter,Form,File, UploadFile,Depends
api_test = APIRouter(prefix="/test" )    

# @api_test.post("/form",name="表单提交")
# async def form_post(form: str=Form(...)):
#     """
#     需要python-multipart；
#     ---------
#     """
#     return {"form": form}
    
# #-------------------------- 文件上传------------------------------

# @api_test.post("/upload",name="文件上传")
# async def upload(file: bytes = File(...)):
#     """
#     @description  :
#     小文件上传,并返回大小
#     加上list就是多文件上传
#     """
#     return {"file": len(file)}

# @api_test.post("/uploadfile",name="文件上传")
# async def uploadfile(files: list[UploadFile] = File(...)):
#     """
#     @description  :
#     先入内存后入磁盘
#     @param  :
#     -------
#     @Returns  :
#     -------
#     """
#     return {"file": len(files)}
# ---------------------------------------------------------------
from typing import Union

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@api_test.get("/users/me", name="用户信息测试")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
