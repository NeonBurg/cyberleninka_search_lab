import load_site

def run():
    #try:
        main_page_html = load_site.get_page('')
        category_links = load_site.get_links_from_menu(main_page_html, 'grnti')
        #category_links = []

        #articles_links = load_site.get_articles_links(load_site.get_page(category_links[0]))
        #print('parse_article: %s' % articles_links[0])
        #parsed_article = load_site.parse_article(load_site.get_page(articles_links[0]), articles_links[0])
        #load_site.save_article(parsed_article)
        #load_site.check_insert_tables(parsed_article)

        #load_site.check_insert_tables()

        #load_site.init_create_tables()
        #load_site.check_tables()

        # cat_link = category_links[0]

        #for cat_link in category_links:
        cat_link = category_links[0]

        articles_first_page_html = load_site.get_page(cat_link)
        count_max_page = load_site.get_count_pages(articles_first_page_html)
        # print('cat_link: %s | max_page: %d' % (cat_link, count_max_page))
        print('---- Parsing: "%s" ...' % cat_link)
        i = 966
        while i <= count_max_page:
            print(' ------ page: %d' % i)
            articles_links = load_site.get_articles_links(load_site.get_page(cat_link + '/' + str(i)))
            for article_link in articles_links:
                article_page_html = load_site.get_page(article_link)
                parsed_article = {}
                if article_page_html != -1:
                    parsed_article = load_site.parse_article(article_page_html, article_link)

                if len(parsed_article) > 0:
                    load_site.save_article(parsed_article)
                else:
                    while len(parsed_article) == 0:
                        load_site.change_proxy()
                        article_page_html = load_site.get_page(article_link)
                        parsed_article = {}
                        if article_page_html != -1:
                            parsed_article = load_site.parse_article(article_page_html, article_link)
            load_site.make_commit()
            i += 1




        load_site.close_conn()

    #except Exception as e:
        #print('Error')
        #raise e


run()