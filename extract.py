from twython import Twython, TwythonError
from pprint import pprint
import itertools
from os.path import join
import json
from datetime import datetime, timedelta

# Valor variável para cada dia de extração
days_ago = 1

# Função para a autenticação com a API
def authentification():
    my_file = open("keys.txt", "r") # Obtenção das chaves de acesso
    content = my_file.read() # leitura do arquivo de text com chaves de acesso
    API_KEY, API_SECRET_KEY = content.split("\n") # salvando chaves em variáveis
    my_file.close()

    twitter = Twython(API_KEY, API_SECRET_KEY) # Acesso ao Twitter por meio do Twython e chaves de acesso
    authentication_tokens = twitter.get_authentication_tokens() # Tokens para autenticação
    print(authentication_tokens['auth_url']) # Imprime na tela o site para autenticação do usuário
    VERIFIER = input('Enter verification code: ') # Salva o código imputado pelo usuário

    # Verificação do código imputado
    twitter = Twython(
        API_KEY, API_SECRET_KEY,
        authentication_tokens['oauth_token'],
        authentication_tokens['oauth_token_secret'])
    authorized_tokens = twitter.get_authorized_tokens(VERIFIER)
    
    # Instancia do Twython com acesso final
    twitter = Twython(
        API_KEY, API_SECRET_KEY,
        authorized_tokens['oauth_token'],
        authorized_tokens['oauth_token_secret']
    )

    return twitter

# Função para extrair tweets
def get_tweets(twitter):
    NUM_TWEETS_TO_FETCH = 1000 
    cursor = twitter.cursor(
        twitter.search, q='eleições 2022', 
        count=100, result_type='mixed', 
        until=(datetime.now() - timedelta(days = days_ago)).strftime("%Y-%m-%d")
        )
    search_tweets = list(itertools.islice(cursor, NUM_TWEETS_TO_FETCH))
    return search_tweets

# Filtrar Tweets para coletar somente os que são retweets
def filter_retweets(search_tweets):
    retweets = []
    for tweet in search_tweets:
        if 'retweeted_status' in tweet:
            retweets.append(tweet)
    return retweets

if __name__ == '__main__':
    twitter = authentification()
    search_tweets = get_tweets(twitter)
    retweets = filter_retweets(search_tweets)
    
    with open(join('datalake', f'extract_date={(datetime.now() - timedelta(days = days_ago)).strftime("%Y-%m-%d")}.json'), 'w') as outfile:
        json.dump(retweets, outfile)
    
    print('Tweets sobre "Eleições 2022" extraidos e salvo com sucesso!')