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

	def ParseYM(self) -> None:
		self.__Get("https://yandex.by/maps/?display-text=%D0%A1%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%BD%D1%8B%D0%B9%20%D1%86%D0%B5%D0%BD%D1%82%D1%80%20%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D0%BC%D0%B0%D1%81%D1%82%D0%B5%D1%80&ll=82.680472%2C50.383318&mode=search&sctx=ZAAAAAgBEAAaKAoSCZNTO8PUcENAES2VtyOcnkdAEhIJpaFGIcmsxj8RjUY%2Br3jquT8iBgABAgMEBSgAOABAkE5IAWoCdWGdAc3MTD2gAQCoAQC9ASYylhfCAZQBrNuJw6oF8ZrQ6OwD99ertMsC0bib0dQDt7bC1ULFtOSenwWvmJ6WxAKwiciNxAKemJKevwXwoZ%2FN5QXbqrz7kATP1qjftwOgrNWjqgbNoIv3zgP9%2B9XkrwbVxqTEbd204ITpBe6dm6bbAq%2Fj1pDYAuiEr5qdAurVg5amBOTwofqOA%2B%2FJ7am0BtC8kaGoAei7753KA4ICF2NoYWluX2lkOigxNDU5Mzg0NjQ2NjYpigIAkgIAmgIMZGVza3RvcC1tYXBzqgIMMTQ1OTM4NDY0NjY2sAIB&sll=82.680472%2C50.383318&sspn=197.606685%2C73.651864&text=chain_id%3A%28145938464666%29&z=2.65")
		sleep(5)
		element = self.__browser.find_element(By.CLASS_NAME, "scroll__container")
		
		for i in range(1000):
			self.__browser.execute_script("arguments[0].scroll(0, " + str(i * 50) + ");", element)
			sleep(0.05)

		blocktags = self.__GetBody().find_all("li",{ "class":"search-snippet-view"})

		for blocktag in blocktags:

			nametag = blocktag.find("div",{ "class":"search-business-snippet-view__title"})
			if nametag: name = nametag.get_text()


			urltag = blocktag.find("a",{ "class":"search-snippet-view__link-overlay _focusable"})
			if urltag: url = "https://yandex.ru" + urltag["href"]

			adresstag = blocktag.find("a",{ "search-business-snippet-view__address"})
			if adresstag: adress = adresstag.get_text()
			
			self.Data["Имя"].append(name)
			self.Data["Адрес"].append(adress)
			self.Data["Ссылка"].append(f"=HYPERLINK(\"{url}\", \"ссылка\")")

		self.__writer.WriteExcel(self.Data, "YM")

	def ParseGM(self) -> None:
		self.__Get("https://www.google.ru/maps/search/%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D0%BC%D0%B0%D1%81%D1%82%D0%B5%D1%80/@62.6992759,52.9857826,3z?entry=ttu")
		sleep(15)

		element = self.__browser.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')
		
		for i in range(300):
			self.__browser.execute_script("arguments[0].scroll(0, " + str(i * 100) + ");", element)
			sleep(0.65)

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
				sleep(0.5)
				self.Data["Имя"].append(name)
				self.Data["Адрес"].append(adress)
				self.Data["Ссылка"].append(f"=HYPERLINK(\"{url}\", \"ссылка\")")

		self.__writer.WriteExcel(self.Data, "GM")
		