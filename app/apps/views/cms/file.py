from flask import Blueprint, jsonify, request

from apps.core.qiniu_file import QiUploader
from apps.core.token_auth import login_required

file_api = Blueprint('file', __name__)


@file_api.route('/file', methods=['POST'])
@login_required
def post_file():
    files = request.files
    uploader = QiUploader(files)
    ret = uploader.upload()
    return jsonify(ret)
