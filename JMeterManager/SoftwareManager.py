#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2024/1/10 1:07
@File  : SoftwareManager.py
'''


from __init__ import ttk, \
    ZipFile, \
    threading, \
    Popen, \
    PIPE, \
    STDOUT, \
    Progressbar, \
    tk, \
    CF_INIT, \
    urlretrieve, \
    filedialog, \
    os, \
    FAVICON_PATH, \
    JM_INI_PATH, \
    os, \
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

from utils import SET_JMETER_INSTALLED_VERSION, SET_JMETER_INSTALL_VERSIONS, _SYSTEM_NAME_
from __version__ import __version__

class Utils(object):
    ''' 工具类 '''
    def __init__(self):
        pass

    @staticmethod
    def SYSTEM_NAME() -> str:
        ''' 获取系统名称 '''
        return platform.system()  # Windows、Linux、Darwin、Java...

    def finder_thread(self, path: str, path_list: list, version_list: list) -> None:
        ''' 多线程查找文件 '''
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename == 'jmeter.bat':
                    try:
                        CMD = f'cd /d "{dirpath}" && jmeter -v' if _SYSTEM_NAME_ == 'Windows' else f'cd {dirpath} && jmeter -v'
                        Popen(CMD, stdout=PIPE, shell=True,  stderr=STDOUT, encoding='utf-8')
                        _timeout_ = 2
                        while not os.path.exists(f'{dirpath}/jmeter.log') and _timeout_ >= 0: sleep(0.5); _timeout_ -= 0.5
                        if os.path.exists(f'{dirpath}/jmeter.log'):
                            with open(f'{dirpath}/jmeter.log', 'r') as f: data = f.readlines(); f.close()
                            v = str(findall(': Version (.+)\n$', [d for d in data if ': Version ' in d][0])[0]).strip()
                            version_list.append(v)
                        path_list.append(os.path.join(dirpath, filename))
                    except Exception as e:
                        pass

    def SET_JMETER_INSTALLED_VERSION(self, status) -> None:
        ''' 在指定安装路径下获取JMeter的列表 '''
        status.set('正在获取已安装版本...')
        path_list = []
        version_list = []
        cf.read(JM_INI_PATH, encoding='utf-8')
        _t = threading.Thread(target=self.finder_thread, args=(cf.get('settings', 'install_path'), path_list, version_list))
        # _t.setDaemon(True)
        _t.start()
        _t.join()
        cf.set('installed', 'jmeter_paths', str(path_list))
        cf.set('installed', 'versions', str(version_list))
        cf.write(open(JM_INI_PATH, 'w', encoding='utf-8'))
        status.set('安装版本检测完成!')

    def SET_JMETER_INSTALL_VERSIONS(self, status):
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
                                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '+ \
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


class SettingsUI(object):
    ''' 设置类
    [current]
    jdk_version =
    jmeter_version =
    jmeter_home =
    jmeter_plugin_version =

    [install]
    archive_versions = ['2.10', '2.11', '2.12', '2.13', '2.6', '2.7', '2.8', '2.9', '3.0', '3.1', '3.2', '3.3', '4.0', '5.0', '5.1.1', '5.1', '5.2.1', '5.2', '5.3', '5.4.1', '5.4.2', '5.4.3', '5.4', '5.5', '5.6.1', '5.6.2', '5.6.3', '5.6']
    mirror_versions = ['5.5', '5.6.1', '5.6.2', '5.6.3', '5.6']

    [installed]
    jmeter_paths = ['D:/jmeter\\apache-jmeter-5.5\\bin\\jmeter.bat', 'D:/jmeter\\apache-jmeter-5.6\\bin\\jmeter.bat', 'D:/jmeter\\apache-jmeter-5.6.1\\bin\\jmeter.bat', 'D:/jmeter\\apache-jmeter-5.6.2\\bin\\jmeter.bat', 'D:/jmeter\\apache-jmeter-5.6.3\\bin\\jmeter.bat']
    versions = ['5.5', '5.6', '5.6.1', '5.6.2', '5.6.3']

    [settings]
    download_urls = ['https://archive.apache.org/dist/jmeter/binaries/', 'https://mirrors.aliyun.com/apache/jmeter/binaries/', 'https://mirrors.tuna.tsinghua.edu.cn/apache/jmeter/binaries/']
    download_path = C:\Users\Administrator/Downloads/
    install_path = D:/jmeter
    '''
    def __init__(self):
        self.software_urls = {
            'python': ['https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe', 'https://www.python.org/ftp/python/3.8.0/python-3.8.0-embed-amd64.zip'],
            'openjdk': ['https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_windows-x64_bin.zip', 'https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_windows-x64_bin.zip'],
            'jmeter': ['https://archive.apache.org/dist/jmeter/binaries/', 'https://mirrors.aliyun.com/apache/jmeter/binaries/', 'https://mirrors.tuna.tsinghua.edu.cn/apache/jmeter/binaries/'],
        }

    @property
    def install_versions(self):
        return self._install_versions

    @install_versions.setter
    def install_versions(self, versions: list):
        versions.remove('')
        versions = list(set(versions))
        versions.sort(reverse=True)
        self._install_versions = versions

    @property
    def installed_paths(self):
        return self._installed_paths

    @installed_paths.setter
    def installed_paths(self, paths: list):
        paths.remove('')
        paths = list(set(paths))
        self._installed_paths = paths

    @property
    def installed_versions(self):
        return self._installed_versions

    @installed_versions.setter
    def installed_versions(self, versions: list):
        versions.remove('')
        versions = list(set(versions))
        self._installed_versions = versions

    @property
    def download_urls(self):
        return self._download_urls

    @download_urls.setter
    def download_urls(self, urls: list):
        urls.remove('')
        urls = list(set(urls))
        self._download_urls = urls

    @property
    def download_path(self):
        return self._download_path

    @download_path.setter
    def download_path(self, path: str):
        self._download_path = path

    @property
    def install_path(self):
        return self._install_path

    @install_path.setter
    def install_path(self, path: str):
        self._install_path = path


class JMeterManagerUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title_text = f"SoftwareManager·@xiaobaiTser v{__version__}      "
        self.title(self.title_text)
        self.iconbitmap(FAVICON_PATH)
        # 窗口设置为自适应
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.resizable(False, False)
        self.check_software_status = tk.StringVar()
        self.check_software_status.set("Python")
        self.operate_message_text = tk.StringVar()
        self.settings_message_text = self.operate_message_text
        self.create_widgets()
        self.settings_init()
        self.run()
        self.after(500, self.refresh_title)
        self.mainloop()

    def settings_init(self):
        ''' 初始化 '''
        self.cf = CF_INIT()
        self.cf.read(JM_INI_PATH, encoding='utf-8')
        self.settings = SettingsUI()
        self.settings.install_versions = self.cf.get('install', 'archive_versions').split(',')
        self.settings.installed_paths = self.cf.get('installed', 'jmeter_paths').split(',')
        self.settings.installed_versions = self.cf.get('installed', 'versions').split(',')
        self.settings.download_urls = self.cf.get('settings', 'download_urls').split(',')
        self.settings.download_path = self.cf.get('settings', 'download_path')
        self.settings.install_path = self.cf.get('settings', 'install_path')

    def run(self):
        ''' 初始化 '''
        self.check_install_list()
        self.refresh_install_version_data()
        self.check_installed_list()
        self.refresh_installed_version_data()
        self.download_lock = 1
        self.remove_lock = 1
        # 监控关闭窗口事件，防止卡线程
        self.protocol('WM_DELETE_WINDOW', self.window_close)

    def check_install_list(self):
        '''  获取可安装的版本号列表 '''
        _t1 = threading.Thread(target=SET_JMETER_INSTALL_VERSIONS, args=(self.operate_message_text,))
        _t1.setDaemon(True)
        _t1.start()

    def check_installed_list(self):
        '''  获取已安装的版本号列表 '''
        _t2 = threading.Thread(target=SET_JMETER_INSTALLED_VERSION, args=(self.operate_message_text,))
        _t2.setDaemon(True)
        _t2.start()

    def window_close(self):
        self.destroy()

    def create_widgets(self):
        '''
        界面介绍：
            两个选项卡：操作页与设置页
            操作页：选择需要安装的版本号下拉框、下载按钮、进度条、提示信息
            设置页：选择镜像站、下载路径、安装路径以配置文件的形式存储在~目录下的jm_ui.ini文件
        :return:
        '''
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")
        self.operate = ttk.Frame(self.tab_control, style='TFrame')
        self.settings = ttk.Frame(self.tab_control, style='TFrame')
        self.tab_control.add(self.operate, text="操 作", )# padding=10, image=PhotoImage(file=BG_IMAGE_PATH))
        self.tab_control.add(self.settings, text="设 置", )# padding=10, image=PhotoImage(file=BG_IMAGE_PATH))
        self.tab_control.pack(expand=1, fill="both")
        self.create_operate()
        self.create_settings()

    def create_operate(self):
        ''' 操作页 '''
        # 设置多行Frame
        software_manager_frame = tk.Frame(self.operate, height=20)
        software_manager_frame.pack()
        row_1_frame = tk.Frame(self.operate, height=20)
        row_1_frame.pack()
        row_2_frame = tk.Frame(self.operate, height=20)
        row_2_frame.pack()
        row_3_frame = tk.Frame(self.operate, height=20)
        row_3_frame.pack()
        row_4_frame = tk.Frame(self.operate, height=20)
        row_4_frame.pack()

        # software_manager_frame
        sm_left_frame = tk.Frame(software_manager_frame, width=100)
        sm_left_frame.grid(row=0, column=0, padx=5, pady=10)
        sm_center_frame = tk.Frame(software_manager_frame, width=100)
        sm_center_frame.grid(row=0, column=1, padx=5, pady=10)
        sm_right_frame = tk.Frame(software_manager_frame, width=100)
        sm_right_frame.grid(row=0, column=2, padx=5, pady=10)

        # python_label = tk.Label(sm_left_frame, text="Python")
        # python_label.grid(row=0, column=0, padx=5, pady=10)
        tk.Radiobutton(sm_left_frame, variable=self.check_software_status,
                       text="Python", value="Python",
                       command=self.check_software).pack()
        tk.Radiobutton(sm_center_frame, variable=self.check_software_status,
                       text="OpenJDK", value="OpenJDK",
                       command=self.check_software).pack()
        tk.Radiobutton(sm_right_frame, variable=self.check_software_status,
                       text="JMeter", value="JMeter",
                       command=self.check_software).pack()

        # row_1_frame
        self.operate_install_label = tk.Label(row_1_frame, text="可安装版本：")
        self.operate_install_label.grid(row=0, column=0, padx=5, pady=10)
        self.operate_install_version = tk.StringVar()
        self.operate_install_version.set("未选择...")

        # 可安装版本随着下载地址的改变而变化
        self.install_versions = eval(self.cf.get('install', 'archive_versions'))
        self.install_versions.sort(reverse=True)
        self.operate_install_version_list = ttk.Combobox(row_1_frame,
                                                         values=self.install_versions,
                                                         textvariable=self.operate_install_version,
                                                         postcommand=self.refresh_install_version_data,
                                                         width=28)
        self.operate_install_version_list.grid(row=0, column=1, padx=5, pady=10)
        self.operate_download_button = tk.Button(
            row_1_frame,
            text="下   载",
            command=self.download_jmeter,
            width=15,
            bg="green",
            fg="white")
        self.operate_download_button.grid(row=0, column=2, padx=5, pady=10)

        # row_2_frame
        self.operate_installed_label = tk.Label(row_2_frame, text="已安装版本：")
        self.operate_installed_label.grid(row=1, column=0, padx=5, pady=10)
        self.operate_installed_version = tk.StringVar()
        self.operate_installed_version.set("未选择...")
        self.operate_installed_version_list = ttk.Combobox(
            row_2_frame,
            values=eval(self.cf.get('installed', 'versions')),
            textvariable=self.operate_installed_version,
            postcommand=self.refresh_installed_version_data,
            width=28)
        self.operate_installed_version_list.grid(row=1, column=1, padx=5, pady=10)
        self.operate_remove_button = tk.Button(
            row_2_frame,
            text="卸   载",
            command=self.remove_jmeter,
            width=15,
            bg="white",
            fg="red",
            # state="disabled"
        )
        self.operate_remove_button.grid(row=1, column=2, padx=5, pady=10)

        # row_3_frame
        self.operate_progressbar = Progressbar(row_3_frame, orient="horizontal", length=400, mode="determinate")
        self.operate_progressbar.grid(row=0, column=0, padx=5, pady=10)
        self.operate_progressbar_proportion = tk.StringVar()
        self.operate_progressbar_proportion.set("0%")
        self.operate_progressbar_proportion_label = tk.Label(
            row_3_frame,
            textvariable=self.operate_progressbar_proportion)
        self.operate_progressbar_proportion_label.grid(row=0, column=1, padx=5, pady=10)

        # row_4_frame
        self.operate_message_text_label = tk.Label(row_4_frame, textvariable=self.operate_message_text, fg="red")
        self.operate_message_text_label.pack(fill="x", padx=5, pady=10)

    def create_settings(self):
        # 设置多行Frame
        row_1_frame = tk.Frame(self.settings, height=20)
        row_1_frame.pack()
        row_2_frame = tk.Frame(self.settings, height=20)
        row_2_frame.pack()
        row_3_frame = tk.Frame(self.settings, height=20)
        row_3_frame.pack()
        row_4_frame = tk.Frame(self.settings, height=20)
        row_4_frame.pack()
        row_5_frame = tk.Frame(self.settings, height=20)
        row_5_frame.pack()

        self.cf.read(JM_INI_PATH, encoding='utf-8')

        # row_1_frame:镜像
        self.settings_mirror_label = tk.Label(row_1_frame, text="镜像站：")
        self.settings_mirror_label.grid(row=0, column=0, padx=10, pady=10)
        self.settings_mirror_url = tk.StringVar()
        self.settings_mirror_url.set(eval(self.cf.get('settings', 'download_urls'))[0])
        self.cf.read(JM_INI_PATH, encoding='utf-8')
        self.settings_mirror_url_list = ttk.Combobox(row_1_frame,
                                                     values=eval(self.cf.get('settings', 'download_urls')),
                                                     textvariable=self.settings_mirror_url,
                                                     width=35,
                                                     postcommand=self.refresh_mirror_url_data,
                                                     state="readonly")
        self.settings_mirror_url_list.grid(row=0, column=1, padx=5, pady=10)

        # row_2_frame:下载路径
        self.settings_download_path_label = tk.Label(row_2_frame, text="下载路径：")
        self.settings_download_path_label.grid(row=0, column=0, padx=5, pady=10)
        self.settings_download_path = tk.StringVar()
        self.settings_download_path.set(self.cf.get('settings', 'download_path'))
        self.settings_download_path_entry = tk.Entry(
            row_2_frame,
            textvariable=self.settings_download_path,
            width=25,
            fg='black')
        self.settings_download_path_entry.grid(row=0, column=1, padx=5, pady=10)
        self.settings_download_path_entry.bind("<Return>", self.choose_download_path_return)
        self.settings_download_path_entry.bind("<FocusIn>", self.choose_download_path_focusin)
        self.settings_download_path_entry.bind("<FocusOut>", self.choose_download_path_focusout)

        self.settings_download = tk.Button(row_2_frame, text="选择路径", command=self.choose_download_path, width=10)
        self.settings_download.grid(row=0, column=2, padx=5, pady=10)

        # row_3_frame:安装路径
        self.settings_install_path_label = tk.Label(row_3_frame, text="安装路径：")
        self.settings_install_path_label.grid(row=0, column=0, padx=5, pady=10)
        self.settings_install_path = tk.StringVar()
        self.settings_install_path.set(self.cf.get('settings', 'install_path'))
        self.settings_install_path_entry = tk.Entry(
            row_3_frame,
            textvariable=self.settings_install_path,
            width=25,
            fg='black')
        self.settings_install_path_entry.grid(row=0, column=1, padx=5, pady=10)
        self.settings_install_path_entry.bind("<Return>", self.choose_install_path_return)
        self.settings_install_path_entry.bind("<FocusIn>", self.choose_install_path_focusin)
        self.settings_install_path_entry.bind("<FocusOut>", self.choose_install_path_focusout)

        self.settings_install_button = tk.Button(row_3_frame, text="选择路径", command=self.choose_install_path, width=10)
        self.settings_install_button.grid(row=0, column=2, padx=5, pady=10)

        # row_4_frame:状态信息
        self.settings_message_text.set("")
        self.settings_message_text_label = tk.Label(
            row_4_frame,
            textvariable=self.settings_message_text,
            fg="red")
        self.settings_message_text_label.pack(side="bottom")

    def check_software(self):
        ''' 选择软件 '''
        print(self.check_software_status.get())

    def refresh_title(self):
        ''' 循环修改标题内容 '''
        # while True:
        self.title_text = self.title_text[1:] + self.title_text[0:1]
        self.title(self.title_text)
        self.after(500, self.refresh_title)

    # @main_requires_admin
    def set_system_environment(self,
                               env_name: str = '',
                               env_path: str = '',
                               add_path: bool = True,
                               end_path: str = '/bin'):
        ''' 设置系统环境，windows使用winreg,linux使用/etc/profile '''
        env_name = env_name.upper().strip()
        if _SYSTEM_NAME_ == "Windows":
            if env_name:
                Popen(f'setx {env_name} "{env_path}"', stdout=PIPE, stderr=STDOUT, shell=False, encoding='utf-8')
            if add_path:
                CMD = f'setx Path %Path%;"{env_path}{end_path}"' if end_path else f'setx Path %Path%;"{env_path}"'
                Popen(CMD, stdout=PIPE, stderr=STDOUT, shell=False, encoding='utf-8')
        else:
            # 添加环境变量到/etc/profile并执行source命令
            if env_name:
                with open(f'/etc/profile', 'a', encoding='utf-8') as f:
                    f.write(f'\nexport {env_name}={env_path}\n')
                    f.flush()
                    f.close()
            if add_path:
                env_value = f'export PATH=$PATH:${env_name}{end_path}' if env_name else f'export PATH=$PATH:{env_path}'
                with open(f'/etc/profile', 'a', encoding='utf-8') as f:
                    f.write(f'\n{env_value}\n')
                    f.flush()
                    f.close()
            Popen(f'source /etc/profile',
                  shell=True,
                  stdout=PIPE,
                  stderr=STDOUT,
                  encoding='utf-8'
                  )

        self.operate_message_text.set(f"【{self.operate_install_version.get()}】环境变量设置成功!")

    def download_thread(self):
        ''' 下载线程 '''
        _version = self.operate_install_version.get()
        if not eval(self.cf.get('installed', 'versions')): self.check_installed_list()
        if _version in ["未选择...", '']: self.operate_message_text.set("请选择版本号!")
        elif _version in eval(self.cf.get('installed', 'versions')): self.operate_message_text.set("版本已安装!")
        else:
            urlretrieve(self.settings_mirror_url.get() +
                        f'/apache-jmeter-{self.operate_install_version.get()}.zip',
                        f'{self.settings_download_path.get()}/apache-jmeter-{self.operate_install_version.get()}.zip',
                        self.download_progress)
            # 更新状态信息
            self.operate_message_text_label.config(fg="green")
            self.settings_message_text_label.config(fg="green")
            self.operate_message_text.set("下载完成!")

            # 解压下载的压缩包到指定目录
            ZipFile(f'{self.settings_download_path.get()}/apache-jmeter-{self.operate_install_version.get()}.zip'). \
                extractall(self.settings_install_path.get())
            self.operate_message_text.set("解压完成!")

            # 删除下载的压缩包
            os.remove(f'{self.settings_download_path.get()}/apache-jmeter-{self.operate_install_version.get()}.zip')
            self.operate_message_text.set("删除压缩包成功!")

            # 更新已安装列表
            self.cf.read(JM_INI_PATH, encoding='utf-8')
            old_versions = eval(self.cf.get('installed', 'versions'))
            new_versions = old_versions.append(self.operate_install_version.get()) if old_versions else [self.operate_install_version.get()]
            if new_versions: new_versions.sort(reverse=True)
            self.cf.set('installed', 'versions', str(new_versions))
            self.cf.write(open(JM_INI_PATH, 'w', encoding='utf-8'))

            # 将默认语言改为中文(只有第一次安装的需要设置)
            JMETER_PROPERTIES_PATH = f'{self.settings_install_path.get()}/apache-jmeter-{self.operate_install_version.get()}/bin/jmeter.properties'
            if os.path.exists(JMETER_PROPERTIES_PATH):
                Popen(f'echo language=zh_CN>>{JMETER_PROPERTIES_PATH}', stdout=PIPE, shell=True)

        # 设置永久系统环境变量（windows使用winreg，其他系统使用直接写入/ect/profile和source命令）
        self.set_system_environment(
            env_name='JMETER_HOME',
            env_path=f'{self.settings_install_path.get()}/apache-jmeter-{self.operate_install_version.get()}',
            add_path=True,
            end_path='/bin'
        )

        # 在已安装列表中添加刚刚安装的版本号
        self.check_installed_list()
        self.refresh_installed_version_data()

        # 更新当前版本为新安装版本
        cmd_result = [v for v in Popen('java -version', shell=True, stdout=PIPE, stderr=STDOUT, encoding='utf-8').stdout.readlines() if 'version' in v][0].split(' ')
        jdk_version = [v for v in cmd_result if '.' in v][0]
        self.cf.set('current', 'jdk_version', jdk_version)
        self.cf.set('current', 'jmeter_version', self.operate_install_version.get())
        self.cf.set('current', 'jmeter_home', f'{self.settings_install_path.get()}/apache-jmeter-{self.operate_install_version.get()}')
        self.cf.write(open(JM_INI_PATH, 'w', encoding='utf-8'))
        self.download_lock = 1

    def download_jmeter(self):
        if self.download_lock:
            self.download_lock = 0
            ''' 基于镜像URL下载JMeter '''
            if self.operate_install_version.get() in ["未选择...", '']:
                self.operate_message_text.set("操作 >> 请选择版本号!")
            elif self.settings_mirror_url.get() in ["未选择...", '']:
                self.operate_message_text.set("设置 >> 请选择镜像站!")
            elif self.settings_download_path.get() in ["未选择...", '']:
                self.operate_message_text.set("设置 >> 请选择下载路径!")
            elif self.settings_install_path.get() in ["未选择...", '']:
                self.operate_message_text.set("设置 >> 请选择安装路径!")
            else:
                _t5 = threading.Thread(target=self.download_thread)
                _t5.setDaemon(True)
                _t5.start()
        else:
            self.operate_message_text.set("正在下载中!")

    def download_progress(self, block_num, block_size, total_size):
        ''' 下载进度条 '''
        self.operate_progressbar['maximum'] = total_size
        self.operate_progressbar['value'] = block_num * block_size
        self.operate_progressbar_proportion.set(str(round(block_num * block_size / total_size * 100)) + "%")
        self.operate_message_text_label.config(fg="green")
        self.operate_message_text.set("下载中...")

    # 删除文件夹及其所有内容
    def delete_folder(self, path):
        dir_list = []
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:

                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    dir_list.append(os.path.join(root, dir))
            for dir in dir_list:
                try:
                    os.rmdir(dir)
                except:
                    dir_list.append(dir)
            os.rmdir(path)
            self.remove_lock = 1

    def remove_thread(self):
        '''  卸载JMeter '''
        version = self.operate_installed_version.get()
        if version in ["未选择...", '']:
            self.operate_message_text.set("操作 >> 请选择版本号再卸载!")
        else:
            self.operate_message_text_label.config(fg="red")
            self.operate_message_text.set("正在卸载...")
            try:
                remove_jmeter_path = eval(self.cf.get('installed', 'jmeter_paths'))[eval(self.cf.get('installed', 'versions')).index(version)]
                if os.path.exists(remove_jmeter_path):
                    delete_dir = os.path.dirname(os.path.dirname(remove_jmeter_path))
                    self.delete_folder(path=delete_dir)
                if not os.path.exists(remove_jmeter_path):
                    # 卸载后更新已下载列表
                    installed_versions = eval(self.cf.get('installed', 'versions'))
                    if installed_versions: installed_versions.remove(self.operate_installed_version.get())
                    self.cf.set('installed', 'versions', str(installed_versions))
                    self.cf.write(open(JM_INI_PATH, 'w', encoding='utf-8'))
                    self.operate_message_text_label.config(fg="green")
                    self.operate_message_text.set("卸载已完成!")
            except ValueError:
                self.operate_message_text_label.config(fg="red")
                self.operate_message_text.set("当前版本已不存在，请重新选择安装路径!")

    def remove_jmeter(self):
        ''' 卸载JMeter '''
        if self.remove_lock:
            self.remove_lock = 0
            if eval(self.cf.get('installed', 'versions')) and eval(self.cf.get('installed', 'jmeter_paths')):
                _t6 = threading.Thread(target=self.remove_thread)
                _t6.setDaemon(True)
                _t6.start()
            else:
                self.operate_message_text_label.config(fg="red")
                self.operate_message_text.set("操作 >> 请先卸载当前版本!")
        else:
            self.operate_message_text_label.config(fg="red")
            self.operate_message_text.set("正在卸载中!")

    def choose_download_path(self):
        ''' 选择下载JMeter的文件夹 '''
        self.cf.read(JM_INI_PATH, encoding='utf-8')

        dirName = filedialog.askdirectory(initialdir=self.cf.get('settings', 'download_path'), title="请选择下载路径")
        if dirName:
            self.settings_download_path.set(dirName)
            self.cf.set('settings', 'download_path', dirName)
            self.cf.write(open(JM_INI_PATH, 'w', encoding='utf-8'))
        else:
            self.settings_download_path.set(self.cf.get('settings', 'download_path'))

    def choose_download_path_return(self, event):
        pass

    def choose_download_path_focusin(self, event):
        pass

    def choose_download_path_focusout(self, event):
        pass

    def choose_install_path_return(self, event):
        pass

    def choose_install_path_focusin(self, event):
        pass

    def choose_install_path_focusout(self, event):
        pass

    def choose_install_path(self):
        ''' 选择安装JMeter的文件夹 '''
        self.cf.read(JM_INI_PATH, encoding='UTF-8')
        dirName = filedialog.askdirectory(initialdir=self.cf.get('settings', 'install_path'), title="请选择安装/解压路径")
        if dirName:
            self.settings_install_path.set(dirName)
            self.cf.set('settings', 'install_path', dirName)
            self.cf.write(open(JM_INI_PATH, 'w', encoding='utf-8'))
            # 更新安装版本检测
            self.check_installed_list()
        else:
            self.settings_install_path.set(self.cf.get('settings', 'install_path'))

    def refresh_install_version_data(self):
        self.cf.read(JM_INI_PATH, encoding='utf-8')
        self.install_versions = eval(self.cf.get('install', 'archive_versions'))
        try:
            self.install_versions.sort(reverse=True)
            self.operate_install_version_list['values'] = self.install_versions
        except AttributeError:
            pass

    def refresh_installed_version_data(self):
        self.cf.read(JM_INI_PATH, encoding='utf-8')
        self.installed_versions = eval(self.cf.get('installed', 'versions'))
        try:
            self.installed_versions.sort(reverse=True)
            self.operate_installed_version_list['values'] = self.installed_versions
        except AttributeError:
            pass

    def refresh_mirror_url_data(self):
        self.cf.read(JM_INI_PATH, encoding='utf-8')
        self.settings_mirror_url_list['values'] = eval(self.cf.get('settings', 'download_urls'))

def main():
    JMeterManagerUI()

if __name__ == '__main__':
    main()