#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2023/12/30 23:44
@File  : __init__.py
'''

from zipfile import ZipFile

from configparser import ConfigParser

import os, sys, platform, threading, tkinter as tk, ctypes

from tkinter import filedialog, ttk

from tkinter.ttk import Progressbar

from subprocess import Popen, PIPE, STDOUT

from urllib.request import urlretrieve, urlopen, Request

from time import sleep

from re import findall

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

FAVICON_PATH = os.path.join(CUR_DIR, 'image/favicon.ico')

BG_IMAGE_PATH = os.path.join(CUR_DIR, 'image/bg.png')

JM_INI_PATH = os.path.join(CUR_DIR, 'jm_ui.ini')

def CF_INIT():
    ''' 初始化配置文件 '''
    cf = ConfigParser()
    if not os.path.exists(JM_INI_PATH):
        cf.add_section('current')
        cf.set('current', 'jdk_version', '')
        cf.set('current', 'jmeter_version', '')
        cf.set('current', 'jmeter_home', '')
        cf.set('current', 'jmeter_plugin_version', '')
        cf.add_section('install')
        cf.set('install', 'archive_versions', '[]')
        cf.set('install', 'mirror_versions', '[]')
        cf.add_section('installed')
        cf.set('installed', 'jmeter_paths', '[]')
        cf.set('installed', 'versions', '[]')
        cf.add_section('settings')
        cf.set('settings', 'download_urls', "['https://archive.apache.org/dist/jmeter/binaries/', " + \
                                           "'https://mirrors.aliyun.com/apache/jmeter/binaries/', " + \
                                           "'https://mirrors.tuna.tsinghua.edu.cn/apache/jmeter/binaries/']")
        cf.set('settings', 'download_path', os.path.expanduser('~/Downloads/'))
        cf.set('settings', 'install_path', os.path.expanduser('~/Desktop/'))

        cf.write(open(JM_INI_PATH, 'w', encoding='utf-8'))
    return cf
