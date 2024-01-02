#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2023/12/30 23:48
@File  : JM_ui.py
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
                        JM_INI_PATH, \
                        main_requires_admin, \
                        CreateKey, \
                        OpenKey, \
                        QueryValueEx, \
                        SetValueEx, \
                        HKEY_LOCAL_MACHINE, \
                        KEY_WRITE, \
                        KEY_ALL_ACCESS, \
                        REG_SZ, \
                        REG_EXPAND_SZ, \
                        CloseKey, \
                        sleep, \
                        ctypes

from utils import SET_JMETER_INSTALLED_VERSION, SET_JMETER_INSTALL_VERSIONS, _SYSTEM_NAME_

class JMeterManagerUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title_text = "JMeterManager·@xiaobaiTser v1.0.0      "
        self.title(self.title_text)
        # 窗口设置为自适应
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.resizable(False, False)
        self.cf = CF_INIT()
        self.cf.read(JM_INI_PATH, encoding='utf-8')
        self.operate_message_text = tk.StringVar()
        self.settings_message_text = tk.StringVar()
        self.create_widgets()

        # 更新数据
        self.operate_message_text.set('正在更新可安装版本号')
        self.settings_message_text.set('正在更新可安装版本号')
        threading.Thread(target=SET_JMETER_INSTALL_VERSIONS).start()
        self.operate_message_text.set('已完成更新可安装版本号')
        self.settings_message_text.set('已完成更新可安装版本号')
        self.operate_message_text.set('正在检测已安装版本号')
        self.settings_message_text.set('正在检测已安装版本号')
        threading.Thread(target=SET_JMETER_INSTALLED_VERSION).start()
        self.operate_message_text.set('已完成已安装版本号检测')
        self.settings_message_text.set('已完成已安装版本号检测')

        self.run()
        self.after(500, self.title_refresh)
        self.mainloop()

    def run(self):
        # 监控关闭窗口事件，防止卡线程
        self.protocol('WM_DELETE_WINDOW', self.window_close)

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
        self.operate = ttk.Frame(self.tab_control)
        self.settings = ttk.Frame(self.tab_control)
        self.tab_control.add(self.operate, text="操 作")
        self.tab_control.add(self.settings, text="设 置")
        self.tab_control.pack(expand=1, fill="both")
        self.create_operate()
        self.create_settings()

    def create_operate(self):
        ''' 操作页 '''
        # 设置多行Frame
        row_1_frame = tk.Frame(self.operate, height=20)
        row_1_frame.pack()
        row_2_frame = tk.Frame(self.operate, height=20)
        row_2_frame.pack()
        row_3_frame = tk.Frame(self.operate, height=20)
        row_3_frame.pack()
        row_4_frame = tk.Frame(self.operate, height=20)
        row_4_frame.pack()

        # row_1_frame
        self.operate_install_label = tk.Label(row_1_frame, text="可安装版本号：")
        self.operate_install_label.grid(row=0, column=0, padx=5, pady=10)
        self.operate_install_version = tk.StringVar()
        self.operate_install_version.set("未选择")

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
        self.operate_installed_label = tk.Label(row_2_frame, text="可卸载装版本：")
        self.operate_installed_label.grid(row=1, column=0, padx=5, pady=10)
        self.operate_installed_version = tk.StringVar()
        self.operate_installed_version.set("可卸载版本号")
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
                                            state="disabled"
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
        self.settings_mirror_label = tk.Label(row_1_frame, text="请选择镜像站：")
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
        self.settings_download_path_label = tk.Label(row_2_frame, text="请选择下载路径：")
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
        self.settings_install_path_label = tk.Label(row_3_frame, text="请选择安装路径：")
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

        # row_4_frame:保存
        # self.settings_save_button = tk.Button(
        #                                         row_4_frame,
        #                                         text="保   存",
        #                                         command=self.save_settings,
        #                                         width=10,
        #                                         fg="white",
        #                                         bg="green")
        # self.settings_save_button.pack(side="bottom")

        # row_5_frame:状态信息
        
        self.settings_message_text.set("")
        self.settings_message_label = tk.Label(
                                                row_4_frame,
                                                textvariable=self.settings_message_text,
                                                fg="red")
        self.settings_message_label.pack(side="bottom")

    def title_refresh_thread(self):
        ''' 循环修改标题内容 '''
        while True:
            self.title_text = self.title_text[1:] + self.title_text[0:1]
            self.title(self.title_text)
            sleep(0.5)

    def title_refresh(self):
        ''' 实时更新标题，类似于跑马灯 '''
        try:
            threading.Thread(target=self.title_refresh_thread).start()
        except RuntimeError:
            pass

    # @main_requires_admin
    def refresh_system_environment(self):
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A

        SMTO_ABORTIFHUNG = 0x0002

        result = ctypes.c_long()
        SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
        SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u'Environment', SMTO_ABORTIFHUNG, 5000,
                            ctypes.byref(result))

    # @main_requires_admin
    def set_system_environment(self,
                               env_name: str = '',
                               env_path: str = '',
                               add_path: bool = True,
                               end_path: str = '/bin'):
        ''' 设置系统环境，windows使用winreg,linux使用/etc/profile '''
        env_name = env_name.upper().strip()
        if _SYSTEM_NAME_ == "Windows":
            REG_PATH = r'SYSTEM\\ControlSet001\\Control\\Session Manager\\Environment'
            write_env_key = OpenKey(HKEY_LOCAL_MACHINE, REG_PATH, 0, access=KEY_ALL_ACCESS)
            path_env = QueryValueEx(write_env_key, 'path')[0]

            if env_name:
                # add key
                SetValueEx(write_env_key, env_name, 0, REG_SZ, env_path)
            if add_path:
                env_value = f'{path_env};%{env_name}%{end_path}' if env_name else f'{path_env};{env_path}'
                SetValueEx(write_env_key, 'path', 0, REG_EXPAND_SZ, env_value)
            CloseKey(write_env_key)
            self.refresh_system_environment()
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


    def download_thread(self):
        ''' 下载线程 '''
        _version = self.operate_install_version.get()
        if _version == "未选择":
            self.operate_message_text.set("请选择版本号!")
        elif _version in eval(self.cf.get('installed', 'versions')):
            self.operate_message_text.set("版本已安装! 请选择其它版本")
        else:
            urlretrieve(self.settings_mirror_url.get() +
                        f'/apache-jmeter-{self.operate_install_version.get()}.zip',
                        f'{self.settings_download_path.get()}/apache-jmeter-{self.operate_install_version.get()}.zip',
                        self.download_progress)
            # 更新状态信息
            self.operate_message_text_label.config(fg="green")
            self.operate_message_text.set("下载完成!")

            # 解压下载的压缩包到指定目录
            ZipFile(f'{self.settings_download_path.get()}/apache-jmeter-{self.operate_install_version.get()}.zip').\
                extractall(self.settings_install_path.get())
            self.operate_message_text.set("解压完成!")

            # 删除下载的压缩包
            os.remove(f'{self.settings_download_path.get()}/apache-jmeter-{self.operate_install_version.get()}.zip')
            self.operate_message_text.set("删除压缩包成功!")

            # 更新已安装列表
            self.cf.read(JM_INI_PATH, encoding='utf-8')
            old_versions = eval(self.cf.get('installed', 'versions'))
            new_versions = old_versions.append(self.operate_install_version.get())
            self.cf.set('installed', 'versions', str(new_versions))
            self.cf.write(open(JM_INI_PATH, 'w', encoding='utf-8'))
            # 在已安装列表中添加刚刚安装的版本号
            self.refresh_installed_version_data()

        # 可以将已安装版本修改为默认版本

        # 设置永久系统环境变量（windows使用winreg，其他系统使用直接写入/ect/profile和source命令）
        self.set_system_environment(
            env_name='JMETER_HOME',
            env_path=f'{self.settings_install_path.get()}/apache-jmeter-{self.operate_install_version.get()}',
            add_path=True,
            end_path='/bin'
        )
        self.operate_message_text.set(f"【{self.operate_install_version.get()}】环境变量设置成功! 请在命令行执行【jmeter】")

        # 更新当前版本为新安装版本
        cmd_result = [v for v in Popen('java -version', shell=True, stdout=PIPE, stderr=STDOUT, encoding='utf-8').stdout.readlines() if 'version' in v][0].split(' ')
        jdk_version = [v for v in cmd_result if '.' in v][0]
        self.cf.set('current', 'jdk_version', jdk_version)
        self.cf.set('current', 'jmeter_version', self.operate_install_version.get())
        self.cf.set('current', 'jmeter_home', f'{self.settings_install_path.get()}/apache-jmeter-{self.operate_install_version.get()}')
        self.cf.write(open(JM_INI_PATH, 'w', encoding='utf-8'))

    def download_jmeter(self):
        ''' 基于镜像URL下载JMeter '''
        if self.operate_install_version.get() == "未选择":
            self.operate_message_text.set("操作 >> 请选择版本号!")
        elif self.settings_mirror_url.get() == "请选择镜像站...":
            self.operate_message_text.set("设置 >> 请选择镜像站!")
        elif self.settings_download_path.get() == "请选择下载路径...":
            self.operate_message_text.set("设置 >> 请选择下载路径!")
        elif self.settings_install_path.get() == "请选择安装路径...":
            self.operate_message_text.set("设置 >> 请选择安装路径!")
        else:
            threading.Thread(target=self.download_thread).start()
            self.operate_message_text_label.config(fg="green")
            self.operate_message_text.set("下载中...")

    def download_progress(self, block_num, block_size, total_size):
        ''' 下载进度条 '''
        self.operate_progressbar['maximum'] = total_size
        self.operate_progressbar['value'] = block_num * block_size
        self.operate_progressbar_proportion.set(str(round(block_num * block_size / total_size * 100)) + "%")
        self.operate_message_text_label.config(fg="green")

    def remove_jmeter(self):

        # 卸载后更新已下载列表
        old_versions = eval(self.cf.get('installed', 'versions'))
        new_versions = old_versions.remove(self.operate_install_version.get())
        self.cf.set('installed', 'versions', str(new_versions))

    def choose_download_path(self):
        ''' 选择下载JMeter的文件夹 '''
        self.cf.read(JM_INI_PATH, encoding='utf-8')
        dirName = filedialog.askdirectory(initialdir='~/Downloads/', title="请选择下载路径")
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
        dirName = filedialog.askdirectory(initialdir='~/Desktop/', title="请选择安装/解压路径")
        if dirName:
            self.settings_install_path.set(dirName)
            self.cf.set('settings', 'install_path', dirName)
            self.cf.write(open(JM_INI_PATH, 'w', encoding='utf-8'))
            # 更新安装版本检测
            self.operate_message_text.set("检测已安装版本中...")
            self.settings_message_text.set("检测已安装版本中...")
            threading.Thread(target=SET_JMETER_INSTALLED_VERSION()).start()
            self.operate_message_text.set("已完成已安装版本检测")
            self.settings_message_text.set("已完成已安装版本检测")
        else:
            self.settings_install_path.set(self.cf.get('settings', 'install_path'))


    def save_settings(self):
        pass

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

if __name__ == '__main__':
    JMeterManagerUI()
