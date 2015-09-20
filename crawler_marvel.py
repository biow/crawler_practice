#!/usr/bin/env python

import sys
import codecs
from bs4 import BeautifulSoup
import urllib2

# constant
PTT_URL = "https://www.ptt.cc"

# resolve the codecs
# ref: http://www.sixfeetup.com/blog/an-introduction-to-beautifulsoup
stream_writer = codecs.lookup('utf-8')[-1]
stdout = stream_writer(sys.stdout)


def check_date(compare_date, article_date, check_type):
    '''
    Check if the date of article is before/after the specific date.

    compare_date: the date used to be compared.
    article_date: date of the article.
    check_type: specify the kind of check. ("before", "after")
    '''
    compare_date_tmp = map(int, compare_date.split('/'))
    article_date_tmp = map(int, article_date.split('/'))

    if compare_date_tmp == article_date_tmp:
        return False
    elif compare_date_tmp > article_date_tmp:
        return True if check_type == "before" else False
    else:
        return True if check_type == "after" else False

def print_article_content(article_url):
    '''
    Print detail of the article.

    article_url: URL of the article.
    '''
    response = urllib2.urlopen(article_url)
    article_soup = BeautifulSoup(response, 'html.parser')

    article_div = article_soup.find(id="main-container")
    article_meta_value_span_list = article_div.findAll('span', class_='article-meta-value')
    article_push_list = article_div.findAll('div', class_='push')

    span_len = len(article_meta_value_span_list)
    article = {
        'author': article_meta_value_span_list[0].string if span_len > 0 else "",
        'title': article_meta_value_span_list[2].string if span_len > 2 else "",
        'date': article_meta_value_span_list[3].string if span_len > 3 else "",
        'content': article_div.strings,
        'pushes': [''.join(push.strings) for push in article_push_list],
    }

    #stdout.write(article['author'] + '\n')
    stdout.write(article['title'] + '\n')
    stdout.write(article['date'] + '\n')
    #stdout.write(list(article['content'])[span_len * 2 + 1] + '\n')
    #for push in article['pushes']:
    #    stdout.write(push)
    print

def get_articles_from_ptt(main_path, start_date, end_date):
    '''
    Get the articles from ptt between start_date and end_date.
    NOTE: the date is not including year, it can only get the articles of this year.

    main_path: the path of index page.
    start_date: the start date. (mm/dd)
    end_date: the end date. (mm/dd)
    '''
    response = urllib2.urlopen(PTT_URL + main_path)

    start_date_found = False
    while not start_date_found:
        article_list_soup = BeautifulSoup(response, 'html.parser')

        for article_item_div in article_list_soup.findAll('div', class_='r-ent'):
            # ignore the sticky articles
            if article_item_div.find_previous_sibling('div', class_='r-list-sep'):
                break

            # check the date
            article_date = article_item_div.find('div', class_='date').string.lstrip()
            if check_date(start_date, article_date, "before"):
                start_date_found = True
                continue
            if check_date(end_date, article_date, "after"):
                continue

            # print content of the article
            if article_item_div.a:
                article_url = PTT_URL + article_item_div.a['href']
            else:
                continue
            print_article_content(article_url)

        prev_path = article_list_soup.find('div', class_='btn-group pull-right').findAll('a', limit=2)[1]['href']
        response = urllib2.urlopen(PTT_URL + prev_path)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: %s <start_date> <end_date>" % (sys.argv[0])
        sys.exit()

    get_articles_from_ptt('/bbs/marvel/index.html', sys.argv[1], sys.argv[2])

