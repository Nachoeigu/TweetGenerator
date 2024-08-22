from src.main import tweet_graph

url = "https://www.unicef.org/press-releases/acute-malnutrition-surges-government-yemen-controlled-areas-extremely-critical"
tweet_type = 'Thread'
output = tweet_graph.invoke({
    "url": url,
    "tweet_type":tweet_type
    })

for tweet in output['output']:
    print(tweet)
    print("\n")