# modules/downloader.py

import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tempfile
import os
import shutil
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC
import requests

class DownloadManager:
    def __init__(self):
        self.spotify_creds = {
            'client_id': os.environ.get('SPOTIPY_CLIENT_ID'),
            'client_secret': os.environ.get('SPOTIPY_CLIENT_SECRET')
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
        # Creamos la carpeta temporal una sola vez
        temp_dir = tempfile.mkdtemp()
        try:
            if plataforma == 'Spotify':
                return self._download_spotify(url, formato, calidad, noplaylist, temp_dir)
            
            if tipo == 'Audio':
                return self._download_audio(url, formato, calidad, noplaylist, temp_dir)
            
            return self._download_video(url, formato, calidad, noplaylist, temp_dir)
        except Exception as e:
            # En caso de error, borramos la carpeta temporal
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
            raise e

    def _get_final_path(self, temp_dir):
        # Esta función encuentra el archivo que yt-dlp realmente creó
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            if os.path.isfile(file_path):
                return file_path, filename
        raise Exception("No se encontró el archivo descargado.")

    def _download_audio(self, url, formato, calidad, noplaylist, temp_dir):
        outtmpl = os.path.join(temp_dir, '%(title)s.%(ext)s')
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': formato,
                'preferredquality': calidad,
            }],
            'noplaylist': not noplaylist,
            'ignoreerrors': False,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return self._get_final_path(temp_dir)

    def _download_video(self, url, formato, calidad, noplaylist, temp_dir):
        outtmpl = os.path.join(temp_dir, '%(title)s.%(ext)s')
        height = calidad.replace('p', '') if calidad != 'best' else 'best'
        ydl_opts = {
            'format': f'bestvideo[height<={height}][ext={formato}]+bestaudio/best',
            'outtmpl': outtmpl,
            'merge_output_format': formato,
            'noplaylist': not noplaylist,
            'ignoreerrors': False,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return self._get_final_path(temp_dir)

    def _download_spotify(self, url, formato, calidad, noplaylist, temp_dir):
        sp = self.get_spotify()
        
        def tag_and_save(path, info):
            audio = ID3(path)
            audio.add(TIT2(encoding=3, text=info['name']))
            audio.add(TPE1(encoding=3, text=info['artists'][0]['name']))
            audio.add(TALB(encoding=3, text=info['album']['name']))
            img = requests.get(info['album']['images'][0]['url']).content
            audio.add(APIC(encoding=3, mime='image/jpeg', type=3, data=img))
            audio.save()
        
        tracks = []
        if 'playlist' in url and not noplaylist:
            tracks = [item['track'] for item in sp.playlist_tracks(url)['items'] if item['track']]
        else:
            tracks = [sp.track(url)]

        if len(tracks) > 1:
            raise Exception('Descarga de playlists no soportada por descarga directa')

        track = tracks[0]
        query = f"{track['artists'][0]['name']} - {track['name']} audio"

        outtmpl = os.path.join(temp_dir, '%(title)s.%(ext)s')
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': formato,
                'preferredquality': calidad
            }],
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch:{query}"])
        
        final_path, filename = self._get_final_path(temp_dir)
        tag_and_save(final_path, track)
        return final_path, filename