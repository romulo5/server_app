import pyexcel.ext.xls
import json

sheet = pyexcel.get_sheet(file_name="pyex/gnd.xls")
sheet.name_columns_by_row(0)
response=json.dumps(sheet.to_records())
