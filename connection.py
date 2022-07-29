import requests
import json
from datetime import date
from dateutil.relativedelta import relativedelta
import csv

# - https://developers.themoviedb.org/3/authentication/how-do-i-generate-a-session-id


class Moviedb:

    def __init__(self):

        self.vote_count_min = 50
        self.vote_average_min = 7
        self.my_genre = 53  # Thriller
        self.base_url = 'https://api.themoviedb.org/3/'
        self.api_key = 'your_api_key'

    def authentication(self):

        """ Connect to the moviedb api with the api key and get a request token """

        authentication_url = f'{self.base_url}/authentication/token/new?api_key={self.api_key}'
        response = requests.get(authentication_url)
        request_token = (response.json()['request_token'])
        return request_token

    def genres_search(self):

        """ Connects to the genres api and returns a list of genres with their ids """
        """ 53: Thriller 28: Action 35: Comedy, 80: Crime"""

        endpoint = 'genre/movie/list'
        try:
            r = requests.get(f'{self.base_url}{endpoint}?api_key={self.api_key}&language=en-US')
        except requests.exceptions.RequestException as err:
            raise err
        genres_dict = dict(r.json())
        return genres_dict

    def discover_movies(self):

        """ Get this year's movies of a certain genre, with a minimum vote count and vote average """
        """ Data is returned in a list, each movie in a dictionary inside the list """

        todays_date = date.today()
        current_year = todays_date.year
        my_movie_list = []
        endpoint = 'discover/movie'
        endpoint_params = f'primary_release_year={current_year}&with_genres={self.my_genre}&sort_by=vote_average.desc'
        connection_string = f'{self.base_url}{endpoint}?&api_key={self.api_key}&{endpoint_params}'

        try:
            r = requests.get(connection_string)
            r = dict(r.json())

        except requests.exceptions.RequestException as err:
            raise err

        for page in range(1, r['total_pages']-1):
            page_data = requests.get(f'{connection_string}&page={page}')

            for movie in page_data.json()['results']:
                if movie['vote_count'] > self.vote_count_min and movie['vote_average'] > self.vote_average_min:
                    my_movie_list.append({'Title': movie['original_title'], 'Vote Avg': movie['vote_average'], 'Vote Count': movie['vote_count']})
        print(f'This years best movies of type: {self.my_genre}, vote avg: {self.vote_average_min} and number of votes: {self.vote_count_min}')
        print(my_movie_list)

    def trending_movies(self):

        """ Get the daily or weekly trending movies."""
        """ Trending movies released in the last month. Sorted by rating descending. Printed as a list """

        todays_date = date.today()
        today_str = str(todays_date)
        last_month = todays_date - relativedelta(months=1)
        last_month = str(last_month)
        media_type = 'movie' # movie, tv or person
        timeframe = 'week' # day or week
        endpoint = f'trending/{media_type}/{timeframe}'
        connection_string = f'{self.base_url}{endpoint}?api_key={self.api_key}'
        trending_list = []

        try:
            movie_results = requests.get(connection_string)
            movie_results = dict(movie_results.json())

        except requests.exceptions.RequestException as err:
            raise err
        for page in range(1, movie_results['total_pages']):
            page_data = requests.get(f'{connection_string}&page={page}')

            for movie in page_data.json()['results']:
                if movie['release_date'] > last_month and movie['release_date'] < today_str and \
                        movie['vote_count'] > self.vote_count_min and movie['vote_average'] > self.vote_average_min:

                    trending_list.append({'title': movie['original_title'], 'vote_avg': movie['vote_average'],
                                          'vote_count': movie['vote_count']})
        print("Sorted trending list, highest ranking reviews first")
        print(sorted(trending_list, key=lambda i: i['vote_avg'], reverse=True))

    def search_movies(self):

        """ Search for movies that include a particular title and print the results to csv """

        movie_data = []
        title = 'Fast and Furious'
        endpoint = 'search/movie'
        endpoint_params = '&language=en-US&page=1&include_adult=false'
        connection_string = f'{self.base_url}{endpoint}?api_key={self.api_key}&{endpoint_params}&query={title}'

        try:
            movie_results = requests.get(connection_string)
        except requests.exceptions.RequestException as err:
            raise err

        header = ['Title', 'Vote Avg', 'Vote Count', 'Release Date']
        with open('movie_data.csv', 'w') as data_file:

            data_writer = csv.writer(data_file)
            data_writer.writerow(header)

            for movie in movie_results.json()['results']:
                movie_data.append({'title': movie['original_title'], 'vote_avg': movie['vote_average'],
                                  'vote_count': movie['vote_count'], 'release_date': movie['release_date']})
                row = (movie['original_title'], movie['vote_average'], movie['vote_count'], movie['release_date'] )
                data_writer.writerow(row)
            

if __name__ == '__main__':


    test = Moviedb()
    test.authentication()
#    test.configurations()
#    test.genres_search()
#    test.discover_movies()
    test.trending_movies()
#    test.search_movies()


