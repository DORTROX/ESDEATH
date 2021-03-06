import requests, wikipedia

TDMB = 'API KEY' #Get your own api key https://www.themoviedb.org/

def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def get_trending_movies():
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key=" + TDMB).json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]

def wikipediaa(query, sentencess):
    try:
        query = query.replace("wikipedia", "")
        results =  wikipedia.summary(query, sentences = sentencess)
        output = f"Wikipedia says, {results}"
        print(results)
        return output
    except wikipedia.exceptions.PageError as e:
        x = query.split(' wikipedia')
        print(f'No result found about {x}')