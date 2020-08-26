import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import MainFunc
pd.set_option('mode.chained_assignment', None)

class CutUi(QWidget):
    def __init__(self,excel_path=None,csv_path=None):
        super(CutUi, self).__init__()
        self.excel_path=excel_path
        self.csv_path=csv_path

    def result(self):
        #result工作簿
        result_data=pd.read_excel(self.excel_path,sheet_name="Result",header=None)
        #修改列名
        result_data.columns=["NOTE","LGL_LSKU","LGL_NAME_LOCAL","LGL_RAW_ADDRESS"]
        return result_data

    def sub(self):
        #减少部分
        data=self.result()
        sub_data=data[data['NOTE'].isin(["减少"])]
        # sub_result.to_excel("not_match_result.xlsx",index=None)
        return sub_data

    def add(self):
        #新增部分
        data=self.result()
        new_data=data[data['NOTE'].isin(["新增"])]
        # new_result.to_excel("new_result.xlsx",index=None)
        return new_data

    def no_change(self):
        #无变化部分
        data=self.result()
        no_change_data=data[data['NOTE'].isin(["无变化"])]
        return no_change_data
    
    def update(self):
        #更新部分
        data=self.result()
        update_data=data[data['NOTE'].isin(["无变化"])]
        return update_data

    def old(self):
        #融合多个old csv文件数据
        if len(self.csv_path)>1:
            old_result=pd.concat([pd.read_csv(path) for path in self.csv_path],ignore_index=True)
        else:
            old_result=pd.read_csv(self.csv_path[0])
        #清洗多余数据
        old_result=old_result[old_result['LGL_LSKU'].notnull()]
        old_data=old_result[old_result['LGL_LSKU'].str.contains("-CHN-",na=False)]
        return old_data

    def sub_merge(self):
        sub_lsku=self.sub()['LGL_LSKU']
        result=pd.merge(sub_lsku,self.old(),how='left',on='LGL_LSKU')
        #减少部分需筛选出来的列
        col=['LGL_LSKU','FS_RECONCILE_RESULT','FS_DATA_SOURCES','FS_PRIMARY_DATA_SOURCE','LGL_NAME_LOCAL','LGL_RAW_ADDRESS','LGL_FLOOR','LGL_TELEPHONE','LGL_EPISODE','LGL_EPISODE_DATES','LGL_POI_NOTES','LGL_LSKU_HERIT','LGL_PRODUCT','LGL_FORMAT']
        merge_data=result[col]
        return merge_data

