from flask import Flask, jsonify
from flask_caching import Cache
from youtube_dl import YoutubeDL

app = Flask(__name__)

yt = YoutubeDL({'simulate': True})
cache_config = {
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": "videos_cache",
    "CACHE_DEFAULT_TIMEOUT": 3000

}

app.config.from_mapping(cache_config)
cache = Cache(app)

@app.route('/playlist/<playlist>', methods=['GET'])
@cache.memoize(timeout=60*60*3)
def get_playlist(playlist):
    playlist_metdata = ['id', 'title', 'uploader', 'uploader_id', 'uploader_url', 'webpage_url']
    video_metadata = ['id', 'title',  'description', 'upload_date', 'uploader', 'uploader_id', 'uploader_url', 'channel_id', 'channel_url', 'duration', 'view_count', 'average_rating', 'age_limit',
     'webpage_url', 'categories', 'tags', 'is_live', 'like_count', 'dislike_count', 'channel', 'n_entries', 'playlist', 'playlist_id', 'playlist_title', 'playlist_uploader', 'playlist_uploader_id', 'playlist_index', 'thumbnail',
     'display_id']
    print(f"https://www.youtube.com/playlist?list={playlist}")
    data = yt.extract_info(f"https://www.youtube.com/playlist?list={playlist}")
    result = {k:v for k,v in data.items() if k in playlist_metdata}
    result['videos'] = [{k:v for k,v in e.items() if k in video_metadata} for e in data['entries']]
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)