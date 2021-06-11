from bs4 import BeautifulSoup
from selenium import webdriver

EXECUTABLE_PATH = "C:/Users/me/Downloads/geckodriver-v0.29.1-win64/geckodriver.exe"


class UGChordExtractor:
    def __init__(self) -> None:
        self.driver = webdriver.Firefox(executable_path=EXECUTABLE_PATH)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.driver.close()

    def extract_chords_from_url(self, url):

        self.driver.get(url)
        normal_chords = self.extract_chords_from_ug_page_source()
        self.click_simplify()
        simplified_chords = self.extract_chords_from_ug_page_source()

        return normal_chords, simplified_chords

    def extract_chords_from_ug_page_source(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        chord_spans = soup.find_all(attrs={"data-name": True})
        chords = [x.attrs["data-name"] for x in chord_spans]
        return chords

    def click_simplify(self):
        for b in self.driver.find_elements_by_tag_name("button"):
            try:
                if b.text == "SIMPLIFY":
                    b.click()
                    return
            except:
                continue
        raise Exception("Failed to find button to click")
