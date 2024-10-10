from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the YouTuber's name from the form
        youtuber_name = request.form['youtuber_name']

        # Use the YouTube Data API to get the YouTuber's channel ID
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={youtuber_name}&key=YOUR_API_KEY"
        response = requests.get(url)
        data = response.json()
        channel_id = data['items'][0]['id']['channelId']

        # Redirect to the channel page
        return redirect(url_for('channel', channel_id=channel_id))
    else:
        return render_template('index.html')

@app.route('/channel/<channel_id>')
def channel(channel_id):
    # Use the YouTube Data API to get the YouTuber's channel information
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key=YOUR_API_KEY"
    response = requests.get(url)
    data = response.json()
    channel_info = data['items'][0]

    # Get the latest videos from the channel
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&order=date&maxResults=5&key=YOUR_API_KEY"
    response = requests.get(url)
    data = response.json()
    videos = data['items']

    return render_template('channel.html', channel_info=channel_info, videos=videos)

if __name__ == '__main__':
    app.run(debug=True)
