from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post
"""这些虚拟对象的属性使用Faker 包提供的随机信息生成器生成，可以生成看起来很逼真的姓名、电子邮件地址、句子，等等。"""


def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password="password",
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def posts(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        """随机生成文章时要为每篇文章随机指定一个用户。为此，我们使用offset() 查询过滤器。
        这个过滤器会跳过参数指定的记录数量。为了每次都得到不同的随机用户，我们先设定一
        个随机的偏移，然后调用first() 方法。"""
        u = User.query.offset(randint(0, user_count-1)).first()
        p = Post(body=fake.text(),
                 timestamp=fake.past_date(),
                 author=u)
        db.session.add(p)
    db.session.commit()
