

import pandas as pd
import requests
import json


## import api key
df_key = pd.read_csv('api_key.csv')
api_key = df_key['key'][0]


## define query params
begin_date = '20200101'
end_date = '20220601'
query_term = 'Amazon'
filter_query = 'news_desk:("Business", "Technology", "U.S.", "Working", "Workplace")'
paginations = range(10)
sort_order = 'relevance'


## loop through 10 pages to get 1000 articles
for page_idx in paginations:
    try:
        url = (
            f'https://api.nytimes.com/svc/search/v2/articlesearch.json? \
                begin_date={begin_date}&end_date={end_date}\
                &q={query_term}&fq={filter_query}\
                &page={page_idx}&sort={sort_order}&api-key={api_key}'
        )
        
        response = requests.get(url)
        response_status = response.status_code

        ## check status code first, otherwise articles cannot be extracted
        if response_status == 200:
            response_json = response.json()

        ## extract articles
        articles = response_json['response']['docs']

        ## save articles to json
        if len(articles) == 10:
            for art_idx, article in enumerate(articles):
                art_filename = f'./project_articles/article_{page_idx * 10 + art_idx}.json'
                with open(art_filename, 'w') as f:
                    json.dump(article, f)
            print('Articles on page {page_idx} fetched successfully')
        else:
            print('No articles found on page {page_idx}')

    except Exception as e:
        print('Fetching error on page {page_idx}: {e}')

print('Extraction completed')
