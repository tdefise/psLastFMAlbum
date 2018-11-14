
import json
import requests
import configparser

LIMIT = 0
USER = 0
API_KEY = ""
FORMAT = ""


def config_parsing():
    global LIMIT, USER, API_KEY, FORMAT
    config = configparser.ConfigParser()
    config.read('config.ini')
    LIMIT = config['Default']['Limit']
    USER = config['Default']['User']
    API_KEY = config['Default']['API_Key']
    FORMAT = config['Default']['Format']


def get_track(response_json):

    album_list = list()

    for track in response_json:
        # Ignore track without album name and ignore currently playing track
        if (track['album']['#text'] != "" and \
                "@attr" not in track.keys()):

            album = str("{} - {}".format(track['artist']['#text'], track['album']['#text']))
            date = track['date']['#text']
            if album not in [item[0] for item in album_list]:
                album_list.append([album, 0, date])
            else:
                for n, i in enumerate(album_list):
                    if i[0] == album:
                        nbr_song_in_album = album_list[n][1] + 1
                        date_listened = album_list[n][2]
                        album_list[n] = [album, nbr_song_in_album, date_listened]
    return album_list


def main():


    config_parsing()

    payload = {'limit': LIMIT, "user": USER, "api_key": API_KEY, "format": FORMAT}
    response = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks', params=payload)
    response_json = json.loads(response.text)["recenttracks"]['track']

    album_list = get_track(response_json)

    print(*("{} - {} ".format(item[2], item[0]) for item in album_list), sep="\n")


if __name__ == '__main__':
    main()
