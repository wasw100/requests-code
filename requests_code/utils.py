# -*- coding: utf-8 -*-
import os
import os.path
from flask import current_app


def get_filepath(name):
    """根据名字获取文件所在的路径"""
    return os.path.join(
        current_app.base_dir,
        'code/{}'.format(name)
    )


def delete_file(filepath):
    # 只能前缀是base_path的文件
    print('delete file:', filepath)
    if not filepath.startswith('{}/code'.format(current_app.base_dir)):
        return
    if os.path.isfile(filepath):
        # 如果文件存在, 删除
        os.remove(filepath)


def delete_code(name):
    """删除py, pyc文件"""
    path1 = get_filepath(name)
    path2 = '{}c'.format(path1)
    delete_file(path1)
    delete_file(path2)
