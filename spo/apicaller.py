from collections import OrderedDict
import spotipy

class APICaller:
    def search_and_get_uri(self, searched_keywords, search_type):
        search_data = spotipy.Spotify().search(' '.join(searched_keywords), limit=1, type=search_type[:-1])
        # get track URI of first result and play it with dbus
        if search_data[search_type]['items']:
            return search_data[search_type]['items'][0]['uri']
        else:
            return None

    def get_search_result_dict(self, searched_keywords, search_type, num_results=10):
        rtn_dict = OrderedDict()
        search_data = spotipy.Spotify().search(' '.join(searched_keywords), limit=num_results, type=search_type[:-1])
        if search_data[search_type]['items']:
            for item in search_data[search_type]['items']:
                if search_type == 'tracks':
                    rtn_dict[item['uri']] = [item['name'], item['artists'][0]['name'], item['album']['name']]
                elif search_type == 'artists':
                    rtn_dict[item['uri']] = [item['name']]
                elif search_type == 'albums':
                    rtn_dict[item['uri']] = [item['name'], item['artists'][0]['name']]
            return rtn_dict
        else:
            return None