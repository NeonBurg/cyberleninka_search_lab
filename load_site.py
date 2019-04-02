import requests, json, re, sqlite3
from requests.exceptions import HTTPError

s = requests.Session()
#conn = sqlite3.connect('cyberleninka_test.db')

site_url = 'https://cyberleninka.ru/'

# ������� ���������� ������� ��������
def get_page(url):

    response = s.get(site_url + url)

    # If the response was successful, no Exception will be raised
    if response:
        return response.text
    else:
        return -1

#������� ������ �� ����
def get_links_from_menu(page_html, menu_class):
    # ������� ������� ���� � ����������� ����
    search = re.split(r'<ul class="%s">' % menu_class, page_html)
    category_menu_content = ''
    url_list = []

    #print('get_links_from_menu: %s' % menu_class)
    #print('search_size = %d' %len(search))

    if len(search) > 1:
        search_menu = re.search('<li>[\s\S]*?<\/ul>', search[1])
        if(search_menu):
            category_menu_content += search_menu.group(0)
            #print('------- menu1:\n %s \n' % category_menu_content)

    if len(search) > 2:
        category_menu_content += search[2]
        #print('------- menu2:\n %s \n' % search[2])

    # ���� ��� ���� <li> ... </li>
    result_links = re.findall(r'<li>[\s\S]*?<\/li>', category_menu_content)

    for key in result_links:
        #link_a = re.search(r'<a\s[a-zA-Z0-9].[^<>]*>.[^<>]*</a>', key)
        link_a = re.search(r'<a[\s]+[^>]*?href[\s]?=[\s\"\']*(.*?)[\"\']*.*?>[\s\S]*?<\/a>', key)

        #print('key = %s' % key)
        if(link_a):
            #print('key = %s' % key)
            split_link = re.split('href="', link_a.group(0), maxsplit=2)
            url = re.split('"',split_link[1])[0]
            #print('url = %s' % url)
            url_list.append(url)

            #print('link_a = %s' % link_a)
            #print('-------------------------------------')

    return url_list

# ������� ������ �� ��� ������ ����������� �� ��������
def get_articles_links(first_page_html):

    #print('get_articles_links: %s\n' %first_page_url)
    #print('first_page_html: \n%s' %first_page_html)

    articles_links = get_links_from_menu(first_page_html, 'list')
    #for article_link in articles_links:
        #print('article_url: %s' % article_link)
        #parse_article(get_page(article_link))
    return articles_links

# ������� ������������ ���������� ������� ��� ���������
def get_count_pages(articles_page_html):

    pages_links = get_links_from_menu(first_page_html, 'paginator')

    if len(pages_links) > 0:
        last_page_url_split = re.split("/", pages_links[len(pages_links) - 1])
        count_pages = last_page_url_split[len(last_page_url_split) - 1]
        print ('count_pages: %s' % count_pages)
        return count_pages
    else:
        return 0

def get_article_authors(article_page_html):
    authors_list = []
    search_menu = re.search(r'<ul class="author-list">[\s\S]*?</ul>', article_page_html)
    if search_menu:
        #print('search_menu: %s' % search_menu.group(0))
        result_links = re.findall('<li[\s\S]*?>(.*?)<\/li>', search_menu.group(0))
        print('author_links_count: %d' % len(result_links))
        for author_link in result_links:
            author_name = re.compile('<span[\s\S]*?>(.*?)<\/span>').search(author_link)
            if author_name:
                authors_list.append(author_name.group(1))

    return authors_list


def parse_article(article_page_html, article_page_url):

    article_parsed = {}

    # --> Article URL:
    article_url = site_url + article_page_url

    # --> Article TITLE:
    title = re.compile('<i itemprop="headline">(.*?)<\/i>').search(article_page_html).group(1)

    # --> Article AUTHORS NAMES:
    authors_list = get_article_authors(article_page_html)
   #for author_name in authors_list:
        #print('author_name: %s' % author_name)

    # --> Article GOST LINK:
    gost_list = re.search('quotes: \{[\s\S]*?\}', article_page_html)
    gost_link = re.split('",', re.split('gost_electronic: "', gost_list.group(0))[1])[0]
    gost_link = gost_link.replace('\\', '')
    gost_link = gost_link.replace(re.search('\([\s\S]*?:[\s\S]*?\)\.', gost_link).group(0), '')
    #print('gost_link: %s' % gost_link)

    # --> Article JOURNAL:
    infoblock = re.search(r'<a href="/journal[\s\S]*?<\/a>', article_page_html)
    journal_name = re.compile('<a[\s\S]*?>(.*?)<\/a>').search(infoblock.group(0)).group(1)
    journal_url = re.compile('href="(.*?)"').search(infoblock.group(0)).group(1)
    #print('journal_url: %s' % journal_url)
    #print('journal_name: %s' % journal_name)

    # --> Article SCIENCE CAT:
    science_cat_menu = re.search('<div class="half-right">[\s\S]*?</ul>', article_page_html).group(0)
    #print('science_cat_menu %s' % science_cat_menu)
    science_cat_menu_li_list = re.findall(r'<li>[\s\S]*?<\/li>', science_cat_menu)
    for science_cat_li in science_cat_menu_li_list:
        science_cat_name = re.compile('<a[\s\S]*?>(.*?)<\/a>').search(science_cat_li).group(1)
        science_cat_url = re.compile('href="(.*?)"').search(infoblock.group(0)).group(1)
        #print('science_cat_li: %s' % science_cat_name)
        #print('science_cat_url: %s' % science_cat_url)

    # --> Article TAGS:
    tags_block = re.search('<i itemprop="keywords">[\s\S]*?</i>', article_page_html).group(0)
    tags_block_spans = re.findall(r'<span[\s\S]*?>[\s\S]*?<\/span>', tags_block)
    for tag_span in tags_block_spans:
        tag_name = re.compile('<span[\s\S]*?>(.*?)<\/span>').search(tag_span).group(1)
        #print('tag_span: %s' % tag_name)

    print('article_title: %s' % title)

    #print()


def save_article(article_page_html):

    print()