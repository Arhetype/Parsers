import csv
from googleapiclient.discovery import build
# Замените 'your-api-key' на свой API-ключ YouTube Data API
YOUTUBE_API_KEY = ''

# URL видео на YouTube
video_url = "https://www.youtube.com/watch?v=56BuUtz8e4k"


def get_youtube_service(api_key):
    return build('youtube', 'v3', developerKey=api_key)


def extract_video_id(url):
    video_id = url.split('v=')[-1]
    return video_id.split('&')[0] if '&' in video_id else video_id


def get_top_10_comments(youtube, video_id):
    try:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=10
        ).execute()

        comments = [{'comment': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                     'likes': item['snippet']['topLevelComment']['snippet']['likeCount']}
                    for item in response.get('items', [])]

        return comments
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"


def save_comments_to_csv(comments):
    with open('comments.csv', 'w', newline='', encoding='utf-16') as csv_file:
        fieldnames = ['Comment', 'Likes']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([{'Comment': comment['comment'], 'Likes': comment['likes']} for comment in comments])


def main():
    youtube = get_youtube_service(YOUTUBE_API_KEY)
    video_id = extract_video_id(video_url)
    top_comments = get_top_10_comments(youtube, video_id)

    if isinstance(top_comments, list):
        save_comments_to_csv(top_comments)
        print("Топ-10 комментариев по лайкам сохранены в файле comments.csv")
    else:
        print(top_comments)


if __name__ == "__main__":
    main()