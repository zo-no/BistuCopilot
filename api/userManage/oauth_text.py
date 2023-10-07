# Todo 待重构：把函数包装起来
# /api/v1/token
# -*- encoding: utf-8 -*-
'''
@Date		:2023/10/04 21:46:26
@Author		:zono
@Description:登录模块
'''

from datetime import datetime, timedelta
from typing import Union,Optional

from fastapi import Depends,APIRouter, HTTPException, status#TODO 使用Query来限制输入
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


# ----------------------配置和数据库-----------------------------------------
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$g6.vyA2TNkCMHiWzCmoEVOzfiftVdX.2ICyycxYfe5UfyOoRnvkP6",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

#TODO 把这些集成到config中
SECRET_KEY = "efb8d310a2e46e859a8e2f196ad25ff41916c90828999d64d50699f4f6cae93c"
ALGORITHM = "HS256"#算法变量
ACCESS_TOKEN_EXPIRE_MINUTES = 30#过期时间


# ---------------------------------------------------------------
app1 = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")#使用bcrypt算法对密码加密
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")#用户校验地址


# ---------------------------------------------------------------
class Token(BaseModel):
    """
    @description  :
    返回给用户的Token
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str

# -----------------------------密码处理函数----------------------------------

def get_password_hash(password: str):
    """
    @description  :
    对密码加密
    @param  :
    -------
    @Returns  :
    str
    """
    return pwd_context.hash(password)

# -----------------------检验用户----------------------------------------
def verify_password(plain_password:str, hashed_password:str) -> bool:
    """
    @description  :
    密码校验函数
    @param  :
    -------
    @Returns  :
    bool
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    """
    @description  :
    检验用户的username是否在库
    @param  :
    -------
    @Returns  :
    -------
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def authenticate_user(fake_db, username: str, password: str):
    """
    @description  :
    调用检验密码和检验用户名，有则返回
    @param  :
    -------
    @Returns  :
    -------
    """
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# -------------------检验成功后返回token--------------------------------------------
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    @description  :
    创建Token函数
    @param  :
    -------
    @Returns  :
    -------
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta#加上过期时间
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)#TODO默认过期时间，集成到config中
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)#入值：字符、key、算法->出值：Token
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    @description  :
    校验Token，验证用户，并获取当前用户
    @param  :
    -------
    @Returns  :
    -------
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据，可能是登录过期",#TODO 日后完善
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])#与encode反过来
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# QUER 函数同名时，先调用哪一个？ 
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    @description  :
    检验用户权限
    @param  :
    -------
    @Returns  :
    -------
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app1.post("/token",response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    @description  :
    登录接口，并返回Token
    @param  :
    -------
    @Returns  :
    access_token
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="账号或密码错误",
                             headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app1.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    @description  :
    一般用户
    @param  :
    -------
    @Returns  :
    -------
    """
    return current_user


@app1.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """
    @description  :
    活跃用户
    @param  :
    -------
    @Returns  :
    -------
    """
    return [{"item_id": "Foo", "owner": current_user.username}]

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('try:app',host="0.0.0.0", port=5000,reload=True)