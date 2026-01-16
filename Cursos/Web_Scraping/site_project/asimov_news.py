from site_scraper import Site
import os
from threading import Thread
import time
from datetime import datetime
import sys 
import pickle
import webbrowser
from math import ceil
from pytimedinput import timedInput

class AsimovNews:
    def __init__(self):
        self.dict_site = {}
        self.all_sites = ['globo','r7','band','uol']

        self.screen = 0
        self.kill = False
        self.page = 1

        self.news = self._read_file('news') if 'news' in os.listdir() else []
        self._update_file(self.news, 'news')
        self.sites = self._read_file('sites') if 'sites' in os.listdir() else []
        self._update_file(self.sites, 'sites')

        for site in self.all_sites:
            self.dict_site[site] = Site(site)

        self.news_thread = Thread(target=self.update_news)
        self.news_thread.daemon = True
        self.news_thread.start()

    def _update_file(self,lista, mode='news'):
         with open(mode, "wb") as fp:
            pickle.dump(lista, fp)
    
    def _read_file(self,mode='news'):
        with open(mode, "rb") as fp:
            n_list = pickle.load(fp)
            return n_list
        
    def _receive_command(self,valid_commands, timeout=30):
        command, timed = timedInput('>>', timeout=timeout)
        while command.lower() not in valid_commands and not timed:
            print(f'Invalid command. Type agains')
            command, timed = timedInput('>>', timeout=timeout)
        command = 0 if command == '' else command
        return command

    def main_loop(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            match self.screen:
                case 0:
                    print('WELCOME TO ASIMOV NEWS')
                    print('Please choose an item from menu:')
                    print('\n1. Last News\n2. Add Site\n3. Remove Site\n4. Close Program')

                    self.screen = int(self._receive_command(['1','2','3','4'],5))
                    print(self.screen,type(self.screen))
                case 1:
                    self.display_news()
                    command = str(self._receive_command(['n','p','o','m'],10)).lower()

                    match command:
                        case 'n':
                            if self.page < self.max_pages: self.page += 1
                        case 'p':
                            if self.page >1: self.page -= 1
                        case 'o':
                            link = int(input('Type the number of the article you want to open: '))
                            if link<1 or link > len(self.filtered_news):
                                print('Invalid article number.')
                            else:
                                webbrowser.open(self.filtered_news[link-1]['link'])
                        case 'm':
                            self.screen = 0
                
                case 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Type the number of the site you want to add in the list of active sites.\n Press 0 to return to main menu.\n')
                    print('\tACTIVE SITES =====================\n')
                    for i in self.sites:
                        print(f'\t{i}')
                    
                    print('\n\tINACTIVE SITES =====================')
                    offline_sites = [i for i in self.all_sites if i not in self.sites]
                    for i in range(len(offline_sites)):
                        print(f'\t{i+1}. {offline_sites[i]}')
                    site = int(self._receive_command([str(i) for i in range(len(offline_sites)+1)],50))

                    if site == 0:
                        self.screen = 0
                        continue
                    self.sites += [offline_sites[site-1]]
                    self._update_file(self.sites, 'sites')
                
                case 3:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Type the number of the site you want to remove from the list of active sites.\n Press 0 to return to main menu.\n')
                    print('\tACTIVE SITES =====================\n')

                    for i in range(len(self.sites)):
                        print(f'\t{i+1}. {self.sites[i]}')
                    site = int(self._receive_command([str(i) for i in range(len(self.sites)+1)],50))    
                    if site == 0:
                        self.screen = 0
                        continue
                    del self.sites[site-1]
                    self._update_file(self.sites, 'sites')
                
                case 4:
                    self.kill = True
                    sys.exit()
            
    def display_news(self):
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f'Last Updated : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')

                        self.filtered_news = [n for n in self.news if n['site'] in self.sites]
                        self.max_pages = ceil(len(self.filtered_news) / 20)

                        if self.page> self.max_pages: self.page = 1

                        constant = (self.page -1) * 10

                        for i,article in enumerate(self.filtered_news[constant:constant+10],start=1):
                            print(f"{constant+i}. {article['date'].strftime('%Y-%m-%d %H:%M:%S')} - {article['site'].upper()} - {article['subject']} ")
                        print(f'\nPage {self.page}/{self.max_pages}')
                        print('===================================================================================')
                        print('Command Options:')
                        print('N - Next Page | P - Previous Page | O - Open Article | M - Main Menu')

    def update_news(self):
        while not self.kill:
            for site in self.all_sites:
                self.dict_site[site].update_news()

                for key, value in self.dict_site[site].news.items():
                    dict_aux = {}
                    dict_aux['date'] = datetime.now()
                    dict_aux['site'] = site
                    dict_aux['subject'] = key
                    dict_aux['link'] = value

                    if len(self.news)==0 :
                        self.news.insert(0, dict_aux)
                        continue
                    add_news = True
                    for news in self.news:
                        if dict_aux['subject'] == news['subject'] and dict_aux['site'] == news['site']:
                            add_news = False
                            break
                    if add_news:
                        self.news.insert(0, dict_aux)
            self.news = sorted(self.news, key=lambda x: x['date'], reverse=True)
            self._update_file(self.news, 'news')
            time.sleep(10)  # Update every 10 seconds

self = AsimovNews()
self.main_loop()
