import bs4
from . import extractor


class UGSongUrlsExtractor(extractor.Extractor):
    def extract_song_urls_from_url(self, url):

        self.driver.get(url)

        links = self.driver.find_elements_by_tag_name("a")

        urls = [
            link.get_attribute("href")
            for link in links
            if "/tab/" in link.get_attribute("href")
        ]

        return urls


class UGChordExtractor(extractor.Extractor):
    def extract_chords_from_url(self, url):

        self.driver.get(url)
        normal_chords = self.extract_chords_from_ug_page_source()
        self.click_simplify()
        simplified_chords = self.extract_chords_from_ug_page_source()

        return normal_chords, simplified_chords

    def extract_chords_from_ug_page_source(self):
        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
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
