# coding=utf-8
import requests, json, re, sqlite3, random, time
from requests.exceptions import HTTPError

s = requests.Session()
conn = sqlite3.connect('cyberleninka_test.db')
cursor = conn.cursor()

site_url = 'http://cyberleninka.ru/'

UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
           "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
           "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/55.0.2883.87 Chrome/55.0.2883.87 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0")

free_proxy_list = ["85.21.8.61:8080",
                   "81.9.30.22:8080",
                   "176.74.13.110:8080",
                   "79.104.25.218:8080",
                   "90.189.151.183:32601",
                   "145.255.6.171:31252",
                   "176.196.238.234:44648",
                   "94.180.249.187:38051",
                   "77.221.220.133:44331",
"176.196.89.216:37209",
"109.194.146.138:3128",
"194.67.37.90:3128",
"81.30.211.104:44861",
"89.109.14.179:32001",
"109.60.154.31:48134",
"95.181.45.234:55878"]

current_proxy_index = 0
#curr_proxy = free_proxy_list[current_proxy_index]

# Получим содержимое главной страницы
def get_page(url):

    try:
        start = time.time()

        ua = UAS[random.randrange(len(UAS))]

        headers = {'user-agent': ua}

        proxies = {
            "https": free_proxy_list[current_proxy_index],
        }
        #print('curr_proxy: %s' % free_proxy_list[current_proxy_index])
        response = s.get(site_url + url, headers=headers, proxies=proxies)

        end = time.time()
        func_sec = end - start
        if int(func_sec) > 10:
            remove_proxy()
            print('request get time sec: %d' % func_sec)
        #print('request get time sec: %d' % func_sec)

    except HTTPError as http_err:
        print('HTTP error occurred: %s' % http_err)  # Python 3.6
        return -1
    except Exception as err:
        print('Other error occurred: %s' %err)  # Python 3.6
        return -1
    else:
        return response.text

def close_conn():
    conn.commit()
    conn.close()

def make_commit():
    conn.commit()

#Получим ссылки из меню
def get_links_from_menu(page_html, menu_class):
    # Находим участок кода с категориями меню
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

    # Ищем все теги <li> ... </li>
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

# Получим ссылки на все статьи находящиеся на странице
def get_articles_links(article_page_html):

    #print('get_articles_links: %s\n' %first_page_url)
    #print('first_page_html: \n%s' %first_page_html)

    articles_links = get_links_from_menu(article_page_html, 'list')
    #for article_link in articles_links:
        #print('article_url: %s' % article_link)
        #parse_article(get_page(article_link))
    return articles_links

# Получим максимальное количество страниц для категории
def get_count_pages(category_page_html):

    pages_links = get_links_from_menu(category_page_html, 'paginator')

    if len(pages_links) > 0:
        last_page_url_split = re.split("/", pages_links[len(pages_links) - 1])
        count_pages = last_page_url_split[len(last_page_url_split) - 1]
        #print ('count_pages: %s' % count_pages)
        return int(count_pages)
    else:
        return 0

def get_article_authors(article_page_html):
    authors_list = []
    search_menu = re.search(r'<ul class="author-list">[\s\S]*?</ul>', article_page_html)
    if search_menu:
        #print('search_menu: %s' % search_menu.group(0))
        result_links = re.findall('<li[\s\S]*?>(.*?)<\/li>', search_menu.group(0))
        #print('author_links_count: %d' % len(result_links))
        for author_link in result_links:
            author_name = re.compile('<span[\s\S]*?>(.*?)<\/span>').search(author_link)
            if author_name:
                authors_list.append(author_name.group(1))

    return authors_list


