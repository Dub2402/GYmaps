import pandas

from datetime import date


class Writer:

	def __init__(self) -> None:
		pass

	def WriteExcel(self, Data, site):
		today = date.today()
		today = today.strftime("%d.%m.%Y")
		
		df = pandas.DataFrame.from_dict(Data)
		if site =="YM":
			df.to_excel(f"Output/YM_{today}.xlsx", index= False)
		else:
			df.to_excel(f"Output/GM_{today}.xlsx", index= False)
