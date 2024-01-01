#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2023/12/30 23:44
@File  : __init__.py.py
'''


from configparser import ConfigParser

import os, sys, platform, glob, threading, tkinter as tk

from tkinter import filedialog, messagebox, ttk

from tkinter.ttk import Progressbar

from subprocess import Popen, PIPE, STDOUT

from urllib.request import urlretrieve, urlopen, Request

from time import sleep

from re import findall

def CF_INIT():
    ''' 初始化配置文件 '''
    cf = ConfigParser()
    if not os.path.exists('jm_ui.ini'):
        cf.add_section('current')
        cf.set('current', 'jdk_version', '')
        cf.set('current', 'jmeter_version', '')
        cf.set('current', 'jmeter_path', '')
        cf.set('current', 'jmeter_plugin_version', '')
        cf.add_section('install')
        cf.set('install', 'archive_versions', '[]')
        cf.set('install', 'mirror_versions', '[]')
        cf.add_section('installed')
        cf.set('installed', 'versions', '[]')
        cf.add_section('settings')
        cf.set('settings', 'download_urls', "['https://archive.apache.org/dist/jmeter/binaries/', " + \
                                           "'https://mirrors.aliyun.com/apache/jmeter/binaries/', " + \
                                           "'https://mirrors.tuna.tsinghua.edu.cn/apache/jmeter/binaries/']")
        cf.set('settings', 'download_path', '~\\Desktop')
        cf.set('settings', 'install_path', 'C:\\Program Files\\JMeter')

        cf.write(open('jm_ui.ini', 'w', encoding='utf-8'))
    return cf