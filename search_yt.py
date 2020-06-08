from youtube_search import YoutubeSearch

def search(search_query):
    results = YoutubeSearch(search_query, max_results=10).to_dict()
    top_result = results[0]
    return 'https://www.youtube.com' + top_result['link']

    
