# from mongoengine import *
# from apps import db

# rbac 权限， 测试权限数据，功能后期在进行编写

USER_ROLE = {
    300: '超级管理员',
    100: '管理员',
    0: '普通用户'
}

# 超级管理员拥有的权限
SUPER = ['编辑用户', '添加用户', '查询用户', '删除用户', '添加标签', '编辑标签', '删除标签', '添加分类', '删除分类', '修改分类',
         '查询日志', '搜索日志', '删除评论', '修改评论', '删除图书', '修改图书']

# 管理员拥有的权限...
ADMIN = ['查询用户', '添加用户', '添加分类', '编辑分类', '添加标签', '编辑标签', '添加图书', '编辑图书', '删除图书', '查询日志',
         '搜索日志', '查看评论', '编辑评论']

# 普通用户拥有的权限
USER = ['添加图书', '编辑图书', '删除图书', '查询日志', '搜索日志', '查看评论']

# ...后续还有什么权限自己添加自己写


# class Permissions(db.DynamicDocument):
#     module = StringField()  # 权限名
#     permission = StringField()  # 权限信息
#     value = IntField(primary_key=True)    # 权限值
#     meta = {
#         'abstract': True,
#         'allow_inheritance': True,
#         'index_cls': False
#     }
#
#     @staticmethod
#     def create_permission():
#         permission = Permissions()
#         pass
def append_permission(role):
    permissions = []
    roles = {}
    if role == 300:
        arr = [{'module': USER_ROLE[role], 'permission': info} for info in SUPER]
        roles[USER_ROLE[role]] = arr
        permissions.append(roles)
        return permissions
    if role == 100:
        arr = [{'module': USER_ROLE[role], 'permission': info} for info in ADMIN]
        roles[USER_ROLE[role]] = arr
        permissions.append(roles)
        return permissions
    if role == 0:
        arr = [{'module': USER_ROLE[role], 'permission': info} for info in USER]
        roles[USER_ROLE[role]] = arr
        permissions.append(roles)
        return permissions




