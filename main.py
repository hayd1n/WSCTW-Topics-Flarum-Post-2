import logging
# 設置logging格式
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

import os
from dotenv import load_dotenv
load_dotenv()

import sys
sys.path.append("./wdasec-announcement-crawler")
import wdasec_announcement_crawler as wdasec

import json

from pytablewriter import MarkdownTableWriter

from datetime import datetime 

from pyflarum import FlarumUser
from pyflarum.flarum.core.posts import PreparedPost

USER = FlarumUser(
    forum_url = os.environ["forum_url"],
    username_or_email = os.environ["username"],
    password = os.environ["password"]
)

def _newPost(discussion, content: str):
    """
    發布新文章

    Args:
        discussion ([type]): 討論版
        content (str): 文章內容

    Returns:
        [type]: Post
    """
    post = PreparedPost(user=USER, discussion=discussion, content=content)
    posted = post.post()
    return posted

def _editPost(post, content: str):
    """
    編輯文章

    Args:
        post ([type]): 文章
        content (str): 文章內容

    Returns:
        [type]: Post
    """
    edit = PreparedPost(user=USER, content=content)
    edited = post.edit(edit)
    return edited

def _generateTable(files: list) -> str:
    """
    產生Markdown表格

    Args:
        files (list): 題目檔案表

    Returns:
        str: Markdown表格
    """
    headers = ["名稱", "檔案"]
    matrix = list()
    for file in files:
        in_files = file['files']
        in_files_list = ["[" + in_file['type'] + "](" + in_file['url'] + ")" for in_file in in_files]
        data = [file['name']]
        data += in_files_list
        matrix.append(data)
    writer = MarkdownTableWriter(headers=headers, value_matrix=matrix)
    return str(writer.dumps())

def _saveLog(files: list):
    """
    保存紀錄檔

    Args:
        files (list): 題目檔案表
    """
    with open("log.json", 'w+') as obj:
        json.dump(files, obj)

def _loadLog() -> list:
    """
    加載紀錄檔

    Returns:
        list: 題目檔案表
    """
    try:
        with open("log.json", 'r') as obj:
            data = json.load(obj)
    except:
        data = None
    return data

def _diffLog(newLog, oldLog) -> list:
    """
    比較題目檔案表差別

    Args:
        newLog ([type]): 新列表
        oldLog ([type]): 舊列表

    Returns:
        list: 差異列表
    """
    diff_log = list()
    for files in newLog:
        new_file = True
        for old_files in oldLog:
            if files == old_files:
                new_file = False
        if new_file: diff_log.append(files)
    return diff_log

if __name__ == "__main__":
    print("技能競賽題目自動推送Flarum V1.0 By CRT_HAO")

    announcement = None
    try:
        logging.info("開始爬取題目...")
        announcement = wdasec.announcement(os.environ["announcement_url"])
    except Exception as e:
        logging.error(e)

    if announcement:
        logging.info("爬取成功！")
        files = announcement['files']

        log = _loadLog()
        diff_files = list()
        if(log):
            logging.info("偵測到log.json，自動比對差別")
            diff_files = _diffLog(files, log)
        logging.info("保存log.jso")
        _saveLog(files)

        table = _generateTable(announcement['files'])
        print(table)

        content = "### 本文章長期更新，有興趣的用戶請關注本文章\n"
        content += ">**更新時間：" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "**\n"
        content += "**題目來源：[連結](" + os.environ["announcement_url"] + ")**\n\n"
        content += table

        logging.info("獲取討論版...")
        discussion = USER.get_discussion_by_id(os.environ["discussion_id"])

        logging.info("編輯文章...")
        first_post = discussion.get_posts()[0]
        _editPost(first_post, content)

        if(len(diff_files) != 0):
            logging.info("發現題目更新，發布新文章...")
            table = _generateTable(diff_files)

            content = ">發現以下題目更新\n\n"
            content += table
            _newPost(discussion, content)

    else:
        logging.error("爬取錯誤，放棄操作。")