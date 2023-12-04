from googleapiclient.discovery import build

# Set your YouTube Data API key here
API_KEY = "AIzaSyCGhKJsoKDI9ekwprUy2JrWWX22744wbu8"

def search_videos(query):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Make API request to search for videos based on the user input
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id",
        maxResults=3
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]

    # Make API request to get video details (including view count)
    videos_response = youtube.videos().list(
        id=",".join(video_ids),
        part="snippet,statistics"
    ).execute()

    # Extract video details, including view count
    videos = videos_response.get("items", [])
    videos_info = [{"title": video["snippet"]["title"], "views": int(video["statistics"]["viewCount"]),
                    "url": f"https://www.youtube.com/watch?v={video['id']}"} for video in videos]

    # Sort videos based on views in descending order
    sorted_videos = sorted(videos_info, key=lambda x: x["views"], reverse=True)

    return sorted_videos[:3]

if __name__ == "__main__":
    # Get user input for the search query
    user_query = input("Enter your YouTube video search query: ")

    # Search for videos and get the top 3 based on views
    top_videos = search_videos(user_query)

    # Display the top videos
    print("\nTop 3 Videos:")
    for i, video in enumerate(top_videos, 1):
        print(f"{i}. Title: {video['title']}")
        print(f"   Views: {video['views']}")
        print(f"   URL: {video['url']}\n")