def parse_article(article_page_html, article_page_url):

    article_parsed = {}

    # --> Article TITLE:
    title = re.compile('<i itemprop="headline">(.*?)<\/i>').search(article_page_html)
    if title:
        article_parsed['title'] = title.group(1)

        # --> Article URL:
        article_url = site_url + article_page_url
        article_parsed['url'] = article_url

        # --> Article AUTHORS NAMES:
        authors_list = get_article_authors(article_page_html)
        article_parsed['authors_list'] = authors_list
       #for author_name in authors_list:
            #print('author_name: %s' % author_name)

        # --> Article GOST LINK:
        gost_list = re.search('quotes: \{[\s\S]*?\}', article_page_html)
        gost_link = ''
        if gost_list:
            gost_list = gost_list.group(0)
            gost_link = re.split('",', re.split('gost_electronic: "', gost_list)[1])[0]
            gost_link = gost_link.replace('\\', '')
            gost_link = gost_link.replace(re.search('\([\s\S]*?:[\s\S]*?\)\.', gost_link).group(0), '')
        article_parsed['gost_link'] = gost_link
        #print('gost_link: %s' % gost_link)

        # --> Article JOURNAL:
        journal_name = 'none'
        journal_url = 'none'
        infoblock = re.search(r'<a href="/journal[\s\S]*?<\/a>', article_page_html)
        if infoblock:
            journal_name = re.compile('<a[\s\S]*?>(.*?)<\/a>').search(infoblock.group(0)).group(1)
            journal_url = re.compile('href="(.*?)"').search(infoblock.group(0)).group(1)
        article_parsed['journal_name'] = journal_name
        article_parsed['journal_url'] = journal_url
        #print('journal_url: %s' % journal_url)
        #print('journal_name: %s' % journal_name)

        # --> Article SCIENCE CAT:
        science_categories_map = {}
        science_cat_menu = re.search('<div class="half-right">[\s\S]*?</ul>', article_page_html)
        if science_cat_menu:
            science_cat_menu = science_cat_menu.group(0)
            #print('science_cat_menu %s' % science_cat_menu)
            science_cat_menu_li_list = re.findall(r'<li>[\s\S]*?<\/li>', science_cat_menu)
            for science_cat_li in science_cat_menu_li_list:
                science_cat_name = re.compile('<a[\s\S]*?>(.*?)<\/a>').search(science_cat_li).group(1)
                science_cat_url = re.compile('href="(.*?)"').search(science_cat_li).group(1)
                science_categories_map[science_cat_name] = science_cat_url
                #print('science_cat_li: %s' % science_cat_name)
                #print('science_cat_url: %s' % science_cat_url)
        article_parsed['science_categories_map'] = science_categories_map

        # --> Article TAGS:
        tags_names_list = []
        tags_block = re.search('<i itemprop="keywords">[\s\S]*?</i>', article_page_html)
        if tags_block:
            tags_block = tags_block.group(0)
            tags_block_spans = re.findall(r'<span[\s\S]*?>[\s\S]*?<\/span>', tags_block)
            for tag_span in tags_block_spans:
                tag_name = re.compile('<span[\s\S]*?>(.*?)<\/span>').search(tag_span).group(1)
                tags_names_list.append(tag_name)
                #print('tag_span: %s' % tag_name)
        article_parsed['tags_names_list'] = tags_names_list

        # --> Article UNIVERSITY:
        #<meta name="eprints.publisher"
        university_search = re.search('<meta name="eprints.publisher" [\s\S]*? \/>', article_page_html)
        university = ''
        if university_search:
            university_search = university_search.group(0)
            university = re.compile('content="(.*?)"').search(university_search).group(1)
            #print('university_search: %s\nuniversity: %s' % (university_search, university))
        article_parsed['university'] = university


        #print('article_title: %s' % title)
    else:
        print('error: title not found')

    return article_parsed



# ----------------========== DB SQLite Methods =========----------------------

def init_create_tables():
    cursor.execute("CREATE TABLE IF NOT EXISTS Journals (id  INTEGER NOT NULL, name integer(10), url integer(10) UNIQUE, PRIMARY KEY (id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Articles (id  INTEGER NOT NULL, title TEXT, url TEXT UNIQUE, gost_link TEXT, journal_id integer(10) NOT NULL, PRIMARY KEY (id), FOREIGN KEY(journal_id) REFERENCES Journals(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Universities (id  INTEGER NOT NULL, name TEXT UNIQUE, PRIMARY KEY (id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Authors (id  INTEGER NOT NULL, FIO TEXT, university_id integer(10), PRIMARY KEY (id), FOREIGN KEY(university_id) REFERENCES Universities(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Tags (id  INTEGER NOT NULL, name TEXT, science_cat_id INTEGER, PRIMARY KEY (id), FOREIGN KEY(science_cat_id) REFERENCES ScienceCategories(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS ScienceCategories (id  INTEGER NOT NULL, name TEXT, url TEXT, PRIMARY KEY (id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS ArticlesTags (id  INTEGER NOT NULL, tag_id integer(10) NOT NULL, article_id integer(10) NOT NULL, PRIMARY KEY (id), FOREIGN KEY(article_id) REFERENCES Articles(id), FOREIGN KEY(tag_id) REFERENCES Tags(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS ArticlesCategories (id  INTEGER NOT NULL, category_id integer(10) NOT NULL, article_id integer(10) NOT NULL, PRIMARY KEY (id), FOREIGN KEY(article_id) REFERENCES Articles(id), FOREIGN KEY(category_id) REFERENCES ScienceCategories(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS ArticlesAuthors (id  INTEGER NOT NULL, article_id integer(10) NOT NULL, author_id integer(10) NOT NULL, PRIMARY KEY (id), FOREIGN KEY(article_id) REFERENCES Articles(id), FOREIGN KEY(author_id) REFERENCES Authors(id))")

