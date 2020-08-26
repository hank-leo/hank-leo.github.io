import xlwings as xw
import pandas as pd
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import MainFunc
import CutPart
import random
import time
import traceback

class SubUi(QWidget):
    def __init__(self,excel_path=None,csv_path=None):
        super(SubUi, self).__init__()
        self.init_ui()
        self.excel_path=excel_path
        self.csv_path=csv_path

    def init_ui(self):
        self.resize(400, 350)
        self.move(900,300)
        self.setWindowTitle('减少部分')

        #查看原数据
        self.search = QPushButton('查看原数据')
        self.search.clicked.connect(self.searchClick)

        #查看关店数据
        self.close = QPushButton('查看关店数据')
        self.close.clicked.connect(self.colseClick)

        #查看关店数据
        self.remodeling = QPushButton('查看装修数据')
        self.remodeling.clicked.connect(self.remodellingCloseClick)

        #查看关店数据
        self.oth = QPushButton('查看没操作过的数据')
        self.oth.clicked.connect(self.other)

        #找出result列数据
        self.save = QPushButton('一键导出结果并保存')
        self.save.clicked.connect(self.saveClick)

        #布局
        gridLayout = QGridLayout()
        gridLayout.addWidget(self.search)
        gridLayout.addWidget(self.close)
        gridLayout.addWidget(self.remodeling)
        gridLayout.addWidget(self.oth)
        gridLayout.addWidget(self.save)
        self.setLayout(gridLayout)

    def searchClick(self):
        result=CutPart.CutUi(self.excel_path,self.csv_path).sub_merge()
        # print(result)
        return result

    def colseClick(self):
        result=self.searchClick()
        time.sleep(random.random()+1)
        #找出已关店数据
        closed_result1=result[result['LGL_EPISODE'].isin(["CLOSED"])]
        closed_result1['NOTE']="已关闭"
        closed_result2=result[result['LGL_EPISODE'].str.endswith("|CLOSED")]
        closed_result2['NOTE']="已关闭"
        #合并上面拆分的表
        colsed_data=pd.concat([closed_result1,closed_result2])
        # print(colsed_data)
        return colsed_data

    def remodellingCloseClick(self):
        result=self.searchClick()
        #找出正在装修的数据
        remodelling_closed_result=result[result['LGL_EPISODE'].str.endswith("|REMODELLING_CLOSED")]
        remodelling_closed_result['NOTE']="正在装修,需确认最新状态"
        #找出尚未开业的数据
        planned_result=result[result['LGL_EPISODE'].str.endswith("PLANNED")]
        planned_result['NOTE']="尚未开业,需确认最新状态"
        #合并上面拆分的表
        remodelling_close_data=pd.concat([remodelling_closed_result,planned_result])
        # print(remodelling_close_data)
        return remodelling_close_data

    def merge_close(self):
        result=pd.concat([self.colseClick(),self.remodellingCloseClick()])
        return result

    def other(self):
        result=self.searchClick()
        mergeClose_data=self.merge_close()
        #合并数据
        result=pd.merge(result,mergeClose_data,how='left',on='LGL_LSKU')
        #找出未操作过的数据
        result=result[result['NOTE'].notnull()==False]
        #修改列名
        result=result[['LGL_LSKU','FS_RECONCILE_RESULT_x','FS_DATA_SOURCES_x','FS_PRIMARY_DATA_SOURCE_x','LGL_NAME_LOCAL_x','LGL_RAW_ADDRESS_x','LGL_FLOOR_x','LGL_TELEPHONE_x','LGL_EPISODE_x','LGL_EPISODE_DATES_x','LGL_POI_NOTES_x','LGL_LSKU_HERIT_x','LGL_PRODUCT_x','LGL_FORMAT_x','NOTE']]
        col=['LGL_LSKU','FS_RECONCILE_RESULT','FS_DATA_SOURCES','FS_PRIMARY_DATA_SOURCE','LGL_NAME_LOCAL','LGL_RAW_ADDRESS','LGL_FLOOR','LGL_TELEPHONE','LGL_EPISODE','LGL_EPISODE_DATES','LGL_POI_NOTES','LGL_LSKU_HERIT','LGL_PRODUCT','LGL_FORMAT','NOTE']
        result.columns=col
        return result

    def matched(self):
        try:
            result=self.other()
            #做过reconcile的部分,保留
            match_result=result[result['FS_RECONCILE_RESULT'].notnull()]
            match_result=match_result[match_result['FS_RECONCILE_RESULT'].str.contains("Match")]
            match_result['NOTE']="做过reconcile,保留"
            return match_result
        except Exception:
            traceback.print_exc()
            pass

    def exce1(self):
        try:
            result=self.other()
            #找出result为exc1的部分
            exce1_result=result[result['FS_RECONCILE_RESULT'].notnull()]
            exce1_result=exce1_result[exce1_result['FS_RECONCILE_RESULT'].str.contains("Exception 1")]
            exce1_result['NOTE']="exc1需确认最新状态"
            return exce1_result
        except Exception:
            traceback.print_exc()
            pass
    
    def exce2(self):
        try:
            result=self.other()
            #找出result为exc2的部分
            exce2_result=result[result['FS_RECONCILE_RESULT'].notnull()]
            exce2_result=exce2_result[exce2_result['FS_RECONCILE_RESULT'].str.contains("Exception 2|Addition")]
            exce2_result['NOTE']="reconcile新增,保留"
            return exce2_result
        except Exception:
            traceback.print_exc()
            pass

    def vdr(self):
        try:
            result=self.other()
            #VDR新增数据
            vdr_result=result[result['FS_RECONCILE_RESULT'].isnull()]
            vdr_result=vdr_result[vdr_result['FS_PRIMARY_DATA_SOURCE'].notnull()]
            vdr_result=vdr_result[vdr_result['FS_PRIMARY_DATA_SOURCE'].str.contains("VDR")]
            vdr_result['NOTE']="VDR新增,保留"
            return vdr_result
        except Exception:
            traceback.print_exc()
            pass

    def harv(self):
        try:
            result=self.other()
            #来源harv，对比最新官网数据,无此店
            harv_result=result[result['FS_RECONCILE_RESULT'].isnull()]
            harv_result=harv_result[harv_result['FS_PRIMARY_DATA_SOURCE'].notnull()]
            harv_result=harv_result[harv_result['FS_PRIMARY_DATA_SOURCE'].str.contains("HARV")]
            harv_result['NOTE']="来源harv，对比最新官网数据,无此店,需确认状态"
            return harv_result
        except Exception:
            traceback.print_exc()
            pass

    def no_result(self):
        try:
            result=self.other()
            #来源harv，对比最新官网数据,无此店
            no_result=result[result['FS_RECONCILE_RESULT'].isnull()]
            no_result=no_result[no_result['FS_PRIMARY_DATA_SOURCE'].isnull()]
            no_result['NOTE']="来源harv，对比最新官网数据,无此店,需确认状态"
            return no_result
        except Exception:
            traceback.print_exc()
            pass
    
    def cust(self):
        try:
            result=self.other()
            #无result,来源cust
            cust_result=result[result['FS_RECONCILE_RESULT'].isnull()]
            cust_result=cust_result[cust_result['FS_PRIMARY_DATA_SOURCE'].notnull()]
            cust_result=cust_result[cust_result['FS_PRIMARY_DATA_SOURCE'].str.contains("CUST")]
            cust_result['NOTE']="客户数据,保留"
            return cust_result
        except Exception:
            traceback.print_exc()
            pass

    def saveClick(self):
        try:
            #合并上面拆分的表
            result=pd.concat([self.merge_close(),self.matched(),self.exce1(),self.exce2(),self.vdr(),self.harv(),self.no_result(),self.cust()])
            #合并数据
            result=pd.merge(self.searchClick(),result,how='left',on='LGL_LSKU')
            result=result[['LGL_LSKU','FS_RECONCILE_RESULT_x','FS_DATA_SOURCES_x','FS_PRIMARY_DATA_SOURCE_x','LGL_NAME_LOCAL_x','LGL_RAW_ADDRESS_x','LGL_FLOOR_x','LGL_TELEPHONE_x','LGL_EPISODE_x','LGL_EPISODE_DATES_x','LGL_POI_NOTES_x','LGL_LSKU_HERIT_x','LGL_PRODUCT_x','LGL_FORMAT_x','NOTE']]
            #修改列名
            col=['LGL_LSKU','FS_RECONCILE_RESULT','FS_DATA_SOURCES','FS_PRIMARY_DATA_SOURCE','LGL_NAME_LOCAL','LGL_RAW_ADDRESS','LGL_FLOOR','LGL_TELEPHONE','LGL_EPISODE','LGL_EPISODE_DATES','LGL_POI_NOTES','LGL_LSKU_HERIT','LGL_PRODUCT','LGL_FORMAT','NOTE']
            result.columns=col
            #根据NOTE列排序
            result= result.sort_values(by=['NOTE'],na_position='first')
            #使用xlwings保存到excel表
            app=xw.App(visible=False,add_book=False)
            app.display_alerts=False
            load_wb=app.books.open(self.excel_path)
            num =len(load_wb.sheets)
            try:
                load_ws=load_wb.sheets['减少']
                load_ws.clear()
            except:
                load_ws=load_wb.sheets.add(name="减少",after=num)
            load_ws.range('A1').value = col
            load_ws.range("A2").expand("table").value=result.values.tolist()
            load_wb.save()
            load_wb.close()
            app.quit()
            QMessageBox.information(self,"结果","导出减少部分成功!")
        except Exception:
            traceback.print_exc()