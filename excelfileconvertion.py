import pandas

def ConvertExcel(data_to_convert_excel,xlsx_filename):
    try:
        df=pandas.DataFrame(data_to_convert_excel)
        df.to_excel(xlsx_filename)
        return True
    except Exception as e:
        print(e)
        return False
