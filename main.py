import json
import os
import sys

import easygui
import urllib.request
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def fetch_tracks():
    window_title = "Bryen's Bandcamp Downloader"

    # Fetch album URL e.g: https://slikback.bandcamp.com/album/-
    url = easygui.enterbox("Enter the URL of the album you want to download.", window_title, "", True)
    if getattr(sys, 'frozen', False):
        # executed as a bundled exe, the driver is in the extracted folder
        chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    else:
        # executed as a simple script, the driver should be in `PATH`
        chromedriver_path = "chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    with Chrome(options=chrome_options, executable_path=chromedriver_path) as browser:
        browser.get(url)
        html = browser.page_source

    soup = BeautifulSoup(html, "html.parser")

    scripts = soup.find_all("script")

    for script in scripts:
        if script.has_attr("data-tralbum"):
            data = json.loads(script['data-tralbum'])
            artist_and_album_id = f"{data['artist']} - {data['id']}"
            output_filename = f"{artist_and_album_id}.txt"
            f = open(output_filename, "w")
            artist = data['artist']
            f.write(f"Artist: {artist}\n")
            f.write(f"Album ID: {data['url']}\n")
            f.write(f"Album ID: {data['id']}\n\n")
            for track in data["trackinfo"]:
                f.write(f"Track ID: {track['track_id']}\n")
                title = track['title']
                f.write(f"Track title: {title}\n")
                mp3_url = track['file']['mp3-128']
                f.write(f"Track download link (MP3 128kbps): {mp3_url}\n\n")
                urllib.request.urlretrieve(mp3_url, f"{title} - {artist}.mp3")
            f.close()
            should_restart = easygui.buttonbox(
                f"Successfully output to: {output_filename}.\n\nDo you wanna download some more shit?",
                window_title, ['Yeah m8', 'Nah m8'])
            if should_restart is 'Yeah m8':
                fetch_tracks()


fetch_tracks()
