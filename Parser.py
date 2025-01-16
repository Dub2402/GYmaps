from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

from Writer import Writer

class Parser:
	def __init__(self) -> None:

		self.__browser = webdriver.Chrome()
		self.__browser.set_window_size(1920, 1080)
		self.__writer = Writer()
		self.Data = {
			"Имя": [],
			"Адрес": [],
			"Ссылка": []
		}

	def __ExecuteJavaScript(self, script: str) -> any:
		"""
		Выполняет JavaScript.
			script – исполняемый код.
		"""

		# Состояние: выполнен ли переход.
		IsSuccess = False
		# Результат выполнения.
		Result = None

		# Пока переход не выполнен.
		while not IsSuccess:

			try:
				# Обновление страницы.
				Result = self.__browser.execute_script(script)

			except: pass

			else: IsSuccess = True

		return Result

	def __Get(self, url: str):
		"""
		Обрабатывает переход браузера по URL.
			url – ссылка для перехода.
		"""

		# Состояние: выполнен ли переход.
		IsSuccess = False

		# Пока переход не выполнен.
		while not IsSuccess:

			try:
				# Переход по ссылке.
				self.__browser.get(url)
				# Остановка цикла.
				IsSuccess = True

			except Exception as ExceptionData: pass

	def __GetBody(self):
		html = self.__ExecuteJavaScript("return document.body.outerHTML;")
		soup = BeautifulSoup(html, "lxml")

		return soup

	def ParseYM(self, Url: str, button) -> None:
		self.__Get(Url)
		sleep(5)
		element = self.__browser.find_element(By.CLASS_NAME, "scroll__container")

		i = 0
		while True:
			self.__browser.execute_script("arguments[0].scroll(0, " + str(i * 300) + ");", element)
			Body = self.__GetBody()
			if Body.find("div", {"class": "add-business-view__link"}):
				self.__browser.execute_script("arguments[0].scroll(0, " + str((i * 300) + 7000) + ");", element)
				break
			i += 1
			sleep(0.1)

		blocktags = self.__GetBody().find_all("li",{ "class":"search-snippet-view"})

		for blocktag in blocktags:

			nametag = blocktag.find("div",{ "class":"search-business-snippet-view__title"})
			if nametag: name = nametag.get_text()
			url = ""

			urltag = blocktag.find("a",{ "class":"link-overlay"})
			if urltag: url = "https://yandex.ru" + urltag["href"]

			adresstag = blocktag.find("a",{ "search-business-snippet-view__address"})
			if adresstag: adress = adresstag.get_text()
			
			self.Data["Имя"].append(name)
			self.Data["Адрес"].append(adress)
			self.Data["Ссылка"].append(f"=HYPERLINK(\"{url}\", \"ссылка\")" if url else "")
			# self.Data["Ссылка"].append(f"{url}" if url else "")
			
			
		self.__writer.WriteExcel(self.Data, "YM")
		button.setText("Начать парсинг данных")
		button.setEnabled(True)

	def ParseGM(self, Url: str, button):
		self.__Get(Url)
		sleep(5)

		element = self.__browser.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')
		i = 0
		while True:
			self.__browser.execute_script("arguments[0].scroll(0, " + str(i * 300) + ");", element)
			Body = self.__GetBody()
			if "Больше результатов нет." in str(Body): break
			i += 1
			sleep(0.5)

		Feed = self.__GetBody().find("div", {"role": "feed"})
		blocktags = Feed.find_all("div", recursive = False)
		blocktags.pop(0)
		blocktags.pop(0)

		for blocktag in blocktags:
			
			nametag = blocktag.find("a")
			if nametag: 
				name = nametag["aria-label"]
				url = nametag["href"].split("?")[0]
				self.__Get(url)
				adresstag = self.__GetBody().find("button",{"data-item-id":"address"})
				if adresstag: adress = adresstag["aria-label"].replace("Адрес: ", "")
				sleep(5)
				self.Data["Имя"].append(name)
				self.Data["Адрес"].append(adress)
				self.Data["Ссылка"].append(f"=HYPERLINK(\"{url}\", \"ссылка\")")
				# self.Data["Ссылка"].append(f"{url}")

		self.__writer.WriteExcel(self.Data, "GM")
		button.setText("Начать парсинг данных")
		button.setEnabled(True)
