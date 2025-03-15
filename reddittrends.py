import praw

def get_reddit_trends(subreddit="india"):
    try:
        # Set up Reddit API client
        reddit = praw.Reddit(
            client_id='ZrROPP178ePREDk5NTcEDA',
            client_secret='AyP2_67pn5AMmDk6ZzOZwA7DFQhUQA',
            user_agent='trending_app'
        )
        
        # Fetch hot posts
        hot_posts = reddit.subreddit(subreddit).hot(limit=10)
        trending_keywords = [post.title for post in hot_posts]
        return trending_keywords
    except Exception as e:
        print(f"Error fetching Reddit trends: {e}")
        print("Please ensure you have valid Reddit API credentials.")
        return []

# Get hot topics from the India subreddit
trending_keywords = get_reddit_trends()
if trending_keywords:
    print("Top Trending Topics in India:")
    for i, keyword in enumerate(trending_keywords, 1):
        print(f"{i}. {keyword}")
else:
    print("No trending topics found.")