def check_tables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables_rows = cursor.fetchall()
    if len(tables_rows) == 0:
        print('No tables was created')

    for row in tables_rows:
        print('table created: %s' %row)

#check and insert Journal:
def insert_journal(journal_name, journal_url):
    cursor.execute("SELECT id FROM Journals WHERE name = ?", [journal_name])
    result = cursor.fetchall()
    journal_id = 0
    if len(result) > 0:
        journal_id = result[0][0]
    else:
        cursor.execute("INSERT INTO Journals(name, url) VALUES(?, ?)", [journal_name, journal_url])
        cursor.execute("SELECT id FROM Journals WHERE name = ?", [journal_name])
        journal_id = cursor.fetchall()[0][0]
    return journal_id

#check and insert Author:
def insert_author(author_FIO, university):

    cursor.execute("SELECT id FROM Universities WHERE name = ?", [university])
    result = cursor.fetchall()
    university_id = 0
    if len(result) > 0:
        university_id = result[0][0]
    else:
        cursor.execute("INSERT INTO Universities(name) VALUES(?)", [university])
        cursor.execute("SELECT id FROM Universities WHERE name = ?", [university])
        university_id = cursor.fetchall()[0][0]

    cursor.execute("SELECT id FROM Authors WHERE FIO = ? AND university_id = ?", [author_FIO, university_id])
    result = cursor.fetchall()
    author_id = 0
    if len(result) > 0:
        author_id = result[0][0]
    else:
        cursor.execute("INSERT INTO Authors(FIO, university_id) VALUES(?, ?)", [author_FIO, university_id])
        cursor.execute("SELECT id FROM Authors WHERE FIO = ? AND university_id = ?", [author_FIO, university_id])
        author_id = cursor.fetchall()[0][0]
    return author_id

#check and insert Category:
def insert_category(cat_name, cat_url):
    cursor.execute("SELECT id FROM ScienceCategories WHERE name = ?", [cat_name])
    result = cursor.fetchall()
    cat_id = 0
    if len(result) > 0:
        cat_id = result[0][0]
    else:
        cursor.execute("INSERT INTO ScienceCategories(name, url) VALUES(?, ?)", [cat_name, cat_url])
        cursor.execute("SELECT id FROM ScienceCategories WHERE url = ?", [cat_url])
        cat_id = cursor.fetchall()[0][0]
    return cat_id

#check and insert TAG:
def insert_tag(tag_name, category_id):
    cursor.execute("SELECT id FROM Tags WHERE name = ? AND science_cat_id = ?", [tag_name, category_id])
    result = cursor.fetchall()
    tag_id = 0
    if len(result) > 0:
        tag_id = result[0][0]
    else:
        cursor.execute("INSERT INTO Tags(name, science_cat_id) VALUES(?, ?)", [tag_name, category_id])
        cursor.execute("SELECT id FROM Tags WHERE name = ?", [tag_name])
        tag_id = cursor.fetchall()[0][0]
    return tag_id

