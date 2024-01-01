#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2023/12/30 23:48
@File  : JM_ui.py
'''
import threading

'''
基于tkinter的界面 + jm_ui.ini配置文件
'''

from JMeterManager import ttk, Progressbar, tk, CF_INIT, urlretrieve, filedialog, messagebox
from JMeterManager.utils import SET_JMETER_INSTALLED_VERSION, SET_JMETER_INSTALL_VERSIONS

class JMeterManagerUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("JMeter管理者·@xiaobaiTser")
        # 窗口设置为自适应
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.resizable(False, False)
        self.cf = CF_INIT()
        self.cf.read('jm_ui.ini', encoding='utf-8')
        self.create_widgets()
        # 更新数据
        _t1 = threading.Thread(target=SET_JMETER_INSTALL_VERSIONS)
        _t1.start()
        _t2 = threading.Thread(target=SET_JMETER_INSTALLED_VERSION)
        _t2.start()

        self.run()
        # self.refresh_data()
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
                                            fg="red")
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
        self.operate_message = tk.StringVar()
        self.operate_message_label = tk.Label(row_4_frame, textvariable=self.operate_message, fg="red")
        self.operate_message_label.pack(fill="x", padx=5, pady=10)

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

        # row_1_frame:镜像
        self.settings_mirror_label = tk.Label(row_1_frame, text="请选择镜像站：")
        self.settings_mirror_label.grid(row=0, column=0, padx=10, pady=10)
        self.settings_mirror_url = tk.StringVar()
        self.settings_mirror_url.set("请选择镜像站...")
        self.cf.read('jm_ui.ini', encoding='utf-8')
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
        self.settings_download_path.set("请选择下载路径...")
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
        self.settings_install_path.set("请选择安装路径...")
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
        self.settings_save_button = tk.Button(
                                                row_4_frame,
                                                text="保   存",
                                                command=self.save_settings,
                                                width=10,
                                                fg="white",
                                                bg="green")
        self.settings_save_button.pack(side="bottom")

        # row_5_frame:状态信息
        self.settings_message_text = tk.StringVar()
        self.settings_message_text.set("")
        self.settings_message_label = tk.Label(
                                                row_5_frame,
                                                textvariable=self.settings_message_text,
                                                fg="red")
        self.settings_message_label.pack(side="bottom")

    def download_thread(self):
        urlretrieve(self.settings_mirror_url.get() + f'/apache-jmeter-{self.operate_install_version.get()}.zip',
                    f'{self.settings_download_path.get()}/apache-jmeter-{self.operate_install_version.get()}.zip',
                    self.download_progress)
        # 更新状态信息
        self.operate_message_label.config(fg="green")
        self.operate_message.set("下载完成!")

        # 下载更新已下载列表
        self.cf.read('jm_ui.ini', encoding='utf-8')
        old_versions = eval(self.cf.get('installed', 'versions'))
        new_versions = old_versions.append(self.operate_install_version.get())
        self.cf.set('installed', 'versions', str(new_versions))

    def download_jmeter(self):
        ''' 基于镜像URL下载JMeter '''
        if self.operate_install_version.get() == "未选择":
            self.operate_message.set("请选择版本号!")
        elif self.settings_mirror_url.get() == "请选择镜像站...":
            self.operate_message.set("请选择镜像站!")
        elif self.settings_download_path.get() == "请选择下载路径...":
            self.operate_message.set("请选择下载路径!")
        else:
            threading.Thread(target=self.download_thread).start()
            self.operate_message_label.config(fg="green")
            self.operate_message.set("下载中...")

    def download_progress(self, block_num, block_size, total_size):
        ''' 下载进度条 '''
        self.operate_progressbar['maximum'] = total_size
        self.operate_progressbar['value'] = block_num * block_size
        self.operate_progressbar_proportion.set(str(round(block_num * block_size / total_size * 100)) + "%")
        self.operate_message_label.config(fg="green")

    def remove_jmeter(self):

        # 卸载后更新已下载列表
        old_versions = eval(self.cf.get('installed', 'versions'))
        new_versions = old_versions.remove(self.operate_install_version.get())
        self.cf.set('installed', 'versions', str(new_versions))

    def choose_download_path(self):
        ''' 选择下载JMeter的文件夹 '''
        dirName = filedialog.askdirectory(initialdir='~/Download/', title="请选择下载路径")
        self.settings_download_path.set(dirName) if dirName else self.settings_download_path.set("请选择下载路径...")


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


    def save_settings(self):
        pass

    def refresh_install_version_data(self):
        self.cf.read('jm_ui.ini', encoding='utf-8')
        self.install_versions = eval(self.cf.get('install', 'archive_versions'))
        self.install_versions.sort(reverse=True)
        self.operate_install_version_list['values'] = self.install_versions

    def refresh_installed_version_data(self):
        self.cf.read('jm_ui.ini', encoding='utf-8')
        self.installed_versions = eval(self.cf.get('installed', 'versions'))
        self.installed_versions.sort(reverse=True)
        self.operate_installed_version_list['values'] = self.installed_versions

    def refresh_mirror_url_data(self):
        self.cf.read('jm_ui.ini', encoding='utf-8')
        self.settings_mirror_url_list['values'] = eval(self.cf.get('settings', 'download_urls'))

if __name__ == '__main__':
    JMeterManagerUI()

