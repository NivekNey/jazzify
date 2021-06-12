from selenium import webdriver

EXECUTABLE_PATH = "C:/Users/me/Downloads/geckodriver-v0.29.1-win64/geckodriver.exe"


class Extractor:
    def __init__(self) -> None:
        self.driver = webdriver.Firefox(executable_path=EXECUTABLE_PATH)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.driver.close()