# Check Insert Tables
def check_insert_tables():
    cursor.execute("SELECT * FROM Articles")
    article_result = cursor.fetchall()

    print('\n---------> Articles:\n')

    if len(article_result) == 0:
        print('Article was not inserted')
    else:
        for article_row in article_result:
            print('---------> article[%d]: %s"\n' % (article_row[0], article_row))

    print('\n-------> Journals:\n')
    cursor.execute("SELECT * FROM Journals")
    result = cursor.fetchall()
    for row in result:
        print(row)

    print('\n-------> Authors:\n')
    cursor.execute("SELECT * FROM Authors")
    result = cursor.fetchall()
    for row in result:
        print(row)

    print('\n-------> Categories:\n')
    cursor.execute("SELECT * FROM ScienceCategories")
    result = cursor.fetchall()
    for row in result:
        print(row)

    print('\n-------> Tags:\n')
    cursor.execute("SELECT * FROM Tags")
    result = cursor.fetchall()
    for row in result:
        print(row)

    print('\n-------> ArticlesTags:\n')
    cursor.execute("SELECT * FROM ArticlesTags")
    result = cursor.fetchall()
    for row in result:
        print(row)

    print('\n-------> ArticlesCategories:\n')
    cursor.execute("SELECT * FROM ArticlesCategories")
    result = cursor.fetchall()
    for row in result:
        print(row)

    print('\n-------> ArticlesAuthors:\n')
    cursor.execute("SELECT * FROM ArticlesAuthors")
    result = cursor.fetchall()
    for row in result:
        print(row)

def test_insert(parsed_article):
    title = 'Тестовый заголовок'
    url = 'http://askue-energy.ru'
    gost_link = 'Тестовая ссылка на ГОСТ // № 4. Тест тест http://askue-energy.ru'
    journal_id = 0
    cursor.execute("INSERT INTO Articles(title, url, gost_link, journal_id) VALUES(?, ?, ?, ?)", [title, url, parsed_article['gost_link'], journal_id])
    cursor.execute("SELECT * FROM Articles")
    result = cursor.fetchall()
    for row in result:
        print(row)

def select_article(article_title):

    cursor.execute("SELECT * FROM Articles WHERE title = ?", [article_title])

    article_result = cursor.fetchall()
    if article_result:
        return article_result[0]
    else:
        return ''

# --------------------------------------------------------------------------------------------------------------



#save Article data
def save_article(parsed_article):

    journal_id = insert_journal(parsed_article['journal_name'], parsed_article['journal_url'])

    #print('journal_id type: %s' % type(journal_id))

    #insert Article:
    cursor.execute("SELECT id FROM Articles WHERE url = ?", [parsed_article['url']])
    article_result = cursor.fetchall()
    if len(article_result) > 0:
        article_id = article_result[0][0]
    else:
        cursor.execute("INSERT INTO Articles(title, url, gost_link, journal_id) VALUES(?, ?, ?, ?)", [parsed_article['title'], parsed_article['url'], parsed_article['gost_link'], journal_id])
        cursor.execute("SELECT id FROM Articles WHERE url = ?", [parsed_article['url']])
        article_id = cursor.fetchall()[0][0]

    #insert Authors:
    authors_list = parsed_article['authors_list']
    for author_fio in authors_list:
        author_id = insert_author(author_fio, parsed_article['university'])
        cursor.execute("INSERT INTO ArticlesAuthors(article_id, author_id) VALUES(?, ?)", [article_id, author_id])

    #insert Categories:
    categories_map = parsed_article['science_categories_map']
    for cat_name, cat_url in categories_map.items():
        category_id = insert_category(cat_name, cat_url)
        cursor.execute("INSERT INTO ArticlesCategories(category_id, article_id) VALUES(?, ?)", [category_id, article_id])
        # insert Tags:
        tags_list = parsed_article['tags_names_list']
        for tag_name in tags_list:
            tag_id = insert_tag(tag_name, category_id)
            cursor.execute("INSERT INTO ArticlesTags(tag_id, article_id) VALUES(?, ?)", [tag_id, article_id])


#Change Proxy
def change_proxy():
    global current_proxy_index
    current_proxy_index += 1
    if current_proxy_index == len(free_proxy_list):
        current_proxy_index = 0
    #curr_proxy = free_proxy_list[current_proxy_index]
    print('change_proxy: %s | proxy_index: %d' % (free_proxy_list[current_proxy_index], current_proxy_index))

def remove_proxy():
    global current_proxy_index
    print('remove_proxy[%d]: %s' % (current_proxy_index, free_proxy_list[current_proxy_index]))
    free_proxy_list.remove(free_proxy_list[current_proxy_index])
    if current_proxy_index >= len(free_proxy_list):
        current_proxy_index = 0
    print('new proxy[%d]: %s' % (current_proxy_index, free_proxy_list[current_proxy_index]))
