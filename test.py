from tortoise import Tortoise, fields
from tortoise.models import Model
import asyncio  # 使用 asyncio 替代 run_async

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    age = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"

    def __str__(self):
        return f"User {self.name}, 年龄: {self.age}"

async def init_db():
    # 初始化数据库连接
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['__main__']}
    )
    # 创建表
    await Tortoise.generate_schemas()

async def test_operations():
    # 创建用户
    user = await User.create(name="张三", age=25)
    print(f"创建用户: {user}")

    # 查询用户
    user_from_db = await User.get(id=user.id)
    print(f"查询用户: {user_from_db}")

    # 更新用户
    await User.filter(id=user.id).update(age=26)
    user_updated = await User.get(id=user.id)
    print(f"更新后的用户: {user_updated}")

    # 查询所有用户
    all_users = await User.all()
    print("所有用户:")
    for u in all_users:
        print(f"- {u}")

    # 删除用户
    await user.delete()
    count = await User.all().count()
    print(f"删除后的用户数量: {count}")

async def main():
    await init_db()
    await test_operations()
    await Tortoise.close_connections()

if __name__ == "__main__":
    # 使用 asyncio.run 替代 run_async
    asyncio.run(main())