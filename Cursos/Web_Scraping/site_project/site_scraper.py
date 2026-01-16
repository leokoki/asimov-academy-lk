import requests

from bs4 import BeautifulSoup

dict_site = {}
dict_site['globo'] = dict(
    url="https://www.globo.com/",
    tg_class=["post__title", "post-multicontent__link--title__text"],
    tag_link_and_tittle="h2",
    link_attr="href", 
    find_post_block="a"
)
dict_site['r7'] = dict(
    url="https://www.r7.com/",
    tg_class=["title"],
    tag_link_and_tittle="a",
    link_attr="href",
    find_post_block='h3'
)
dict_site['band'] = dict(
    url="https://www.band.com.br/",
    tg_class=["title"],
    tag_link_and_tittle=["h2", "h3"],
    link_attr="href",
    find_post_block='a'
)
dict_site['uol'] = dict(
    url="https://www.uol.com.br/",
    tg_class=['headlineHorizontalAvatar__content__title','headlineStandard__container__title title__element','title__element headlineHorizontal__content__title','title__element headlineMain__title','title__element headlineSub__content__title'],
    tag_link_and_tittle="h3",
    link_attr="href",
    find_post_block='a'
)


class Site:
    def __init__(self, site):
        self.site = site
        self.news = []

    def update_news(self):
        # Fetch site configuration
        url = dict_site[self.site.lower()]['url']
        tg_class = dict_site[self.site.lower()]['tg_class']  
        tag_link_and_tittle = dict_site[self.site.lower()]['tag_link_and_tittle']
        link_attr = dict_site[self.site.lower()]['link_attr']
        find_post_block = dict_site[self.site.lower()]['find_post_block']
        # Make request to the site
        browsers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        page = requests.get(url, headers=browsers)

        resposta = page.text
        soup = BeautifulSoup(resposta, "html.parser")

        noticias = soup.find_all(find_post_block)

        news_dict_title_link = {}
        for noticia in noticias:
            if type(tag_link_and_tittle)==list: # Some sites use different tags for titles in the same page
                for tg in tag_link_and_tittle:
                    if getattr(noticia, tg) != None:
                        tag_element = getattr(noticia, tg)
                        break
                    else:
                        tag_element = None
            else:
                tag_element = getattr(noticia, tag_link_and_tittle)
            if tag_element != None: # Verify if tag_link_and_tittle exists (some sites use <a> others <h2>, etc)
                if tag_element.get('class') != None: # Verify if tag has class attribute
                    for tg in tg_class:
                        # Some sites use space between the name of the classes
                        class_joined = ' '.join(tag_element.get('class'))  if len(tag_element.get('class')) > 1 else tag_element.get('class')                      
                        if tg == class_joined:
                            news_dict_title_link[tag_element.text.replace('\n', '').strip()] = noticia.get(link_attr)
                else:
                    for tg in tg_class:
                        if tag_element.get(tg) != None: # Some sites use custom attributes instead of class
                            news_dict_title_link[tag_element.text.replace('\n', '').strip()] = tag_element[link_attr]
        
        self.news = news_dict_title_link


