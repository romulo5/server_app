import pyexcel as pe
import pyexcel.ext.xls # import it to handle xls file

sheet = pyexcel.get_sheet(file_name="gnd.xls", name_columns_by_row=0)
print(sheet.rows())
    #print("}")("%s: Autorizado: %d - Pago: %d" % (record['GND'], record['Autorizado'], record['Pago']))