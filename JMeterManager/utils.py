#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2023/12/31 1:17
@File  : utils.py
'''

from JMeterManager import os, \
                        platform, \
                        glob, \
                        threading, \
                        Popen, \
                        PIPE, \
                        STDOUT, \
                        sleep, \
                        findall, \
                        Request, \
                        urlopen, \
                        CF_INIT

'''
获取系统名称、（多线程）获取系统已经安装的所有JMeter版本
'''

_SYSTEM_NAME_ = platform.system()  # Windows、Linux、Darwin、Java...

lock = threading.Lock()

cf = CF_INIT()

def GET_SYSTEM_DEVICES_LIST() -> list:
    ''' 获取windows系统所有盘符 '''
    return [i.replace(' ', '').replace('\n', '')
            for i in os.popen('wmic logicaldisk get deviceid |findstr :').readlines()
            if i.replace(' ', '').replace('\n', '') != '']

def finder_thread(path: str):
    lock.acquire()   # 锁住资源，防止多线程同时操作合并列表
    path_list.extend(glob.glob(path, recursive=True))
    lock.release()  # 释放资源

def GET_JMETER_PATH_LIST() -> list:
    ''' 获取JMeter路径列表 '''
    global path_list
    path_list = []
    if _SYSTEM_NAME_ == 'Windows':
        for device in GET_SYSTEM_DEVICES_LIST():
            t = threading.Thread(target=finder_thread, args=(f'{device}\\**\\jmeter.bat',))
            t.start()
            t.join()
    else:
        path_list.extend(glob.glob('**/jmeter.sh', recursive=True))
    return path_list

def SET_JMETER_INSTALLED_VERSION():
    ''' 获取基本存在所有JMeter安装版本 '''
    jmeter_version_list = set()
    for file_full_path in GET_JMETER_PATH_LIST():
        file_path = os.path.dirname(file_full_path)
        CMD = f'cd /d "{file_path}" && jmeter -v' if _SYSTEM_NAME_ == 'Windows' else f'cd {file_path} && jmeter -v'
        try:
            Popen(CMD, shell=True, stdout=PIPE, stderr=STDOUT, encoding='utf-8')
            _timeout_ = 10
            while not os.path.exists('{file_path}/jmeter.log') and _timeout_ >= 0: sleep(0.5); _timeout_ -= 0.5
            with open(f'{file_path}/jmeter.log', 'r') as f: data = f.readlines(); f.close()
            jmeter_version_list.add(str(findall(': Version (.+)\n$', [d for d in data if ': Version ' in d][0])[0]).strip())
        except PermissionError:
            raise PermissionError('没有足够的权限执行命令!')
    cf.set('installed', 'versions', str(list(jmeter_version_list)))
    cf.write(open('jm_ui.ini', 'w', encoding='utf-8'))

def SET_JMETER_INSTALL_VERSIONS():
    ''' 解析URL获取可下载的所有版本 '''
    cf.read('jm_ui.ini', encoding='utf-8')
    urls_url = cf.get('settings', 'download_urls')
    for url in eval(urls_url):
        HtmlResponse = urlopen(
                            Request(
                                url,
                                headers={
                                    'User-Agent':
                                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '+\
                                        'Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
                                })
                            ).read().decode('utf-8')
        versions = findall('<a href="apache-jmeter-(.+).zip"', HtmlResponse)

        cf.set('install', 'archive_versions', str(versions)) \
                if url.startswith('https://archive.apache.org') \
                else cf.set('install', 'mirror_versions', str(versions))
        cf.write(open('jm_ui.ini', 'w', encoding='utf-8'))
