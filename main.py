
import json
import requests
import configparser


class INISettings:
	
    def __init__(self):
        self.limit = 0
        self.user = 0
        self.api_key = ""
        self.format = ""

    def config_parsing(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.limit = config['Default']['Limit']
        self.user = config['Default']['User']
        self.api_key = config['Default']['API_Key']
        self.format = config['Default']['Format']


def get_tracks(response_json):

    album_list = list()
    for track in response_json:
        # Ignore track without album name and ignore currently playing track
        if track['album']['#text'] != "" and "@attr" not in track.keys():

            album = str("{} - {}".format(track['artist']['#text'],
                                         track['album']['#text']))
            date = track['date']['#text']

            album_list = add_album(album, date, album_list)

    return album_list


def add_album(album, date, album_list):

    album_in_list = [item[0] for item in album_list]

    if album not in album_in_list:
        album_list.append([album, date])
        return album_list

    for n, i in enumerate(album_list):
        if i[0] == album:
            date = album_list[n][1]
            album_list[n] = [album, date]

    return album_list


def display_list(album_list):
    for item in album_list:
        print("{} - {} ".format(item[1], item[0]))


def main():

    config = INISettings()
    config.config_parsing()

    LASTFM_URL = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks"

	
    payload = {'limit': config.limit, "user": config.user,
               "api_key": config.api_key, "format": config.format}
    response = requests.get(LASTFM_URL, params=payload)
    response_json = json.loads(response.text)["recenttracks"]['track']
    album_list = get_tracks(response_json)
    display_list(album_list)


if __name__ == '__main__':
    main()
