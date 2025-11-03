import yt_dlp

def download(episode, target_folder):
    ydl_opts = {
        'outtmpl': f'{target_folder}/{episode.get('episode')}',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(episode.get('manifest_url'))

