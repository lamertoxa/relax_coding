import logging
import psycopg2
from typing import List
from time import time, sleep
import requests

requests_per_minute = 100
links_per_page = 200


class DBfunction:
    def __init__(self, dbname='postgres', username='postgres', password='postgres', host='localhost', port='5432'):
        self.conn = psycopg2.connect(
            database=dbname, user=username, password=password, host=host, port=port)
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True
        self.check_links_table = (
            '''SELECT EXISTS (SELECT FROM pg_tables WHERE 
                                    schemaname = 'public' AND tablename  = 'links');''',
            '''CREATE TABLE LINKS(
                                    ID SERIAL PRIMARY KEY,
                                    START_TITLE TEXT NOT NULL,
                                    FINISH_TITLE TEXT NOT NULL,
                                    LINK TEXT NOT NULL);'''
        )

    def check_exist_table(self, table):
        self.cursor.execute(table[0])
        if self.cursor.fetchone()[0]:
            pass
        else:
            self.cursor.execute(table[1])

    def add_new_links(self, path):
        self.cursor.execute(f"INSERT INTO LINKS(START_TITLE,FINISH_TITLE,"
                            f"LINK) VALUES (%s, %s, %s);",
                            (path[0], path[-1], path))

    def search_exist_links(self, start, finish):
        self.cursor.execute(f"SELECT * FROM links WHERE START_TITLE = %s AND FINISH_TITLE = %s;",
                            (start, finish))
        try:
            query = self.cursor.fetchone()[-1].replace('{', '').replace('}', '').replace('\"', '').split(',')
            return query
        except TypeError:
            return None
    def save_to_db(self,titles):


    def close(self):
        self.conn.close()


class WikiRacer:
    WORDS_TO_AVOID = ['Вікіпедія:Стиль/Посилання', 'Обговорення:']

    def __init__(self):
        self.start_time = None
        self.in_queque = []
        self.current_viewing = []
        self.last_result = []
        self.checked_links = set()
        self.link_path = dict()
        self.last_request = time()
        self.count_request = 0
        self.db = DBfunction()
        self.stop_loop_bool = False

    def find_path(self, start: str, finish: str) -> List[str]:
        # implementation goes here
        self.start_time = time()

        def stop_loop(result=None,stored_path=None):
            if stored_path:
                self.last_result = stored_path
            elif result:
                self.last_result = [start] + self.link_path[result[0]] + [result[1]]
            else:
                self.last_result =[]
            self.stop_loop_bool = True
            if not self.db.search_exist_links(start, finish):
                self.db.add_new_links(self.last_result)


        def checked_links():
            for checked in self.current_viewing:
                self.checked_links.add(checked[1])
                self.link_path[checked[1]] = self.link_path.get(checked[1], []) + [checked[1]]

        def sleep_requests():
            if self.count_request >= requests_per_minute and int(time() - self.last_request) < 60:
                sleep(60 - int(time() - self.last_request))
                self.last_request = time()
                self.count_request = 0

        def check_time():
            if int(time() - self.start_time) >= 600:
                self.last_result = []
                clear_data()
                return True

        def clear_data():
            self.start_time = None
            self.in_queque = []
            self.current_viewing = []
            self.checked_links = set()
            self.link_path = dict()
            self.count_request = 0
            self.stop_loop_bool = True



        def redirect(title):
            url_wiki = f"http://uk.wikipedia.org/w/api.php?action=query&titles={title[1]}&prop=links&pllimit=" \
                       f"{links_per_page}&format=json"

            sleep_requests()

            response = requests.get(url_wiki)
            self.count_request += 1
            data = response.json()
            list_titles = [[title[1], i['title']] for i in data['query']
            ['pages'][list(data['query']['pages'].keys())[0]].get('links', "")
                          if i not in self.WORDS_TO_AVOID and not (i is None)]
            self.db.save_to_db(list_titles)
            self.in_queque.extend(list_titles)
            for guessed_title in list_titles:
                if check_time():
                    break
                if finish.lower() == guessed_title[1].lower():
                    checked_links()
                    stop_loop(guessed_title)
                    break

        self.db.check_exist_table(self.db.check_links_table)
        check_exist_link = self.db.search_exist_links(start, finish)

        if check_exist_link:
            stop_loop(stored_path=check_exist_link)

        while True:
            if self.in_queque:
                self.current_viewing, self.in_queque = self.in_queque[:], []
                for task in self.current_viewing:
                    if task[1] in self.checked_links:
                        continue
                    redirect(task)
                    if self.stop_loop_bool:
                        clear_data()
                        self.stop_loop_bool = False
                        return self.last_result
                checked_links()

            else:
                redirect([[], start])


def main():
    task = WikiRacer().find_path('Україна', 'НАТО')
    print(task)


if __name__ == "__main__":
    main()
