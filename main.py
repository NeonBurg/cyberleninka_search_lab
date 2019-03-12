import load_site

def run():
    try:
        main_page_html = load_site.get_page('')
        category_links = load_site.get_links_from_menu(main_page_html, 'grnti')

        articles_links = load_site.get_articles_links(load_site.get_page(category_links[0]))

        print('parse_article: %s' % articles_links[0])
        load_site.parse_article(load_site.get_page(articles_links[0]), articles_links[0])

        #for article_url in articles_links:
            #load_site.save_article(load_site.get_page(article_url))

        #for cat_link in category_links:
        #    load_site.get_page(cat_link)


        #print('response: %s' % response)

    except Exception as e:
        print('Error')
        raise e


run()