# -*- encoding: utf-8 -*-
'''
@Date		:2023/10/04 22:21:31
@Author		:zono
@Description:规范后端与数据库的交互格式，数据库模型。    对应Djongo的orm
'''

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date,DateTime,func
from sqlalchemy.orm import relationship

from database.sqlite import Base


class User(Base):
    """
    @description  :
    用户表
    """
    #表名
    __tablename__ = "users"
    #字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)#用户id,自增长
    username = Column(String, unique=True, index=True,nullable=False)# 用户名不可空、注解
    hashed_password = Column(String)#密码
    is_active = Column(Boolean, default=True)#权限

    # items = relationship("Item", back_populates="owner")#关联表Item

    # created_at = Column(DateTime,server_default=func.now())
    # updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now())#只在更新时调用

    # __mapper_args__ = {
    #     'order_by': id.desc()# 按id倒序排列
    # }

    # def __repr__(self):
    #     return f"<User {self.id}>"


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")


# TODO 将想好的表创建

# TODO 解决表的实时变动
