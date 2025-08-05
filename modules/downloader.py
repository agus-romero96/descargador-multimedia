# --- modules/downloader.py ---
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tempfile
import os
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC
import requests

class DownloadManager:
    def __init__(self):
        self.spotify_creds = {
            'client_id': '79220c1558cb410c9bdb102f77d67447',
            'client_secret': '3b9aa57d9c7143728611a584889abab8'
        }

    def get_spotify(self):
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=self.spotify_creds['client_id'],
            client_secret=self.spotify_creds['client_secret']
        ))

    def get_options(self):
        return {
            'plataformas': ['YouTube', 'Spotify'],
            'tipos': ['Audio', 'Video'],
            'formatos_audio': ['mp3', 'wav', 'aac'],
            'calidades_audio': ['320', '192', '128'],
            'formatos_video': ['mp4', 'mkv', 'webm'],
            'calidades_video': ['1080p', '720p', '480p', 'best']
        }

    def download(self, plataforma, tipo, url, formato, calidad, noplaylist):
        if plataforma == 'Spotify':
            return self._download_spotify(url, formato, calidad, noplaylist)
        if tipo == 'Audio':
            return self._download_audio(url, formato, calidad, noplaylist)
        return self._download_video(url, formato, calidad, noplaylist)
    def _download_audio(self, url, formato, calidad, noplaylist):
        # Crear archivo temporal
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{formato}')
        tmp.close()
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': tmp.name,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': formato,
                'preferredquality': calidad,
            }],
            'noplaylist': not noplaylist,
            'ignoreerrors': True,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        filename = os.path.basename(tmp.name)
        return tmp.name, filename

    def _download_video(self, url, formato, calidad, noplaylist):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{formato}')
        tmp.close()
        height = calidad.replace('p', '') if calidad != 'best' else 'best'
        ydl_opts = {
            'format': f'bestvideo[height<={height}][ext={formato}]+bestaudio/best',
            'outtmpl': tmp.name,
            'merge_output_format': formato,
            'noplaylist': not noplaylist,
            'ignoreerrors': True,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        filename = os.path.basename(tmp.name)
        return tmp.name, filename

    def _download_spotify(self, url, formato, calidad, noplaylist):
        sp = self.get_spotify()
        def tag_and_save(path, info):
            audio = ID3(path)
            audio.add(TIT2(encoding=3, text=info['name']))
            audio.add(TPE1(encoding=3, text=info['artists'][0]['name']))
            audio.add(TALB(encoding=3, text=info['album']['name']))
            img = requests.get(info['album']['images'][0]['url']).content
            audio.add(APIC(encoding=3, mime='image/jpeg', type=3, data=img))
            audio.save()
        # Uso sencillo: solo primer item o playlist completo
        tracks = []
        if 'playlist' in url and not noplaylist:
            tracks = [item['track'] for item in sp.playlist_tracks(url)['items'] if item['track']]
        else:
            tracks = [sp.track(url)]

        # Si es más de una pista, no soportado en stream directo
        if len(tracks) > 1:
            raise Exception('Descarga de playlists no soportada por descarga directa')

        track = tracks[0]
        query = f"{track['artists'][0]['name']} - {track['name']} audio"
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{formato}')
        tmp.close()
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': formato,
                'preferredquality': calidad
            }],
            'outtmpl': tmp.name,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch:{query}"])
        tag_and_save(tmp.name, track)
        filename = os.path.basename(tmp.name)
        return tmp.name, filename
