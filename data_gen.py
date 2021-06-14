from jazzify import ug
import joblib
import pandas as pd


def create_data(
    parallelism=8,
    chords_explore_page="https://www.ultimate-guitar.com/explore?genres[]=84&order=hitstotal_desc&type[]=Chords",
    pages=10,
    output_path="train.tsv",
):

    # crawl explore pages to get song urls

    song_urls = []
    with ug.UGSongUrlsExtractor() as ext:
        for page in range(1, pages + 1):
            url = f"{chords_explore_page}&page={page}"
            song_urls.extend(ext.extract_song_urls_from_url(url))
    print(f"{len(song_urls)} songs to extract")

    # batch the song urls by parallelizm

    url_batches = [[] for _ in range(parallelism)]
    for i, url in enumerate(song_urls):
        url_batches[i % parallelism].append(url)
    print(f"{len(url_batches)} batches prepared, max with {len(url_batches[0])} urls")

    # crawl songs in parallel

    def fn(url_batch):
        with ug.UGChordExtractor() as ext:
            chords = []
            for url in url_batch:
                try:
                    chords.append(ext.extract_chords_from_url(url))
                except:
                    print(f"failed {url}")
        return chords

    chord_batches = joblib.Parallel(n_jobs=parallelism)(
        joblib.delayed(fn)(url_batch) for url_batch in url_batches
    )
    chords = list(x for xs in chord_batches for x in xs)
    print(f"{len(chords)} songs extracted")

    # save data

    pd.DataFrame(chords).to_csv(output_path, index=False, sep="\t")


if __name__ == "__main__":
    create_data()
