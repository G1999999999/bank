# -*- coding:utf-8 -*-
import datetime
from datetime import  datetime
from datetime import date
import wx.adv
import wx.grid
import wx
import psycopg2
import random
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import re
class TransparentStaticText(wx.StaticText):
    def __init__(self, parent, id=wx.ID_ANY, label='', pos=wx.DefaultPosition,
                 size=wx.DefaultSize,style=wx.TRANSPARENT_WINDOW, name='TransparentStaticText'):
        wx.StaticText.__init__(self, parent, id, label, pos, size, style, name)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_SIZE, self.OnSize)
    def OnPaint(self, event):
        bdc = wx.PaintDC(self)
        dc = wx.GCDC(bdc)
        font_face = self.GetFont()
        font_color = self.GetForegroundColour()
        dc.SetFont(font_face)
        dc.SetTextForeground(font_color)
        dc.DrawText(self.GetLabel(), 0, 0)
    def OnSize(self, event):
        self.Refresh()
        event.Skip()
class Frame(wx.Frame):
    def __init__(self):
        self.exit_1=0
        wx.Frame.__init__(self, None, title='银行储蓄管理系统', size=(837, 546), name='frame', style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        #541072960
        self.startwindow = wx.Panel(self)
        self.startwindow.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)
        self.Centre()
        self.label1 = wx.StaticText(self.startwindow, size=(111, 32), pos=(72, 40),
                                    label='请选择要办理的业务',name='staticText',style=2321, )
        self.label1.SetOwnBackgroundColour('white')
        self.check_nums = '\n'
        self.icon1 = wx.Icon(name="00.ico", type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon1)
        # 初始界面
        self.button7 = wx.Button(self.startwindow, size=(180, 70), pos=(300, 100), label='登录', name='button')
        self.button7.Bind(wx.EVT_LEFT_DOWN or wx.EVT_ENTER_WINDOW, self.login_in)
        self.button8 = wx.Button(self.startwindow, size=(180, 70), pos=(300, 175), label='办理账户', name='button')
        self.button8.Bind(wx.EVT_LEFT_DOWN, self.open_account)
        self.button9 = wx.Button(self.startwindow, size=(180, 70), pos=(300, 250), label='查询账户', name='button')
        self.button9.Bind(wx.EVT_LEFT_DOWN, self.find_account)
        self.find_pw = wx.Button(self.startwindow, size=(180, 70), pos=(300, 325), label='重置密码', name='button')
        self.find_pw.Bind(wx.EVT_LEFT_DOWN, self.find_password)
        # 业务办理界面
        self.button1 = wx.Button(self.startwindow, size=(180, 80), pos=(100, 100), label='存款', name='button')
        self.button1.Bind(wx.EVT_LEFT_DOWN, self.save_money)
        self.button1.Hide()
        self.button2 = wx.Button(self.startwindow, size=(180, 80), pos=(100, 200), label='取款', name='button')
        self.button2.Bind(wx.EVT_LEFT_DOWN, self.withdraw_money)
        self.button2.Hide()
        self.transfer_ = wx.Button(self.startwindow, size=(180, 80), pos=(300, 100), label='转账', name='button')
        self.transfer_.Bind(wx.EVT_LEFT_DOWN, self.transfer_show)
        self.transfer_.Hide()
        self.button3 = wx.Button(self.startwindow, size=(180, 80), pos=(100, 300), label='解冻账户', name='button')
        self.button3.Bind(wx.EVT_LEFT_DOWN, self.unfreeze_account_show)
        self.button3.Hide()
        self.button6 = wx.Button(self.startwindow, size=(180, 80), pos=(500, 300), label='冻结账户', name='button')
        self.button6.Bind(wx.EVT_LEFT_DOWN, self.blocked_account_show)
        self.button6.Hide()
        self.button4 = wx.Button(self.startwindow, size=(180, 80), pos=(500, 100), label='查询余额', name='button')
        self.button4.Bind(wx.EVT_LEFT_DOWN, self.check_balance)
        self.button4.Hide()
        self.button5 = wx.Button(self.startwindow, size=(180, 80), pos=(500, 200), label='查询历史纪录', name='button')
        self.button5.Bind(wx.EVT_LEFT_DOWN, self.check_history)
        self.button5.Hide()
        self.button0 = wx.Button(self.startwindow, size=(180, 80), pos=(300, 200), label='返回', name='button')
        self.button0.Bind(wx.EVT_LEFT_DOWN, self.mainwin)
        self.button0.Hide()
        self.zhuxiao = wx.Button(self.startwindow, size=(180, 80), pos=(300, 300), label='注销', name='button')
        self.zhuxiao.Bind(wx.EVT_LEFT_DOWN, self.cancel_show)
        self.zhuxiao.Hide()
        # 登录页面
        self.no_card = TransparentStaticText(self.startwindow, size=(60, 30), pos=(230, 200), label='银行卡号:',
                                             name='staticText', style=2321)
        self.no_card.Hide()
        self.pa_card = TransparentStaticText(self.startwindow, size=(90, 30), pos=(210, 300), label='请输入6位密码:',
                                             name='staticText', style=2321)
        self.pa_card.Hide()
        self.in_no_card = wx.TextCtrl(self.startwindow, size=(300, 30), pos=(300, 200), value='', name='text', style=0)
        self.in_no_card.Hide()
        self.in_pa_card = wx.TextCtrl(self.startwindow, size=(300, 30), pos=(300, 300), value='', name='text',
                                      style=wx.TE_PASSWORD)
        self.in_pa_card.Hide()
        self.log = wx.Button(self.startwindow, size=(70, 30), pos=(330, 400), label='确定', name='button')
        self.log.Bind(wx.EVT_LEFT_DOWN, self.log_che)
        self.log.Hide()
        self.return_ = wx.Button(self.startwindow, size=(70, 30), pos=(430, 400), label='退出', name='button')
        self.return_.Bind(wx.EVT_LEFT_DOWN, self.mainwin)
        self.return_.Hide()
        # 开户界面
        self.mess = TransparentStaticText(self.startwindow, size=(100, 50), pos=(100, 50), label='请输入信息',
                                          name='staticText', style=2321)
        self.mess.Hide()
        self.user_name = TransparentStaticText(self.startwindow, size=(50, 30), pos=(230, 30), label='姓名:',
                                               name='staticText', style=2321)
        self.user_name.Hide()
        self.id_num = TransparentStaticText(self.startwindow, size=(60, 30), pos=(230, 80), label='身份证号:',
                                            name='staticText', style=2321)
        self.id_num.Hide()
        self.address = TransparentStaticText(self.startwindow, size=(60, 30), pos=(230, 215 - 50 - 20), label='居住地址:',
                                             name='staticText', style=2321)
        self.address.Hide()
        self.pass1 = TransparentStaticText(self.startwindow, size=(70, 30), pos=(220, 210), label='设置6位密码:',
                                           name='staticText', style=2321)
        self.pass1.Hide()
        self.pass2 = TransparentStaticText(self.startwindow, size=(70, 30), pos=(220, 260), label='确认6位密码:',
                                           name='staticText', style=2321)
        self.pass2.Hide()
        self.mail = TransparentStaticText(self.startwindow, size=(50, 30), pos=(230, 310), label='邮箱:',
                                          name='staticText', style=2321)
        self.mail.Hide()
        self.in_mail = wx.TextCtrl(self.startwindow, size=(300, 30), pos=(300, 310), value='', name='text', style=0)
        self.in_mail.Hide()
        self.mail_yanzhengma = TransparentStaticText(self.startwindow, size=(70, 30), pos=(230, 360), label='邮箱验证码:',
                                                     name='staticText', style=2321)
        self.mail_yanzhengma.Hide()
        self.in_mail_yanzhengma = wx.TextCtrl(self.startwindow, size=(170, 30), pos=(300, 360), value='', name='text',
                                              style=0)
        self.in_mail_yanzhengma.Hide()
        self.b_yanzhengma_ = wx.Button(self.startwindow, size=(130, 30), pos=(470, 360), label='获得验证码', name='button')
        self.b_yanzhengma_.Bind(wx.EVT_LEFT_DOWN, self.get_yanzhengma_)
        self.b_yanzhengma_.Hide()
        self.in_user_name = wx.TextCtrl(self.startwindow, size=(300, 30), pos=(300, 30), value='', name='text', style=0)
        self.in_user_name.Hide()
        self.in_id_num = wx.TextCtrl(self.startwindow, size=(300, 30), pos=(300, 80), value='', name='text', style=0)
        self.in_id_num.Hide()
        self.in_address = wx.TextCtrl(self.startwindow, size=(300, 60), pos=(300, 130), value='', name='text',
                                      style=wx.TE_MULTILINE)
        self.in_address.Hide()
        self.in_pass1 = wx.TextCtrl(self.startwindow, size=(300, 30), pos=(300, 210), value='', name='text',
                                    style=wx.TE_PASSWORD)
        self.in_pass1.Hide()
        self.in_pass2 = wx.TextCtrl(self.startwindow, size=(300, 30), pos=(300, 260), value='', name='text',
                                    style=wx.TE_PASSWORD)
        self.in_pass2.Hide()
        self.create = wx.Button(self.startwindow, size=(70, 30), pos=(330, 400), label='创建', name='button')
        self.create.Bind(wx.EVT_LEFT_DOWN, self.create_account)
        self.create.Hide()
        # 存款
        self.save_ = TransparentStaticText(self.startwindow, size=(205, 30), pos=(180, 100), label='请选择或输入存款金额（单位：元）：',
                                           name='staticText', style=2321)
        self.save_.Hide()
        self.in_save = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 100), value='', name='text', style=0)
        self.in_save.Hide()
        self.save = wx.Button(self.startwindow, size=(70, 30), pos=(330, 300), label='存款', name='button')
        self.save.Bind(wx.EVT_LEFT_DOWN, self.save_money_che or self.clear_yue1)
        self.save.Hide()
        self.save_re = wx.Button(self.startwindow, size=(70, 30), pos=(430, 300), label='返回', name='button')
        self.save_re.Bind(wx.EVT_LEFT_DOWN, self.business_handing)
        self.save_re.Hide()
        self.save_yu = TransparentStaticText(self.startwindow, size=(150, 30), pos=(310, 200), label='可用余额：',
                                             name='staticText', style=2321)
        self.save_yu.Hide()
        self.save_yue = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 200), style=wx.TE_READONLY)
        self.save_yue.Hide()
        self._50_ = wx.Button(self.startwindow, size=(70, 30), pos=(210, 136), label='50', name='button')
        self._50_.Bind(wx.EVT_LEFT_DOWN, self._50sel)
        self._50_.Hide()
        self._100_ = wx.Button(self.startwindow, size=(70, 30), pos=(300, 136), label='100', name='button')
        self._100_.Bind(wx.EVT_LEFT_DOWN, self._100sel)
        self._100_.Hide()
        self._500_ = wx.Button(self.startwindow, size=(70, 30), pos=(390, 136), label='500', name='button')
        self._500_.Bind(wx.EVT_LEFT_DOWN, self._500sel)
        self._500_.Hide()
        self._1000_ = wx.Button(self.startwindow, size=(70, 30), pos=(480, 136), label='1000', name='button')
        self._1000_.Bind(wx.EVT_LEFT_DOWN, self._1000sel)
        self._1000_.Hide()
        self._2000_ = wx.Button(self.startwindow, size=(70, 30), pos=(570, 136), label='2000', name='button')
        self._2000_.Bind(wx.EVT_LEFT_DOWN, self._2000sel)
        self._2000_.Hide()
        # 取款
        self.withdraw_ = TransparentStaticText(self.startwindow, size=(205, 30), pos=(180, 200),
                                               label='请选择或输入取款金额（单位：元）：', name='staticText', style=2321)
        self.withdraw_.Hide()
        self.in_withdraw = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 200), value='', name='text', style=0)
        self.in_withdraw.Hide()
        self.withdraw = wx.Button(self.startwindow, size=(70, 30), pos=(330, 300), label='取款', name='button')
        self.withdraw.Bind(wx.EVT_LEFT_DOWN, self.withdraw_money_che or self.clear_yue1)
        self.withdraw.Hide()
        self.withdraw_yu = TransparentStaticText(self.startwindow, size=(190, 30), pos=(200, 100), label='可取余额（单位：元）：',
                                                 name='staticText', style=2321)
        self.withdraw_yu.Hide()
        self.withdraw_yue = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 100), style=wx.TE_READONLY)
        self.withdraw_yue.Hide()
        self._50 = wx.Button(self.startwindow, size=(70, 30), pos=(210, 236), label='50', name='button')
        self._50.Bind(wx.EVT_LEFT_DOWN, self._50sel)
        self._50.Hide()
        self._100 = wx.Button(self.startwindow, size=(70, 30), pos=(300, 236), label='100', name='button')
        self._100.Bind(wx.EVT_LEFT_DOWN, self._100sel)
        self._100.Hide()
        self._500 = wx.Button(self.startwindow, size=(70, 30), pos=(390, 236), label='500', name='button')
        self._500.Bind(wx.EVT_LEFT_DOWN, self._500sel)
        self._500.Hide()
        self._1000 = wx.Button(self.startwindow, size=(70, 30), pos=(480, 236), label='1000', name='button')
        self._1000.Bind(wx.EVT_LEFT_DOWN, self._1000sel)
        self._1000.Hide()
        self._2000 = wx.Button(self.startwindow, size=(70, 30), pos=(570, 236), label='2000', name='button')
        self._2000.Bind(wx.EVT_LEFT_DOWN, self._2000sel)
        self._2000.Hide()
        # 查询余额
        self.check_ba = TransparentStaticText(self.startwindow, size=(150, 30), pos=(200, 205), label='余额（单位：元）：',
                                              name='staticText', style=2321)
        self.check_ba.Hide()
        self.check_bal = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(350, 200), style=wx.TE_READONLY)
        self.check_bal.Hide()
        self.check_yu = wx.Button(self.startwindow, size=(70, 30), pos=(290, 300), label='查询', name='button')
        self.check_yu.Bind(wx.EVT_LEFT_DOWN, self.check_balance_che or self.clear_yue1)
        self.check_yu.Hide()
        # 查询历史记录
        self.date1 = wx.adv.DatePickerCtrl(self.startwindow, size=(150, 30), pos=(350, 150), name='datectrl', style=2)
        self.date1.Hide()
        self.date2 = wx.adv.DatePickerCtrl(self.startwindow, size=(150, 30), pos=(350, 200), name='datectrl', style=2)
        self.date2.Hide()
        self.date1_ = TransparentStaticText(self.startwindow, size=(100, 30), pos=(250, 155), label='起始日期:',
                                            name='staticText', style=2321)
        self.date1_.Hide()
        self.date2_ = TransparentStaticText(self.startwindow, size=(100, 30), pos=(250, 205), label='结束日期:',
                                            name='staticText', style=2321)
        self.date2_.Hide()
        self.label_date = TransparentStaticText(self.startwindow, size=(170, 50), pos=(100, 100), label='请选择日期范围',
                                                name='staticText', style=2321)
        self.label_date.Hide()
        self.check_his = wx.Button(self.startwindow, size=(70, 30), pos=(290, 300), label='查询', name='button')
        self.check_his.Bind(wx.EVT_LEFT_DOWN, self.che_his_mainwin or self.clear_yue1)
        self.check_his.Hide()
        # 查询历史记录1
        self.grid = wx.grid.Grid(self.startwindow, id=wx.ID_ANY, size=(775, 460), pos=(10, 10))
        self.grid.Hide()
        self.check_his_re = wx.Button(self.startwindow, size=(70, 30), pos=(350, 470), label='返回', name='button')
        self.check_his_re.Bind(wx.EVT_LEFT_DOWN, self.check_history)
        self.check_his_re.Hide()
        # 查询银行卡
        self.id_find = TransparentStaticText(self.startwindow, size=(125, 30), pos=(200, 165), label='请输入持卡人身份证号:',
                                             name='staticText', style=2321)
        self.id_find.Hide()
        self.in_id_num1 = wx.TextCtrl(self.startwindow, size=(300, 30), pos=(350, 160), value='', name='text', style=0)
        self.in_id_num1.Hide()
        self.find = wx.Button(self.startwindow, size=(70, 30), pos=(290, 300), label='查询', name='button')
        self.find.Bind(wx.EVT_LEFT_DOWN, self.find_account_)
        self.find.Hide()
        self.find_re = wx.Button(self.startwindow, size=(70, 30), pos=(430, 300), label='返回', name='button')
        self.find_re.Bind(wx.EVT_LEFT_DOWN, self.mainwin)
        self.find_re.Hide()
        self.grid1 = wx.grid.Grid(self.startwindow, id=wx.ID_ANY, size=(775, 460), pos=(10, 10))
        self.grid1.Hide()
        self.find_account_re = wx.Button(self.startwindow, size=(70, 30), pos=(700, 100), label='返回', name='button')
        self.find_account_re.Bind(wx.EVT_LEFT_DOWN, self.find_account)
        self.find_account_re.Hide()
        # 查询银行卡1
        self.name_ = wx.TextCtrl(self.startwindow, size=(160, 30), pos=(105, 10), value='', name='text',
                                 style=wx.TE_READONLY)
        self.name_.Hide()
        self.sex_ = wx.TextCtrl(self.startwindow, size=(50, 30), pos=(350, 10), value='', name='text',
                                style=wx.TE_READONLY)
        self.sex_.Hide()
        self.age_ = wx.TextCtrl(self.startwindow, size=(50, 30), pos=(560, 10), value='', name='text',
                                style=wx.TE_READONLY)
        self.age_.Hide()
        self.num_1 = wx.TextCtrl(self.startwindow, size=(300, 30), pos=(120, 60), value='', name='text',
                                 style=wx.TE_READONLY)
        self.num_1.Hide()
        self.address_ = wx.TextCtrl(self.startwindow, size=(300, 50), pos=(120, 105), value='', name='text',
                                    style=wx.TE_MULTILINE ^ wx.TE_READONLY)
        self.address_.Hide()
        self.name = TransparentStaticText(self.startwindow, size=(50, 30), pos=(55, 10), label='姓名:', name='staticText',
                                          style=0)
        self.name.Hide()
        self.sex = TransparentStaticText(self.startwindow, size=(50, 30), pos=(300, 10), label='性别:', name='staticText',
                                         style=0)
        self.sex.Hide()
        self.age = TransparentStaticText(self.startwindow, size=(50, 30), pos=(510, 10), label='年龄:', name='staticText',
                                         style=0)
        self.age.Hide()
        self.num1 = TransparentStaticText(self.startwindow, size=(60, 30), pos=(55, 60), label='身份证号:',
                                          name='staticText', style=0)
        self.num1.Hide()
        self.address1 = TransparentStaticText(self.startwindow, size=(60, 30), pos=(55, 115), label='居住地址:',
                                              name='staticText', style=0)
        self.address1.Hide()
        # 修改个人信息
        self.change_information = wx.Button(self.startwindow, size=(100, 30), pos=(555, 100), label='修改个人信息',
                                            name='button')
        self.change_information.Bind(wx.EVT_LEFT_DOWN, self.change_information_show)
        self.change_information.Hide()
        self.change_information_ = wx.Button(self.startwindow, size=(70, 30), pos=(330, 300), label='修改', name='button')
        self.change_information_.Bind(wx.EVT_LEFT_DOWN, self.change_information_e)
        self.change_information_.Hide()
        self.change_re = wx.Button(self.startwindow, size=(70, 30), pos=(430, 300), label='返回', name='button')
        self.change_re.Bind(wx.EVT_LEFT_DOWN, self.find_account_)
        self.change_re.Hide()
        self.change_id = TransparentStaticText(self.startwindow, size=(130, 30), pos=(210, 100), label='身份证号：',
                                               name='staticText', style=2321)
        self.change_id.Hide()
        self.change_id_ = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(350, 100), value='', name='text',
                                      style=wx.TE_READONLY)
        self.change_id_.Hide()
        self.change_name = TransparentStaticText(self.startwindow, size=(130, 30), pos=(210, 150), label='姓名：',
                                                 name='staticText', style=2321)
        self.change_name.Hide()
        self.change_name_ = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(350, 150), value='', name='text',
                                        style=0)
        self.change_name_.Hide()
        self.change_address = TransparentStaticText(self.startwindow, size=(130, 30), pos=(210, 220), label='居住地址：',
                                                    name='staticText', style=2321)
        self.change_address.Hide()
        self.change_address_ = wx.TextCtrl(self.startwindow, size=(200, 60), pos=(350, 200), value='', name='text',
                                           style=wx.TE_MULTILINE)
        self.change_address_.Hide()
        # 冻结账户
        self.card_num = TransparentStaticText(self.startwindow, size=(130, 30), pos=(250, 100), label='银行卡账号：',
                                              name='staticText', style=2321)
        self.card_num.Hide()
        self.card_num_ = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 100), value='', name='text',
                                     style=wx.TE_READONLY)
        self.card_num_.Hide()
        self.frozen = wx.Button(self.startwindow, size=(70, 30), pos=(330, 300), label='冻结', name='button')
        self.frozen.Bind(wx.EVT_LEFT_DOWN, self.blocked_account)
        self.frozen.Hide()
        self.save_re = wx.Button(self.startwindow, size=(70, 30), pos=(430, 300), label='返回', name='button')
        self.save_re.Bind(wx.EVT_LEFT_DOWN, self.business_handing)
        self.save_re.Hide()
        self.pass_ = TransparentStaticText(self.startwindow, size=(100, 30), pos=(260, 200), label='请输入6位密码：',
                                           name='staticText', style=2321)
        self.pass_.Hide()
        self.in_pass_ = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 200), value='', name='text',
                                    style=wx.TE_PASSWORD)
        self.in_pass_.Hide()
        # 解冻账户
        self.card_num_j = TransparentStaticText(self.startwindow, size=(130, 30), pos=(250, 100), label='银行卡账号：',
                                                name='staticText', style=2321)
        self.card_num_j.Hide()
        self.card_num_jd = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 100), value='', name='text',
                                       style=wx.TE_READONLY)
        self.card_num_jd.Hide()
        self.unf = wx.Button(self.startwindow, size=(70, 30), pos=(330, 300), label='解冻', name='button')
        self.unf.Bind(wx.EVT_LEFT_DOWN, self.unfreeze_account)
        self.unf.Hide()
        self.save_re = wx.Button(self.startwindow, size=(70, 30), pos=(430, 300), label='返回', name='button')
        self.save_re.Bind(wx.EVT_LEFT_DOWN, self.business_handing)
        self.save_re.Hide()
        self.pass_j = TransparentStaticText(self.startwindow, size=(100, 30), pos=(260, 150), label='请输入6位密码：',
                                            name='staticText', style=2321)
        self.pass_j.Hide()
        self.in_pass_j = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 150), value='', name='text',
                                     style=wx.TE_PASSWORD)
        self.in_pass_j.Hide()
        self.unf_yanzhengma = TransparentStaticText(self.startwindow, size=(80, 30), pos=(280, 200), label='邮箱验证码：',
                                                    name='staticText', style=2321)
        self.unf_yanzhengma.Hide()
        self.unf_yanzhengma_ = wx.TextCtrl(self.startwindow, size=(100, 30), pos=(390, 200), value='', name='text',
                                           style=wx.TE_PASSWORD)
        self.unf_yanzhengma_.Hide()
        self.unf_yanzhengma_j = wx.Button(self.startwindow, size=(70, 30), pos=(500, 200), label='获得验证码', name='button')
        self.unf_yanzhengma_j.Bind(wx.EVT_LEFT_DOWN, self.get_yanzhengma)
        self.unf_yanzhengma_j.Hide()
        # 注销账户
        self.card_num_c = TransparentStaticText(self.startwindow, size=(130, 30), pos=(250, 100), label='银行卡账号：',
                                                name='staticText', style=2321)
        self.card_num_c.Hide()
        self.card_num_ca = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 100), value='', name='text',
                                       style=wx.TE_READONLY)
        self.card_num_ca.Hide()
        self.cancel_ = wx.Button(self.startwindow, size=(70, 30), pos=(330, 300), label='注销', name='button')
        self.cancel_.Bind(wx.EVT_LEFT_DOWN, self.cancel)
        self.cancel_.Hide()
        self.save_re = wx.Button(self.startwindow, size=(70, 30), pos=(430, 300), label='返回', name='button')
        self.save_re.Bind(wx.EVT_LEFT_DOWN, self.business_handing)
        self.save_re.Hide()
        self.pass_c = TransparentStaticText(self.startwindow, size=(100, 30), pos=(260, 150), label='请输入6位密码：',
                                            name='staticText', style=2321)
        self.pass_c.Hide()
        self.in_pass_c = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 150), value='', name='text',
                                     style=wx.TE_PASSWORD)
        self.in_pass_c.Hide()
        self.cancel_yanzhengma = TransparentStaticText(self.startwindow, size=(80, 30), pos=(280, 200), label='邮箱验证码：',
                                                       name='staticText', style=2321)
        self.cancel_yanzhengma.Hide()
        self.cancel_yanzhengma_ = wx.TextCtrl(self.startwindow, size=(100, 30), pos=(390, 200), value='', name='text',
                                              style=wx.TE_PASSWORD)
        self.cancel_yanzhengma_.Hide()
        self.cancel_yanzhengma_j = wx.Button(self.startwindow, size=(70, 30), pos=(500, 200), label='获得验证码',
                                             name='button')
        self.cancel_yanzhengma_j.Bind(wx.EVT_LEFT_DOWN, self.get_yanzhengma)
        self.cancel_yanzhengma_j.Hide()
        # 转账
        self.tran_num_yue = TransparentStaticText(self.startwindow, size=(160, 30), pos=(230, 50), label='可转账余额（单位：元）：',
                                                  name='staticText', style=2321)
        self.tran_num_yue.Hide()
        self.tran_num_yue_ = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 50), value='', name='text',
                                         style=wx.TE_READONLY)
        self.tran_num_yue_.Hide()
        self.tran_num_c = TransparentStaticText(self.startwindow, size=(130, 30), pos=(250, 100), label='收款方账号：',
                                                name='staticText', style=2321)
        self.tran_num_c.Hide()
        self.tran_num_ca = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 100), value='', name='text', style=0)
        self.tran_num_ca.Hide()
        self.transfer_su = wx.Button(self.startwindow, size=(70, 30), pos=(330, 300), label='确定转账', name='button')
        self.transfer_su.Bind(wx.EVT_LEFT_DOWN, self.transfer)
        self.transfer_su.Hide()
        self.save_re = wx.Button(self.startwindow, size=(70, 30), pos=(430, 300), label='返回', name='button')
        self.save_re.Bind(wx.EVT_LEFT_DOWN, self.business_handing)
        self.save_re.Hide()
        self.pass_tr = TransparentStaticText(self.startwindow, size=(90, 30), pos=(280, 250), label='交易密码(6位)：',
                                             name='staticText', style=2321)
        self.pass_tr.Hide()
        self.in_pass_tr = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 250), value='', name='text',
                                      style=wx.TE_PASSWORD)
        self.in_pass_tr.Hide()
        self.tran_money = TransparentStaticText(self.startwindow, size=(150, 30), pos=(230, 150), label='转账金额（单位：元）:',
                                                name='staticText', style=2321)
        self.tran_money.Hide()
        self.tran_money_ = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 150), value='', name='text', style=0)
        self.tran_money_.Hide()
        self._50_tr = wx.Button(self.startwindow, size=(70, 30), pos=(210, 200), label='50', name='button')
        self._50_tr.Bind(wx.EVT_LEFT_DOWN, self._50sel)
        self._50_tr.Hide()
        self._100_tr = wx.Button(self.startwindow, size=(70, 30), pos=(300, 200), label='100', name='button')
        self._100_tr.Bind(wx.EVT_LEFT_DOWN, self._100sel)
        self._100_tr.Hide()
        self._500_tr = wx.Button(self.startwindow, size=(70, 30), pos=(390, 200), label='500', name='button')
        self._500_tr.Bind(wx.EVT_LEFT_DOWN, self._500sel)
        self._500_tr.Hide()
        self._1000_tr = wx.Button(self.startwindow, size=(70, 30), pos=(480, 200), label='1000', name='button')
        self._1000_tr.Bind(wx.EVT_LEFT_DOWN, self._1000sel)
        self._1000_tr.Hide()
        self._2000_tr = wx.Button(self.startwindow, size=(70, 30), pos=(570, 200), label='2000', name='button')
        self._2000_tr.Bind(wx.EVT_LEFT_DOWN, self._2000sel)
        self._2000_tr.Hide()
        # 重置密码2
        self.find_password_card = TransparentStaticText(self.startwindow, size=(100, 30), pos=(280, 100),
                                                        label='银行卡账号：', name='staticText', style=2321)
        self.find_password_card.Hide()
        self.find_password_card_ = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 100), value='', name='text',
                                               style=wx.TE_READONLY)
        self.find_password_card_.Hide()
        self.find_password_mail = TransparentStaticText(self.startwindow, size=(130, 30), pos=(310, 150), label='邮箱：',
                                                        name='staticText', style=2321)
        self.find_password_mail.Hide()
        self.find_password_mail_ = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 150), value='', name='text',
                                               style=wx.TE_READONLY)
        self.find_password_mail_.Hide()
        self.find_yanzhengma = TransparentStaticText(self.startwindow, size=(80, 30), pos=(285, 200), label='邮箱验证码：',
                                                     name='staticText', style=2321)
        self.find_yanzhengma.Hide()
        self.find_yanzhengma_ = wx.TextCtrl(self.startwindow, size=(100, 30), pos=(390, 200), value='', name='text',
                                            style=0)
        self.find_yanzhengma_.Hide()
        self.find_yanzhengma_j = wx.Button(self.startwindow, size=(70, 30), pos=(500, 200), label='获得验证码',
                                           name='button')
        self.find_yanzhengma_j.Bind(wx.EVT_LEFT_DOWN, self.get_yanzhengma_find_)
        self.find_yanzhengma_j.Hide()
        self.fpass_s = TransparentStaticText(self.startwindow, size=(100, 30), pos=(280, 250), label='请设置新密码：',
                                             name='staticText', style=2321)
        self.fpass_s.Hide()
        self.fin_pass_s = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 250), value='', name='text',
                                      style=wx.TE_PASSWORD)
        self.fin_pass_s.Hide()
        self.fpass_s_ = TransparentStaticText(self.startwindow, size=(100, 30), pos=(295, 300), label='确认密码：',
                                              name='staticText', style=2321)
        self.fpass_s_.Hide()
        self.fin_pass_s_ = wx.TextCtrl(self.startwindow, size=(200, 30), pos=(390, 300), value='', name='text',
                                       style=wx.TE_PASSWORD)
        self.fin_pass_s_.Hide()
        self.find_p = wx.Button(self.startwindow, size=(70, 30), pos=(330, 350), label='确认重置', name='button')
        self.find_p.Bind(wx.EVT_LEFT_DOWN, self.find_password_sure)
        self.find_p.Hide()
        self.find_re_ = wx.Button(self.startwindow, size=(70, 30), pos=(430, 350), label='返回', name='button')
        self.find_re_.Bind(wx.EVT_LEFT_DOWN, self.find_password)
        self.find_re_.Hide()
        # 重置密码1
        self.find_password_ca = TransparentStaticText(self.startwindow, size=(180, 30), pos=(170, 185),
                                                      label='请输入需要重置密码的银行卡号:', name='staticText', style=2321)
        self.find_password_ca.Hide()
        self.find_password_ca_ = wx.TextCtrl(self.startwindow, size=(300, 30), pos=(350, 180), value='', name='text',
                                             style=0)
        self.find_password_ca_.Hide()
        self.find_pa = wx.Button(self.startwindow, size=(70, 30), pos=(290, 300), label='重置', name='button')
        self.find_pa.Bind(wx.EVT_LEFT_DOWN, self.find_password_)
        self.find_pa.Hide()
        self.find_re = wx.Button(self.startwindow, size=(70, 30), pos=(430, 300), label='返回', name='button')
        self.find_re.Bind(wx.EVT_LEFT_DOWN, self.mainwin)
        self.find_re.Hide()
    def hide(self):
        #重置密码
        self.find_pw.Hide()
        self.find_password_ca.Hide()
        self.find_password_ca_.Hide()
        self.find_pa.Hide()
        self.find_re.Hide()

        self.find_password_card.Hide()
        self.find_password_card_.Hide()
        self.find_password_mail.Hide()
        self.find_password_mail_.Hide()
        self.find_yanzhengma.Hide()
        self.find_yanzhengma_.Hide()
        self.find_yanzhengma_j.Hide()
        self.fpass_s.Hide()
        self.fin_pass_s.Hide()
        self.fpass_s_.Hide()
        self.fin_pass_s_.Hide()
        self.find_p.Hide()
        self.find_re_.Hide()
        #业务办理页面
        self.button1.Hide()
        self.button2.Hide()
        self.button3.Hide()
        self.button4.Hide()
        self.button5.Hide()
        self.button6.Hide()
        self.button0.Hide()
        self.transfer_.Hide()
        self.zhuxiao.Hide()
        #主页面
        self.button7.Hide()
        self.button8.Hide()
        self.button9.Hide()
        #登录页面
        self.no_card.Hide()
        self.pa_card.Hide()
        self.in_no_card.Hide()
        self.in_pa_card.Hide()
        self.log.Hide()
        self.return_.Hide()
        self.label1.Hide()
        #开户界面
        self.mess.Hide()
        self.user_name.Hide()
        self.id_num.Hide()
        self.address.Hide()
        self.pass1.Hide()
        self.pass2.Hide()
        self.in_user_name.Hide()
        self.in_id_num.Hide()
        self.in_address.Hide()
        self.in_pass1.Hide()
        self.in_pass2.Hide()
        self.create.Hide()
        self.mail.Hide()
        self.in_mail.Hide()
        self.mail_yanzhengma.Hide()
        self.in_mail_yanzhengma.Hide()
        self.b_yanzhengma_.Hide()
        #存款
        self.save_.Hide()
        self.in_save.Hide()
        self.save.Hide()
        self.save_yu.Hide()
        self.save_yue.Hide()
        self.save_re.Hide()
        self._50_.Hide()
        self._100_.Hide()
        self._500_.Hide()
        self._1000_.Hide()
        self._2000_.Hide()
        # 取款
        self.withdraw_.Hide()
        self.in_withdraw.Hide()
        self.withdraw.Hide()
        self.withdraw_yu.Hide()
        self.withdraw_yue.Hide()
        self._50.Hide()
        self._100.Hide()
        self._500.Hide()
        self._1000.Hide()
        self._2000.Hide()
        #查询余额
        self.check_yu.Hide()
        self.check_ba.Hide()
        self.check_bal.Hide()
        #查询历史纪录
        self.date1.Hide()
        self.date2.Hide()
        self.date1_.Hide()
        self.date2_.Hide()
        self.label_date.Hide()
        self.check_his.Hide()
        self.grid.Hide()
        self.check_his_re.Hide()
        #查询账户
        self.id_find.Hide()
        self.in_id_num1.Hide()
        self.find.Hide()
        self.find_re.Hide()
        self.grid1.Hide()
        self.find_account_re.Hide()
        self.name_.Hide()
        self.sex_.Hide()
        self.age_.Hide()
        self.num_1.Hide()
        self.address_.Hide()
        self.name.Hide()
        self.sex.Hide()
        self.age.Hide()
        self.num1.Hide()
        self.address1.Hide()
        #修改个人信息
        self.change_information.Hide()
        self.change_information_.Hide()
        self.change_id.Hide()
        self.change_id_.Hide()
        self.change_name.Hide()
        self.change_name_.Hide()
        self.change_address.Hide()
        self.change_address_.Hide()
        self.change_re.Hide()
        #冻结
        self.card_num.Hide()
        self.card_num_.Hide()
        self.frozen.Hide()
        self.save_re.Hide()
        self.pass_.Hide()
        self.in_pass_.Hide()
        #解冻
        self.card_num_j.Hide()
        self.card_num_jd.Hide()
        self.unf.Hide()
        self.save_re.Hide()
        self.pass_j.Hide()
        self.in_pass_j.Hide()
        self.unf_yanzhengma.Hide()
        self.unf_yanzhengma_.Hide()
        self.unf_yanzhengma_j.Hide()
        #注销账户
        self.card_num_c.Hide()
        self.card_num_ca.Hide()
        self.cancel_.Hide()
        self.save_re.Hide()
        self.pass_c.Hide()
        self.in_pass_c.Hide()
        self.cancel_yanzhengma.Hide()
        self.cancel_yanzhengma_.Hide()
        self.cancel_yanzhengma_j.Hide()
        #转账
        self.tran_num_c.Hide()
        self.tran_num_ca.Hide()
        self.transfer_su.Hide()
        self.save_re.Hide()
        self.pass_tr.Hide()
        self.in_pass_tr.Hide()
        self.tran_money.Hide()
        self.tran_money_.Hide()
        self.tran_num_yue.Hide()
        self.tran_num_yue_.Hide()
        self._50_tr.Hide()
        self._100_tr.Hide()
        self._500_tr.Hide()
        self._1000_tr.Hide()
        self._2000_tr.Hide()
    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("00000.png")
        dc.DrawBitmap(bmp, 0, 0)
    def find_password(self,event):
        self.hide()
        self.find_password_ca.Show()
        self.find_password_ca_.Show()
        self.find_pa.Show()
        self.find_re.Show()
        self.find_password_ca_.Clear()
        self.find_yanzhengma_.Clear()
        self.fin_pass_s.Clear()
        self.fin_pass_s_.Clear()
    def find_password_(self,event):
        conn = psycopg2.connect(dbname="bank", user="joe", password="Bigdata@1234", host="119.3.227.175", port="5432")
        cor = conn.cursor()
        cor.execute('select cno from card')
        box_card = cor.fetchall()
        list_cno = []
        for cno in box_card:
            list_cno.append(cno[0])
        accout = self.find_password_ca_.GetValue()
        if accout == '':
            message1 = wx.MessageDialog(self, '请输入银行卡号', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        elif len(accout) != 19 or accout not in list_cno:
            message1 = wx.MessageDialog(self, '银行卡号输入有误，请重试', 'Error', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        else:
            self.hide()
            self.find_password_card.Show()
            self.find_password_card_.Show()
            self.find_password_mail.Show()
            self.find_password_mail_.Show()
            self.find_yanzhengma.Show()
            self.find_yanzhengma_.Show()
            self.find_yanzhengma_j.Show()
            self.fpass_s.Show()
            self.fin_pass_s.Show()
            self.fpass_s_.Show()
            self.fin_pass_s_.Show()
            self.find_p.Show()
            self.find_re_.Show()
            card_show=self.find_password_ca_.GetValue()
            self.find_password_card_.SetValue(card_show)
            self.ca_num = self.find_password_ca_.GetValue()
            select_pw = 'select email from card where cno=(%s)'
            cor.execute(select_pw, [self.ca_num])
            box_card_mail = cor.fetchall()
            list_mail = []
            for cno in box_card_mail:
                list_mail.append(cno[0])
            self.find_password_mail_.SetValue(list_mail[0])
            conn.close()
    def find_password_sure(self,event):
        find_yanzhengma=self.find_yanzhengma_.GetValue()
        pass1_=self.fin_pass_s.GetValue()
        pass2_ = self.fin_pass_s_.GetValue()
        if self.check_nums=='\n':
            message1 = wx.MessageDialog(self, '请先获得验证码', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        elif self.find_yanzhengma_.GetValue()=='':
            message1 = wx.MessageDialog(self, '请输入验证码', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        elif find_yanzhengma!=self.check_nums:
            message_e = wx.MessageDialog(self, '验证码错误', 'Errors', wx.OK | wx.ICON_INFORMATION)
            message_e.Center()
            message_e.ShowModal()
            self.find_yanzhengma_.Clear()
        elif pass1_.isdigit() == False:
            message1 = wx.MessageDialog(self, '密码只能包含数字', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.fin_pass_s.Clear()
            self.fin_pass_s_.Clear()
        elif len(pass1_)!=6 or len(pass2_)!=6 :
            message1 = wx.MessageDialog(self, '密码必须为6位', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.fin_pass_s.Clear()
            self.fin_pass_s_.Clear()
        elif pass1_!=pass2_:
            message_e = wx.MessageDialog(self, '两次密码输入不一致', 'Errors', wx.OK | wx.ICON_INFORMATION)
            message_e.Center()
            message_e.ShowModal()
            self.fin_pass_s.Clear()
            self.fin_pass_s_.Clear()
        else:
            self.check_nums = '\n'
            conn = psycopg2.connect(dbname="bank",user="joe",password="Bigdata@1234",host="119.3.227.175",port="5432")
            cur = conn.cursor()
            change_password_sql = "UPDATE Card SET password=(%s) WHERE cno=(%s) "
            sql_update = []
            sql_update.append(pass1_)
            sql_update.append(self.ca_num)
            cur.execute(change_password_sql, sql_update)
            conn.commit()
            conn.close()
            message1 = wx.MessageDialog(self, '重置密码成功', 'Successfully', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.fin_pass_s.Clear()
            self.fin_pass_s_.Clear()
            self.find_yanzhengma_.Clear()
            self.find_password(event=self.find_p)
    def mainwin(self,event):
        self.hide()
        self.label1.Show()
        self.button7.Show()
        self.button8.Show()
        self.find_pw.Show()
        self.find_password_ca_.Clear()
        self.button9.Show()
        self.in_no_card.Clear()
        self.in_pa_card.Clear()
        self.in_mail_yanzhengma.Clear()
        self.in_mail.Clear()
        self.in_user_name.Clear()
        self.in_id_num.Clear()
        self.in_address.Clear()
        self.in_pass1.Clear()
        self.in_pass2.Clear()
    def business_handing(self, event):
        self.hide()
        self.in_pass_j.Clear()
        self.unf_yanzhengma_.Clear()
        self.label1.Show()
        self.button1.Show()
        self.button2.Show()
        self.button3.Show()
        self.button4.Show()
        self.button5.Show()
        self.button6.Show()
        self.button0.Show()
        self.transfer_.Show()
        self.zhuxiao.Show()
        self.save_yue.Clear()
        self.withdraw_yue.Clear()
        self.check_bal.Clear()
        self.in_save.Clear()
        self.in_withdraw.Clear()
        self.check_bal.Clear()
        self.tran_money_.Clear()
        self.tran_num_ca.Clear()
        self.in_pass_tr.Clear()
    def log_che(self, event):
        conn = psycopg2.connect(dbname="bank",user="joe",password="Bigdata@1234",host="119.3.227.175",port="5432")
        cor = conn.cursor()
        cor.execute('select cno from card')
        box_card = cor.fetchall()
        list_cno = []
        for cno in box_card:
            list_cno.append(cno[0])
        num = self.in_no_card.GetValue()
        password_s = self.in_pa_card.GetValue()
        if len(num)!=19 or num not in list_cno:
            message1 = wx.MessageDialog(self, '银行卡号输入有误，请重试', 'Error', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        else:
            sql = 'select password from Card where cno=(%s)' % str(num)
            cor.execute(sql)
            list = []
            for password in cor.fetchall():
                list.append(password)
            self.password_ = str(' '.join(list[0]))
            if self.password_ == password_s:
                self.in_pa_card.Clear()
                self.business_handing(event=self.log)
            else:
                message1 = wx.MessageDialog(self, '密码错误，请重新输入', 'Warnings', wx.OK | wx.ICON_INFORMATION)
                self.in_pa_card.Clear()
                message1.Center()
                message1.ShowModal()
            conn.commit()
            conn.close()
    def login_in(self,event):
        self.hide()
        self.no_card.Show()
        self.pa_card.Show()
        self.in_no_card.Show()
        self.in_pa_card.Show()
        self.log.Show()
        self.return_.Show()
    def judge_date(self,ye, mon, day):
        dates = []
        ye = int(ye)
        mon = int(mon)
        day = int(day)
        dates.append(ye)
        dates.append(mon)
        dates.append(day)
        try:
            a = date(dates[0], dates[1], dates[2])
        except ValueError:
            return 1
        else:
            return -1
    def create_account(self, event):
        em=self.in_mail.GetValue()
        idnum = self.in_id_num.GetValue()
        username = self.in_user_name.GetValue()
        add = self.in_address.GetValue()
        pass1 = self.in_pass1.GetValue()
        pass2 = self.in_pass2.GetValue()
        ya=self.in_mail_yanzhengma.GetValue()
        if username == '':
            message1 = wx.MessageDialog(self, '姓名不能为空', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        elif len(idnum)!=18  or int(idnum[6:10])<1753 or (self.judge_date(idnum[6:10],idnum[10:12], idnum[12:14])==1) :
            message1 = wx.MessageDialog(self, '身份证格式不正确', 'Error', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.in_id_num.Clear()
        elif add == '':
            message1 = wx.MessageDialog(self, '居住地址不能为空', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        elif pass1.isdigit() == False:
            message1 = wx.MessageDialog(self, '密码只能包含数字', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.in_pass1.Clear()
            self.in_pass2.Clear()
        elif len(pass1)!=6 or len(pass2)!=6:
            message1 = wx.MessageDialog(self, '密码必须为6位', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.in_pass1.Clear()
            self.in_pass2.Clear()
        elif em == '':
            message1 = wx.MessageDialog(self, '请输入邮箱', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        elif ya == '':
            message1 = wx.MessageDialog(self, '请输入验证码', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        elif pass1!=pass2:
            message_e = wx.MessageDialog(self, '两次密码输入不一致', 'Errors', wx.OK | wx.ICON_INFORMATION)
            message_e.Center()
            message_e.ShowModal()
            self.in_pass1.Clear()
            self.in_pass2.Clear()
        elif self.check_nums=='\n':
            message1 = wx.MessageDialog(self, '请先获得验证码', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        elif self.in_mail_yanzhengma.GetValue()!=self.check_nums:
            message_e = wx.MessageDialog(self, '验证码错误', 'Errors', wx.OK | wx.ICON_INFORMATION)
            message_e.Center()
            message_e.ShowModal()
            self.in_mail_yanzhengma.Clear()
        else:
            bno = '00000001'
            conn = psycopg2.connect(dbname="bank",user="joe",password="Bigdata@1234",host="119.3.227.175",port="5432")
            cur = conn.cursor()
            cur.execute('select uno from Users')
            uno_list = []
            for box in cur.fetchall():
                uno_list.append(box[0])
            if idnum not in uno_list:
                if int(idnum[16]) % 2 != 0:
                    sex = '男'
                else:
                    sex = '女'
                birth_date = idnum[6:14]
                sql1 = "insert into Users values(%s,%s,%s,%s,%s)"
                sql_insert = [idnum, username, sex, birth_date, add]
                cur.execute(sql1, sql_insert)
                conn.commit()
            else:
                save_sql = "UPDATE users SET u_address=(%s) WHERE uno=(%s) "
                list1 = []
                list1.append(add)
                list1.append(idnum)
                cur.execute(save_sql, list1)
                save_sql = "UPDATE users SET uname=(%s) WHERE uno=(%s) "
                list2 = []
                list2.append(username)
                list2.append(idnum)
                cur.execute(save_sql, list2)
                conn.commit()
            c_num = random.randint(1000000000000000000, 9223372036854775805)
            # 判断卡号是否在card表中已经存在
            select = 'select cno from card'
            cur.execute(select)
            list_1 = []
            box_c_num = cur.fetchall()
            for i in box_c_num:
                print(i[0])
                list_1.append(i[0])
            while 1:
                if c_num in list_1:
                    c_num = random.randint(100000000000000000, 9223372036854775805)
                else:
                    break
            time = datetime.now()
            sql2 = "insert into Card values(%s,%s,%s,%s,%s,%s,%s,%s)"
            sql_insert1 = [c_num, '0', pass1, bno, 'using', idnum,time,self.email]
            cur.execute(sql2, sql_insert1)
            conn.commit()
            message_s = wx.MessageDialog(self, '开户成功,卡号：'+str(c_num), 'Successfully', wx.OK | wx.ICON_INFORMATION)
            message_s.Center()
            message_s.ShowModal()
            self.in_user_name.Clear()
            self.in_id_num.Clear()
            self.in_address.Clear()
            self.in_pass1.Clear()
            self.in_pass2.Clear()
            self.mainwin(event=self.return_)
            # 关闭数据库的连接
            conn.close()
            self.check_nums = '\n'
    def open_account(self, event):
        self.hide()
        self.mess.Show()
        self.user_name.Show()
        self.id_num.Show()
        self.address.Show()
        self.pass1.Show()
        self.pass2.Show()
        self.in_user_name.Show()
        self.in_id_num.Show()
        self.in_address.Show()
        self.in_pass1.Show()
        self.in_pass2.Show()
        self.create.Show()
        self.return_.Show()
        self.mail.Show()
        self.in_mail.Show()
        self.mail_yanzhengma.Show()
        self.in_mail_yanzhengma.Show()
        self.b_yanzhengma_.Show()
    def save_money(self, event):
        conn = psycopg2.connect(dbname="bank",user="joe",password="Bigdata@1234",host="119.3.227.175", port="5432")
        cur = conn.cursor()
        accout = self.in_no_card.GetValue()
        frozen_sql = "select state from card where cno=(%s) "
        cur.execute(frozen_sql, [accout])
        box1 = cur.fetchall()
        for state in box1:
            print(state[0])
        select_Card = 'select money from Card where cno= (%s)'
        cur.execute(select_Card, [accout])
        box = cur.fetchall()
        for money_ in box:
            print(money_[0])
        self.save_yue.SetValue(str(money_[0]))
        conn.commit()
        conn.close()
        if state[0]=='using':
            self.hide()
            self.save_.Show()
            self.in_save.Show()
            self.save.Show()
            self.save_yue.Show()
            self.save_re.Show()
            self.save_yu.Show()
            self._50_.Show()
            self._100_.Show()
            self._500_.Show()
            self._1000_.Show()
            self._2000_.Show()
        else:
            message1 = wx.MessageDialog(self, '账户已被冻结', 'Warnings', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
    def clear_yue1(self, event):
        self.save_yue.Clear()
        self.withdraw_yue.Clear()
        self.check_bal.Clear()
    def save_money_che(self,event):
        accout = self.in_no_card.GetValue()
        conn = psycopg2.connect(dbname="bank",user="joe",password="Bigdata@1234",host="119.3.227.175",port="5432")
        cur = conn.cursor()
        money=self.in_save.GetValue()
        money=float(money)
        if money < 0:
            message1 = wx.MessageDialog(self, '输入金额有误,请重新输入', 'Error', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.in_save.Clear()
        else:
            # 查询余额
            select_Card = 'select money from Card where cno= (%s)'
            cur.execute(select_Card, [accout])
            box = cur.fetchall()
            for money_ in box:
                pass
            # 存款的实现
            save_sql = "UPDATE Card SET money=(%s) WHERE cno=(%s) "
            sql_update = []
            sql_update.append(money_[0] + money)
            sql_update.append(accout)
            cur.execute(save_sql, sql_update)
            # 在历史记录插入该操作
            time = datetime.now()
            sql_insert_to_history = "insert into History values(%s,%s,%s,%s,%s,%s,%s)"
            sql_insert = [accout,'00000001', money, money_[0], money_[0] + money, time,'存入']
            cur.execute(sql_insert_to_history, sql_insert)
            conn.commit()
            conn.close()
            message1 = wx.MessageDialog(self, '存款成功', 'Successfully', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.save_yue.SetValue(str(money_[0] + money))
    def withdraw_money(self, event):
        conn = psycopg2.connect(dbname="bank",user="joe",password="Bigdata@1234",host="119.3.227.175",port="5432")
        cur = conn.cursor()
        accout = self.in_no_card.GetValue()
        frozen_sql = "select state from card where cno=(%s) "
        cur.execute(frozen_sql, [accout])
        box1 = cur.fetchall()
        for state in box1:
            pass
        if state[0] == 'using':
            self.hide()
            self.withdraw_.Show()
            self.in_withdraw.Show()
            self.withdraw.Show()
            self.withdraw_yue.Show()
            self.withdraw_yu.Show()
            self.save_re.Show()
            self._50.Show()
            self._100.Show()
            self._500.Show()
            self._1000.Show()
            self._2000.Show()
            accout = self.in_no_card.GetValue()
            select = 'select money from Card where cno= (%s)'
            cur.execute(select, [accout])
            cards = cur.fetchall()
            for money in cards:
                pass
            self.check_bal.SetValue(str(money[0]))
            self.withdraw_yue.SetValue(str(money[0]))
            conn.commit()
            conn.close()
        else:
            message1 = wx.MessageDialog(self, '账户已被冻结', 'Warnings', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
    def withdraw_money_che(self,event):
        money=self.in_withdraw.GetValue()
        money = float(money)
        if money < 0:
            message1 = wx.MessageDialog(self, '输入金额有误,请重新输入', 'Error', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.in_withdraw.Clear()
        else:
            money=-money
            conn = psycopg2.connect(dbname="bank",user="joe",password="Bigdata@1234",host="119.3.227.175",port="5432")
            accout = self.in_no_card.GetValue()
            cur = conn.cursor()
            # 查询余额
            select_Card = 'select money from Card where cno= (%s)'
            cur.execute(select_Card, [accout])
            box = cur.fetchall()
            for money_ in box:
                pass
            # 存款的实现
            sql_update = []
            sql_update.append(money_[0] + money)
            if (sql_update[0] >= 0):
                save_sql = "UPDATE Card SET money=(%s) WHERE cno=(%s) "
                sql_update.append(accout)
                cur.execute(save_sql, sql_update)
                # 在历史记录插入该操作
                time = datetime.now()
                sql_insert_to_history = "insert into History values(%s,%s,%s,%s,%s,%s,%s)"
                sql_insert = [accout, '00000001', money, money_[0], money_[0] + money, time,'取款']
                cur.execute(sql_insert_to_history, sql_insert)
                conn.commit()
                conn.close()
                message1 = wx.MessageDialog(self, '取款成功', 'Successfully', wx.OK | wx.ICON_INFORMATION)
                message1.Center()
                message1.ShowModal()
                self.withdraw_yue.SetValue(str(money_[0] + money))
                self.in_withdraw.Clear()
            else:
                message1 = wx.MessageDialog(self, '取款金额大于存款金额，取款失败', 'Warnings', wx.OK | wx.ICON_INFORMATION)
                self.in_withdraw.Clear()
                message1.Center()
                message1.ShowModal()
    def check_balance(self,event):
        self.hide()
        self.check_ba.Show()
        self.check_bal.Show()
        self.check_yu.Show()
        self.save_re.Show()
    def check_balance_che(self, event):
        conn = psycopg2.connect(dbname="bank",user="joe",password="Bigdata@1234",host="119.3.227.175",port="5432")
        cur = conn.cursor()
        accout = self.in_no_card.GetValue()
        select = 'select money from Card where cno= (%s)'
        cur.execute(select, [accout])
        cards = cur.fetchall()
        print(accout)
        for money in cards:
            pass
        self.check_bal.SetValue(str(money[0]))
        conn.commit()
        conn.close()
    def check_history(self,event):
        self.hide()
        self.date1.Show()
        self.date2.Show()
        self.date1_.Show()
        self.date2_.Show()
        self.label_date.Show()
        self.check_his.Show()
        self.save_re.Show()
        self.grid.Hide()
        self.check_his_re.Close()
    def che_his_mainwin(self,event):
        conn = psycopg2.connect(dbname="bank",user="joe",password="Bigdata@1234",host="119.3.227.175",port="5432")
        cur = conn.cursor()
        accout = self.in_no_card.GetValue()
        first_time = str(self.date1.GetValue())
        last_time = str(self.date2.GetValue())
        first_time=first_time.replace('/','-')
        last_time = last_time.replace('/','-')
        last_time=re.findall('(.*\s)',last_time)
        last_time[0]=last_time[0]+'23:59:59'
        first_time=datetime.strptime(first_time, "%Y-%m-%d %H:%M:%S")
        last_time = datetime.strptime(last_time[0], "%Y-%m-%d %H:%M:%S")
        if first_time>last_time:
            message1 = wx.MessageDialog(self, '起始日期不能超前于结束日期', 'Error', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        else:
            last_time=str(last_time)
            select_History = 'select * from History where cno=(%s) and operating_time between (%s) and (%s)'
            select_History_sql = [accout, first_time, last_time]
            cur.execute(select_History, select_History_sql)
            history = cur.fetchall()
            self.hide()
            self.grid = wx.grid.Grid(self.startwindow, id=wx.ID_ANY, size=(800, 460), pos=(10, 10))
            self.grid.CreateGrid(len(history) + 1, 7)
            print(len(history))
            self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            self.grid.EnableEditing(False)
            self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            self.grid.SetColSize(0, 150)
            self.grid.SetColSize(1, 90)
            self.grid.SetColSize(2, 90)
            self.grid.SetColSize(3, 100)
            self.grid.SetColSize(4, 100)
            self.grid.SetColSize(5, 100)
            self.grid.SetColSize(6, 150)
            self.grid.HideColLabels()
            self.grid.HideRowLabels()
            # 第1行数据
            self.grid.SetCellValue(0, 0, "日期")
            self.grid.SetCellValue(0, 1, "转入（元）")
            self.grid.SetCellValue(0, 2, "转出（元）")
            self.grid.SetCellValue(0, 3, "原有余额（元）")
            self.grid.SetCellValue(0, 4, "现有余额（元）")
            self.grid.SetCellValue(0, 5, "操作")
            self.grid.SetCellValue(0, 6, "对方账户")
            for a in range(0, len(history)):
                if history[a][2] >= 0:
                    self.grid.SetCellValue(a + 1, 0, (str(history[a][5]))[0:19])
                    self.grid.SetCellValue(a + 1, 1, str(history[a][2]))
                    self.grid.SetCellValue(a + 1, 2, '-')
                    self.grid.SetCellValue(a + 1, 3, str(history[a][3]))
                    self.grid.SetCellValue(a + 1, 4, str(history[a][4]))
                    self.grid.SetCellValue(a + 1, 5, str(history[a][6]))
                    self.grid.SetCellValue(a + 1, 6, str(history[a][7]))
                elif history[a][2] < 0:
                    self.grid.SetCellValue(a + 1, 0, (str(history[a][5]))[0:19])
                    self.grid.SetCellValue(a + 1, 1, '-')
                    self.grid.SetCellValue(a + 1, 2, str(-history[a][2]))
                    self.grid.SetCellValue(a + 1, 3, str(history[a][3]))
                    self.grid.SetCellValue(a + 1, 4, str(history[a][4]))
                    self.grid.SetCellValue(a + 1, 5, str(history[a][6]))
                    self.grid.SetCellValue(a + 1, 6, str(history[a][7]))
                if str(history[a][6])!='转账':
                    self.grid.SetCellValue(a + 1, 6,'-')
            conn.commit()
            conn.close()
            self.check_his_re.Show()
    def find_account(self,event):
        self.hide()
        self.in_id_num1.Clear()
        self.id_find.Show()
        self.in_id_num1.Show()
        self.find.Show()
        self.find_re.Show()
    def find_account_(self, event):
        id_=self.in_id_num1.GetValue()
        conn = psycopg2.connect(dbname="bank", user="joe", password="Bigdata@1234", host="119.3.227.175", port="5432")
        cur = conn.cursor()
        cur.execute('select uno from users')
        box_uno = cur.fetchall()
        list_uno = []
        for uno in box_uno:
            list_uno.append(uno[0])
        if len(id_)!=18:
            message1 = wx.MessageDialog(self, '身份证账号有误', 'Error', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        elif id_ not in list_uno:
            message1 = wx.MessageDialog(self, '还未办理银行卡', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        else:
            id_num=self.in_id_num1.GetValue()
            select1 = 'select * from Users where uno= (%s)'
            cur.execute(select1, [id_num])
            box = cur.fetchall()
            for user in box:
                pass
            date1 = datetime.strptime(str(user[3]), '%Y-%m-%d %H:%M:%S')
            days = (datetime.now() - date1).days
            age = int((int(days) / 365))
            self.hide()
            self.change_information.Show()
            self.name_.Show()
            self.sex_.Show()
            self.age_.Show()
            self.num_1.Show()
            self.address_.Show()
            self.name_.SetValue(user[1])
            self.sex_.SetValue(user[2])
            self.age_.SetValue(str(age))
            self.num_1.SetValue(user[0])
            self.address_.SetValue(user[4])
            self.name.Show()
            self.sex.Show()
            self.age.Show()
            self.num1.Show()
            self.address1.Show()
            self.user_na=user[1]
            self.user_ad=user[4]
            select = 'select * from Card where uno= (%s)'
            cur.execute(select, [id_num])
            cards = cur.fetchall()
            self.grid1 = wx.grid.Grid(self.startwindow, id=wx.ID_ANY, size=(775, 340), pos=(10, 190))
            self.grid1.CreateGrid(len(cards)+1, 6)
            self.grid1.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            # 第1行数据
            self.grid1.SetCellValue(0, 0, "卡号")
            self.grid1.SetCellValue(0, 1, "余额（单位：元）")
            self.grid1.SetCellValue(0, 2, "开户日期")
            self.grid1.SetCellValue(0, 3, "网点编号")
            self.grid1.SetCellValue(0, 4, "银行卡状态")
            self.grid1.SetCellValue(0, 5, "邮箱")
            self.grid1.EnableEditing(False)
            # 第2行及其以后数据
            self.grid1.SetColSize(0, 190)
            self.grid1.SetColSize(1, 110)
            self.grid1.SetColSize(2, 150)
            self.grid1.SetColSize(3, 70)
            self.grid1.SetColSize(4, 70)
            self.grid1.SetColSize(5, 150)
            self.grid1.HideColLabels()
            self.grid1.HideRowLabels()
            for a in range(0, len(cards)):
                self.grid1.SetCellValue(a + 1, 0, str(cards[a][0]))
                self.grid1.SetCellValue(a + 1, 1, str(cards[a][1]))
                self.grid1.SetCellValue(a + 1, 2, str(cards[a][6]))
                self.grid1.SetCellValue(a + 1, 3, str(cards[a][3]))
                self.grid1.SetCellValue(a + 1, 4, str(cards[a][4]))
                self.grid1.SetCellValue(a + 1, 5, str(cards[a][7]))
            conn.commit()
            conn.close()
            self.find_account_re.Show()
    def blocked_account_show(self, event):
        self.hide()
        self.card_num.Show()
        self.card_num_.Show()
        self.frozen.Show()
        self.save_re.Show()
        self.pass_.Show()
        self.in_pass_.Show()
        num = self.in_no_card.GetValue()
        self.card_num_.SetValue(num)
    def blocked_account(self, event):
        pass_a = self.in_pass_.GetValue()
        accout = self.in_no_card.GetValue()
        conn = psycopg2.connect(dbname="bank", user="joe", password="Bigdata@1234", host="119.3.227.175", port="5432")
        # 创建游标对象，相当于ADO的记录集
        cor = conn.cursor()
        sql = 'select password from Card where cno=(%s)' % str(accout)
        cor.execute(sql)
        list = []
        for password in cor.fetchall():
            list.append(password)
        password_ = str(' '.join(list[0]))
        if password_ == pass_a:
            cur = conn.cursor()
            frozen_sql = "UPDATE Card SET state='frozen' WHERE cno=(%s) "
            cur.execute(frozen_sql, [accout])
            conn.commit()
            print('abc,鼠标左键按下')
            self.in_pa_card.Clear()
            message1 = wx.MessageDialog(self, '冻结成功', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.in_pass_.Clear()
            self.business_handing(event=self.log)
        else:
            message1 = wx.MessageDialog(self, '密码错误，请重新输入', 'Warnings', wx.OK | wx.ICON_INFORMATION)
            self.in_pass_.Clear()
            message1.Center()
            message1.ShowModal()
    def unfreeze_account_show(self,event):
        self.hide()
        self.card_num_j.Show()
        self.card_num_jd.Show()
        self.unf.Show()
        self.save_re.Show()
        self.pass_j.Show()
        self.in_pass_j.Show()
        self.unf_yanzhengma.Show()
        self.unf_yanzhengma_.Show()
        self.unf_yanzhengma_j.Show()
        num = self.in_no_card.GetValue()
        self.card_num_jd.SetValue(num)
    def unfreeze_account(self,event):
        accout = self.in_no_card.GetValue()
        password_s = self.password_
        self.card_num_jd.SetValue(accout)
        yanzhengma=self.unf_yanzhengma_.GetValue()
        pa=self.in_pass_j.GetValue()
        if pa==password_s and yanzhengma==self.check_nums:
            conn = psycopg2.connect(dbname="bank", user="joe", password="Bigdata@1234", host="119.3.227.175",port="5432")
            cur = conn.cursor()
            frozen_sql = "UPDATE Card SET state='using' WHERE cno=(%s) "
            cur.execute(frozen_sql, [accout])
            conn.commit()
            conn.close()
            self.unf_yanzhengma_.Clear()
            self.in_pass_j.Clear()
            message1 = wx.MessageDialog(self, '解冻成功', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.in_pass_.Clear()
            self.business_handing(event=self.log)
            self.check_nums = '\n'
        else:
            self.unf_yanzhengma_.Clear()
            self.in_pass_j.Clear()
            message1 = wx.MessageDialog(self, '密码或验证码错误', 'Errors', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
    def get_yanzhengma(self,event):
        message1 = wx.MessageDialog(self, '验证码已发送，请注意查收', 'Message', wx.OK | wx.ICON_INFORMATION)
        message1.Center()
        message1.ShowModal()
        conn = psycopg2.connect(dbname="bank",user="joe",password="Bigdata@1234",host="119.3.227.175",port="5432")
        cur = conn.cursor()
        accout =self.in_no_card.GetValue()
        select = 'select * from card where cno= (%s)'
        cur.execute(select, [accout])
        box = cur.fetchall()
        for email in box:
            pass
        my_sender = 'kilven7769@foxmail.com'  # 发件人邮箱账号
        my_pass = 'uypiyrhaakuljfca'  # 发件人邮箱的授权码
        my_user = email[7]  # 收件人邮箱账号，我这边发送给自己
        self.check_nums = str(random.randint(100000, 999999))
        msg = MIMEText('【357银行】您的验证码为：' + str(self.check_nums) + '请妥善保管', 'plain', 'utf-8')
        msg['From'] = formataddr(["From nicead.top", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "验证码"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
        conn.close()
    def get_yanzhengma_(self,event):
        message1 = wx.MessageDialog(self, '验证码已发送，请注意查收', 'Message', wx.OK | wx.ICON_INFORMATION)
        message1.Center()
        message1.ShowModal()
        self.email=self.in_mail.GetValue()
        my_sender = 'kilven7769@foxmail.com'
        my_pass = 'uypiyrhaakuljfca'
        my_user = self.email
        self.check_nums = str(random.randint(100000, 999999))
        msg = MIMEText('【357银行】您的验证码为：' + str(self.check_nums) + '请妥善保管', 'plain', 'utf-8')
        msg['From'] = formataddr(["From nicead.top", my_sender])
        msg['To'] = formataddr(["FK", my_user])
        msg['Subject'] = "验证码"
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
    def get_yanzhengma_find_(self, event):
        message1 = wx.MessageDialog(self, '验证码已发送，请注意查收', 'Message', wx.OK | wx.ICON_INFORMATION)
        message1.Center()
        message1.ShowModal()
        find_email = self.find_password_mail_.GetValue()
        my_sender = 'kilven7769@foxmail.com'  # 发件人邮箱账号
        my_pass = 'uypiyrhaakuljfca'  # 发件人邮箱的授权码
        my_user = find_email  # 收件人邮箱账号，我这边发送给自己
        self.check_nums = str(random.randint(100000, 999999))
        msg = MIMEText('【357银行】您的验证码为：' + str(self.check_nums) + '请妥善保管', 'plain', 'utf-8')
        msg['From'] = formataddr(["From nicead.top", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "验证码"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
    def cancel_show(self, event):
        conn = psycopg2.connect(dbname="bank", user="joe", password="Bigdata@1234", host="119.3.227.175", port="5432")
        cur = conn.cursor()
        accout = self.in_no_card.GetValue()
        select = 'select money from Card where cno= (%s)'
        cur.execute(select, [accout])
        cards = cur.fetchall()
        conn.close()
        for money in cards:
            pass
        if money[0]>0:
            message1 = wx.MessageDialog(self, '账户有余额，无法注销', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        else:
            self.hide()
            self.card_num_c.Show()
            self.card_num_ca.Show()
            self.cancel_.Show()
            self.save_re.Show()
            self.pass_c.Show()
            self.in_pass_c.Show()
            self.cancel_yanzhengma.Show()
            self.cancel_yanzhengma_.Show()
            self.cancel_yanzhengma_j.Show()
            num = self.in_no_card.GetValue()
            self.card_num_ca.SetValue(num)
    def cancel(self, event):
        accout = self.in_no_card.GetValue()
        password_s = self.password_
        self.card_num_jd.SetValue(accout)
        yanzhengma = self.cancel_yanzhengma_.GetValue()
        pa = self.in_pass_c.GetValue()
        if pa == password_s and yanzhengma == self.check_nums:
            conn = psycopg2.connect(dbname="bank", user="joe", password="Bigdata@1234", host="119.3.227.175",port="5432")
            cur = conn.cursor()
            sql_delete1 = 'delete  from History where cno=(%s)' % str(accout)
            cur.execute(sql_delete1)
            sql_delete2 = 'delete  from Card where cno=(%s)' % str(accout)
            cur.execute(sql_delete2)
            conn.commit()
            conn.close()
            self.unf_yanzhengma_.Clear()
            self.in_pass_c.Clear()
            message1 = wx.MessageDialog(self, '注销完成', 'Message', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.in_pass_.Clear()
            self.mainwin(event=self.log)
            self.check_nums = '\n'
        else:
            self.cancel_yanzhengma_.Clear()
            self.in_pass_c.Clear()
            message1 = wx.MessageDialog(self, '密码或验证码错误', 'Errors', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
    def _50sel(self,event):
        self.in_withdraw.SetValue('50')
        self.in_save.SetValue('50')
        self.tran_money_.SetValue('50')
    def _100sel(self,event):
        self.in_withdraw.SetValue('100')
        self.in_save.SetValue('100')
        self.tran_money_.SetValue('100')
    def _500sel(self,event):
        self.in_withdraw.SetValue('500')
        self.in_save.SetValue('500')
        self.tran_money_.SetValue('500')
    def _1000sel(self,event):
        self.in_withdraw.SetValue('1000')
        self.in_save.SetValue('1000')
        self.tran_money_.SetValue('1000')
    def _2000sel(self,event):
        self.in_withdraw.SetValue('2000')
        self.in_save.SetValue('2000')
        self.tran_money_.SetValue('2000')
    def change_information_show(self,event):
       self.hide()
       self.change_information_.Show()
       self.change_id.Show()
       self.change_id_.Show()
       self.change_name.Show()
       self.change_name_.Show()
       self.change_address.Show()
       self.change_address_.Show()
       self.change_re.Show()
       self.id=self.in_id_num1.GetValue()
       self.change_id_.SetValue(self.id)
       self.change_name_.SetValue(self.user_na)
       self.change_address_.SetValue(self.user_ad)
    def change_information_e(self,event):
        new_address=self.change_address_.GetValue()
        new_name=self.change_name_.GetValue()
        conn = psycopg2.connect(dbname="bank",user="joe",password="Bigdata@1234",host="119.3.227.175",port="5432")
        cur = conn.cursor()
        save_sql = "UPDATE users SET uname=(%s),u_address=(%s) WHERE uno=(%s) "
        list1 = []
        list1.append(new_name)
        list1.append(new_address)
        list1.append(self.id)
        cur.execute(save_sql, list1)
        conn.commit()
        conn.close()
        message1 = wx.MessageDialog(self, '修改成功', 'Successfully', wx.OK | wx.ICON_INFORMATION)
        message1.Center()
        message1.ShowModal()
        self.find_account_(event=self.change_information_)
    def transfer_show(self,event):
        conn = psycopg2.connect(dbname="bank", user="joe", password="Bigdata@1234", host="119.3.227.175", port="5432")
        cur = conn.cursor()
        accout = self.in_no_card.GetValue()
        frozen_sql = "select state from card where cno=(%s) "
        cur.execute(frozen_sql, [accout])
        box1 = cur.fetchall()
        for state in box1:
            pass
        select_Card = 'select money from Card where cno= (%s)'
        cur.execute(select_Card, [accout])
        box = cur.fetchall()
        for money_ in box:
            pass
        self.tran_num_yue_.SetValue(str(money_[0]))
        conn.commit()
        conn.close()
        if state[0] == 'using':
            self.hide()
            self.tran_num_c.Show()
            self.tran_num_ca.Show()
            self.transfer_su.Show()
            self.save_re.Show()
            self.pass_tr.Show()
            self.in_pass_tr.Show()
            self.tran_money.Show()
            self.tran_money_.Show()
            self.tran_num_yue.Show()
            self.tran_num_yue_.Show()
            self._50_tr.Show()
            self._100_tr.Show()
            self._500_tr.Show()
            self._1000_tr.Show()
            self._2000_tr.Show()
        else:
            message1 = wx.MessageDialog(self, '账户已被冻结', 'Warnings', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
    def transfer(self,event):
        conn = psycopg2.connect(dbname="bank",user="joe",password="Bigdata@1234",host="119.3.227.175",port="5432")
        cur = conn.cursor()
        cur.execute('select cno from card')
        box_card = cur.fetchall()
        list_cno = []
        for cno in box_card:
            list_cno.append(cno[0])
        accout = self.in_no_card.GetValue()
        accout_s=self.tran_num_ca.GetValue()
        password_tr = self.in_pass_tr.GetValue()
        trans_money=self.tran_money_.GetValue()
        trans_money=float(trans_money)
        if trans_money<0:
            message1 = wx.MessageDialog(self, '输入金额有误,请重新输入', 'Error', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
            self.tran_money_.Clear()
            self.in_pass_tr.Clear()
        elif accout_s not in list_cno:
            message1 = wx.MessageDialog(self, '收款方账号不存在', 'Error', wx.OK | wx.ICON_INFORMATION)
            message1.Center()
            message1.ShowModal()
        else:
            select_Card1 = 'select money from Card where cno= (%s)'
            cur.execute(select_Card1, [accout])
            box1 = cur.fetchall()
            for money in box1:
                print(money[0])
            sql = 'select password from Card where cno=(%s)' % str(accout)
            cur.execute(sql)
            list = []
            for password in cur.fetchall():
                list.append(password)
            self.password_ = str(' '.join(list[0]))
            select_name = 'select uname from card,users where users.uno=card.uno and  cno= (%s) '
            cur.execute(select_name, [accout_s])
            box0 = cur.fetchall()
            list_name = []
            for name in box0:
                list_name.append(name[0])
                if len(name[0]) == 2:
                    pass
                elif len(name[0]) >= 2:
                    list_name[0] = list_name[0].replace(list_name[0][-2], '*')
            if (money[0] - trans_money) < 0 or password_tr!=self.password_:
                message1 = wx.MessageDialog(self, '余额不足或密码错误', 'Errors', wx.OK | wx.ICON_INFORMATION)
                message1.Center()
                message1.ShowModal()
                self.tran_money_.Clear()
                self.in_pass_tr.Clear()
            else:
                dlg = wx.MessageDialog(self, '收款方姓名：'+str(list_name[0])+'是否继续转账', 'Message', wx.YES_NO | wx.ICON_QUESTION)
                if dlg.ShowModal() == wx.ID_YES:
                    select_Card2 = 'select money from Card where cno= (%s)'
                    cur.execute(select_Card2, [accout_s])
                    box2 = cur.fetchall()
                    for money_s in box2:
                        pass
                    # 取出操作
                    save_sql = "UPDATE Card SET money=(%s) WHERE cno=(%s) "
                    sql_update = []
                    sql_update.append(money[0] - trans_money)
                    sql_update.append(accout)
                    cur.execute(save_sql, sql_update)
                    # 在历史记录插入该操作
                    time = datetime.now()
                    sql_insert_to_history = "insert into History values(%s,%s,%s,%s,%s,%s,%s,%s)"
                    sql_insert = [accout,'00000001', -trans_money, money[0], money[0] - trans_money, time,'转账',accout_s]
                    cur.execute(sql_insert_to_history, sql_insert)
                    conn.commit()
                    # 存款的实现
                    save_sql = "UPDATE Card SET money=(%s) WHERE cno=(%s) "
                    sql_update1 = []
                    sql_update1.append(money_s[0] + trans_money)
                    sql_update1.append(accout_s)
                    cur.execute(save_sql, sql_update1)
                    # 在历史记录插入该操作
                    time = datetime.now()
                    sql_insert_to_history = "insert into History values(%s,%s,%s,%s,%s,%s,%s,%s)"
                    sql_insert = [accout_s,'00000001', trans_money, money_s[0], money_s[0] + trans_money, time,'转账',accout]
                    cur.execute(sql_insert_to_history, sql_insert)
                    conn.commit()
                    dlg.Destroy()
                    message1 = wx.MessageDialog(self, '转账成功', 'Successfully', wx.OK | wx.ICON_INFORMATION)
                    message1.Center()
                    message1.ShowModal()
                    self.tran_money_.Clear()
                    self.tran_num_ca.Clear()
                    self.in_pass_tr.Clear()
                    select_Card = 'select money from Card where cno= (%s)'
                    cur.execute(select_Card, [accout])
                    box = cur.fetchall()
                    for money_ in box:
                        pass
                    self.tran_num_yue_.SetValue(str(money_[0]))
                    conn.commit()
                    conn.close()
                else:
                    dlg.Destroy()

class myApp(wx.App):
    def  OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True
if __name__ == '__main__':
    app = myApp()
    app.MainLoop()
    if app.frame.exit_1==1:
        app.ExitOnFrameDelete()
