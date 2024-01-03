#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2023/12/31 1:17
@File  : utils.py
'''

from __init__ import os, \
                        JM_INI_PATH, \
                        platform, \
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

cf = CF_INIT()

def GET_SYSTEM_DEVICES_LIST() -> list:
    ''' 获取windows系统所有盘符 '''
    return [i.replace(' ', '').replace('\n', '')
            for i in os.popen('wmic logicaldisk get deviceid |findstr :').readlines()
            if i.replace(' ', '').replace('\n', '') != '']

def finder_thread(path: str, path_list: list, version_list: list) -> None:
    ''' 多线程查找文件 '''
    # path_list.extend(glob.glob(path, recursive=True))
    v = ''
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename == 'jmeter.bat':
                try:
                    CMD = f'cd /d "{dirpath}" && jmeter -v' if _SYSTEM_NAME_ == 'Windows' else f'cd {dirpath} && jmeter -v'
                    Popen(CMD, stdout=PIPE, shell=True,  stderr=STDOUT,encoding='utf-8')
                    _timeout_ = 2
                    while not os.path.exists(f'{dirpath}/jmeter.log') and _timeout_ >= 0: sleep(0.5); _timeout_ -= 0.5
                    if os.path.exists(f'{dirpath}/jmeter.log'):
                        with open(f'{dirpath}/jmeter.log', 'r') as f: data = f.readlines(); f.close()
                        v = str(findall(': Version (.+)\n$', [d for d in data if ': Version ' in d][0])[0]).strip()
                        version_list.append(v)
                    path_list.append(os.path.join(dirpath, filename))
                except Exception as e:
                    pass

def SET_JMETER_INSTALLED_VERSION(status) -> None:
    ''' 在指定安装路径下获取JMeter的列表 '''
    # status.set('正在获取已安装版本...')
    path_list = []
    version_list = []
    cf.read(JM_INI_PATH, encoding='utf-8')
    _t = threading.Thread(target=finder_thread, args=(cf.get('settings', 'install_path'), path_list, version_list))
    # _t.setDaemon(True)
    _t.start()
    _t.join()
    cf.set('installed', 'jmeter_paths', str(path_list))
    cf.set('installed', 'versions', str(version_list))
    cf.write(open(JM_INI_PATH, 'w', encoding='utf-8'))
    # status.set('安装版本检测完成!')

def SET_JMETER_INSTALL_VERSIONS(status):
    ''' 解析URL获取可下载的所有版本 '''
    status.set('正在获取全部版本号...')
    cf.read(JM_INI_PATH, encoding='utf-8')
    urls_url = cf.get('settings', 'download_urls')
    for url in eval(urls_url):
        try:
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
            # versions.sort(reverse=True)
            cf.set('install', 'archive_versions', str(versions)) \
                    if url.startswith('https://archive.apache.org') \
                    else cf.set('install', 'mirror_versions', str(versions))
            cf.write(open(JM_INI_PATH, 'w', encoding='utf-8'))
            status.set('版本号获取已完成!')
        except Exception as e:
            status.set(f'获取版本号失败! {e}')
            break