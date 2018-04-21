#! usr/bin/python
#coding=utf-8

'''
模块名称：
模块主要功能：
模块实现的方法：
模块对外接口：
模块作者：
编写时间：
修改说明：
修改时间：
'''

#验证数据合法性   取出指令号  按照指令号调用不同的方法进行解析


class   dataParser(object):
    def __init__(self, data):
        self.sourceDate = data
        self.SleepCmd = 0x00




    # 7878  0d  01  0356314041420996  3a  0d0a
    # 指令号是0x14时的解析
    # LBS个数：05 为基站数量，基站数量最小为2个
    # MCCMNC：mcc2byte，mnc1byte 01CC00为46000

    def processSleepCmd(self):
        content = {'SleepCmd': 0x01}
        return self.get_callback(content)

    # 指令是0x17时的解析
    def processWifiCmd(self):
        # 离线wifi所有数据
        wifi_data = self.sourceDate[4].split(' ')

        # wifi数量
        num = self.sourceDate[2]
        # 日期时间
        time = wifi_data[0]
        # wifi数据3- -2
        demo_wifi = wifi_data[3:-1]
        wifi = ' '.join(demo_wifi)
        # LBS数据
        demo_LBS = []
        for i in range(3, 10):
            demo_LBS.append(i)
        LBS = ' '.join(demo_LBS)
        print 'wifi数量：', num
        print '日期时间: ', time
        print 'wifi数据：', wifi
        print 'LBS数据：', LBS
        result = ' '.join([self.sourceDate[0]+self.sourceDate[1]],
                          num, self.sourceDate[3], time, self.sourceDate[-1])
        content = {'WifiCmd': result}
        return self.get_callback(content)

    # 指令是0x69时的解析
    def processLBSCmd(self):
        # LBS所有数据
        LBS_DATA = self.sourceDate[4]
        LBS = {}

        # wifi数量
        num = self.sourceDate[2]
        # 日期时间
        time = LBS_DATA[0]
        # wifi数据
        if num != 00:
            demo_wifi = LBS_DATA[1:int(num)]
            wifi_worlds = {}
            for world in demo_wifi:
                list = []
                list2 = []
                i = 0
                while i < len(world):
                    list.append(world[i: i + 2])
                    i += 2
                print list
                for i in list:
                    i = '0x' + i
                    list2.append(i)
                wifi_world = ':'.join(list2)
                # 给wifi数据建立一个字典,value为信号强度
                wifi_worlds[wifi_world[:-5]] = [wifi_world[-4:]]
                # LBS数量
                LBS_num = LBS_DATA[int(num)+1]
                # MCCMNC
                MCCMNC = int(LBS_DATA[int(num)+2][:3], 16)
                # LBS数据
                for i in LBS_DATA[int(num)+3:-1]:
                    LBS[i] = [int(i[:4], 16), int(i[4:8], 16), int(i[8:10], 16)]
        else:
            wifi_worlds = None
            # LBS数量
            LBS_num = LBS_DATA[1]
            # MCCMNC
            MCCMNC = int(LBS_DATA[2][:3], 16)
            # LBS 数据
            for i in LBS_DATA[3: 3+int(LBS_num)]:
                LBS[i] = [int(i[:4], 16), int(i[4:8], 16), int(i[8:10], 16)]

        print 'wifi数量：', num
        print '日期时间：', time
        print 'WIFI数据：', wifi_worlds
        print 'LBS数量：', LBS_num
        print 'MCCMNC：', MCCMNC
        print 'LBS数据：', LBS
        content = content = {'wifi_num': num, 'time': time, 'wifi_world': wifi_worlds,
                             'LBS_num':LBS_num, 'MCCMNC': MCCMNC, 'LBS': LBS}
        return self.get_callback(content)







    def parserProcess(self):
        #判断数据的合法性
        if self.sourceDate[0]!=0x78 or self.sourceDate[1]!=0x78:
            return None
        else:
            self.len = self.sourceDate[2] #获取长度
            self.cmd = self.sourceDate[3]#获取指令号
            #根据指令号进行不同的协议处理
            if self.cmd==0x01:
                self.processLoginCmd()
            elif self.cmd==0x08:
                self.processHeartCmd()
            elif self.cmd==0x10:
                self.processGpsCmd()
            elif self.cmd==0x13:
                self.processStatusCmd()
            elif self.cmd==0x14:
                self.processSleepCmd()
            elif self.cmd==0x17:
                self.processWifiCmd()
            elif self.cmd==0x69:
                self.processLBSCmd()

    def get_callback(self, content):
        result = '%s, content: %s' % (self.sourceDate[4], content)
        print '---------------------------'
        print 'get_callback'
        print '回复的内容:', result
        print '---------------------------'
        return result


