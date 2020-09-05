import os
from flask import current_app
from werkzeug.utils import secure_filename
from qiniu import Auth, put_file, etag
from apps.models.file import File
from apps.utils.file import Uploader
from apps.config.setting import DevelopmentConfig
#  七牛云key
access_key = DevelopmentConfig.access_key
secret_key = DevelopmentConfig.secret_key


class LocalUploader(Uploader):  # 这个是把图片保存到本地的形式

    def upload(self):
        ret = []
        self.mkdir_if_not_exists()
        site_domain = current_app.config.get('SITE_DOMAIN')\
            if current_app.config.get('SITE_DOMAIN') else 'http://127.0.0.1:5000'
        for single in self._file_storage:
            file_md5 = self._generate_md5(single.read())
            single.seek(0)
            exists = File.objects(md5=file_md5).first()
            # print(exists, single)  # <File 4> <FileStorage: 'test.png' ('image/*')>
            if exists:
                ret.append({
                    "key": single.name,
                    "id": str(exists.id),
                    "path": exists.path,
                    "url": site_domain + os.path.join(current_app.static_url_path, exists.path)
                })
            else:
                absolute_path, relative_path, real_name = self._get_store_path(single.filename)
                print(absolute_path, relative_path)  # /Users.../lin-cms-flask/app/assets..png, 2020/04/...png
                secure_filename(single.filename)  # 这个是安全获取文件名，如果想不安全获取就用file.filename
                single.save(absolute_path)  # 这个意思是 把这个文件保存到本地
                file = File.create_file(
                    name=real_name,
                    path=relative_path,
                    extension=self._get_ext(single.filename),  # single.filename: 获取文件后缀名
                    size=self._get_size(single),  
                    md5=file_md5
                )
                ret.append({
                    "key": single.name,
                    "id": file.id,
                    "path": file.path,
                    "url": site_domain + os.path.join(current_app.static_url_path, file.path)
                })
        return ret


class QiUploader(Uploader):  # 这个是将图片上传至七牛云对象存储服务器里

    def upload(self):
        ret = []
        self.mkdir_if_not_exists()
        site_domain = current_app.config.get('SITE_DOMAIN') \
            if current_app.config.get('SITE_DOMAIN') else 'http://127.0.0.1:5000'
        for single in self._file_storage:
            file_md5 = self._generate_md5(single.read())
            single.seek(0)
            exists = File.objects(md5=file_md5).first()
            # print(exists, single)  # <File 4> <FileStorage: 'test.png' ('image/*')>
            if exists:
                ret.append({
                    "key": single.name,
                    "id": str(exists.id),
                    "path": exists.path,
                    "url": exists.path
                })
                print(ret)
            else:
                absolute_path, relative_path, real_name = self._get_store_path(single.filename)
                # print(absolute_path, relative_path) /Users/lrboy/Desktop/lin-cms-flask/app/assets..png,2020/04/...png
                secure_filename(single.filename)  # 这个是安全获取文件名，如果想不安全获取就用file.filename
                single.save(absolute_path)  # 这个意思是 把这个文件保存到本地
                # 需要填写你的 Access Key 和 Secret Key， 构建鉴权对象
                q = Auth(access_key, secret_key)
                # 要上传的空间
                bucket_name = 'lrboy'
                # 上传后保存的文件名
                key = relative_path
                # 生成上传 Token，可以指定过期时间等
                token = q.upload_token(bucket_name, key, 3600)
                # 要上传文件的本地路径
                localfile = absolute_path
                # 先存进数据库一波
                blog_file = File.create_file(
                    name=real_name,
                    path=site_domain + relative_path,
                    extension=self._get_ext(single.filename),  # single.filename: 获取文件后缀名
                    size=self._get_size(single),
                    md5=file_md5,
                )
                res, info = put_file(token, key, localfile)
                if info.status_code == 200:
                    print('图片上传成功')
                    assert res['key'] == key
                    assert res['hash'] == etag(localfile)
                    print(blog_file)
                    ret.append({
                        "key": single.name,
                        "id": str(blog_file.id),
                        "path": blog_file.path,
                        "url": blog_file.path
                    })
        return ret
