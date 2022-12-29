import xlrd
import xlwt
import pandas as pd

"""
pip3 install xlrd == 1.2.0
pip3 install xlwt == 0.7.5
"""

def contrast(processed_export_excel_file, all_number_file, same_name_file):
    """
    @param processed_export_excel_file: 导出名单处理后
    @param all_number_file: 总人数的名单
    @param same_name_file: 导出文件名
    """
    # 打开Excel文件
    # 打开处理后的导出名单
    data1 = xlrd.open_workbook(processed_export_excel_file)
    # 打开总人数的名单
    data2 = xlrd.open_workbook(all_number_file)
    #创建新excel
    new_excel = xlwt.Workbook()
    #创建新表
    new_sheet = new_excel.add_sheet('派蒙提取结果')
    # 打开
    data3=xlrd.open_workbook(same_name_file)

    # 读取原神语音的各个表
    df = pd.read_excel("/Users/jinyuxin/Desktop/虚拟偶像语音合成模型/原神语音.xlsx",sheet_name=None,header=None)
    l=0
    for sheet in df:
        print("sheet: "+ sheet)
        data3=xlrd.open_workbook(same_name_file)
        # 获取第一个sheet
        sheet1 = data1.sheet_by_index(0)
        #获取第2个表格第i个sheet
        sheet2 = data2.sheet_by_index(l)
        sheet3 = data3.sheet_by_index(0)
        #  获取三个Excel文件的行数和列数
        grows1 = sheet1.nrows
        grows2 = sheet2.nrows
        grows3 = sheet3.nrows
        # print("grows1:" + str(grows1))
        # print("grows2:" + str(grows2))
        # print("grows3:" + str(grows3))
        
        # 相同项 行
        same_content = []
        # 相同项 列
        same_column = []

        # sheet2中的所有人员
        excel_2_content = []
        for i in range(grows2):
            excel_2_content.append(sheet2.cell_value(i, 0))
        for i in range(grows1):
            for j in range(grows2):
                sheet1_value = sheet1.cell_value(i, 0)
                sheet2_value = sheet2.cell_value(j, 0)

                sheet2_column=sheet2.cell_value(j,1)

                # sheet1的字符串包含sheet2的字符串
                if str(sheet2_value) in str(sheet1_value):

                    same_content.append(sheet2_value)

                    same_column.append(sheet2_column)

        print("相同项：" + str(same_content) + " "+str(same_column))
        l=l+1

        # 将相同项写入新的Excel文件
        for i in range(len(same_content)) :
           if len(same_content)!=0:
                new_sheet.write(grows3+i, 0, same_content[i])
                new_sheet.write(grows3+i, 1, same_column[i])
                #print(grows3,i,same_content[i])
                new_excel.save(same_name_file)
        #print(grows3)


if __name__ == '__main__':
    file1 = r"/Users/jinyuxin/Desktop/虚拟偶像语音合成模型/提取派蒙文件名.xlsx"
    file2 = r"/Users/jinyuxin/Desktop/虚拟偶像语音合成模型/原神语音.xlsx"
    outfile = r"/Users/jinyuxin/Desktop/虚拟偶像语音合成模型/diff.xlsx"
    contrast(file1, file2, outfile)

