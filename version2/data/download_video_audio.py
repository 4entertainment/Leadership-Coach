import os
import yt_dlp


class YouTubePlaylistDownloader:
    """
    A class that downloads videos from a YouTube playlist in the specified mode.

    Attributes:
        output_folder (str): The folder where downloaded files will be saved.
    """

    def __init__(self, output_folder: str = 'output'):
        """
        Initializes the class instance and prepares the output folder.
        """
        self.output_folder = output_folder
        self._ensure_output_folder()

    def _ensure_output_folder(self) -> None:
        """
        Checks if the output folder exists, and creates it if it doesn't.
        """
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def download_playlist(self, playlist_url: str, mode: str = 'video') -> None:
        """
        Downloads the playlist from the specified URL.

        Args:
            playlist_url (str): The URL of the playlist to be downloaded.
            mode (str): Download mode; 'video' or 'audio'.
                        The 'video' mode merges video and audio streams.
                        The 'audio' mode downloads only the audio file.
        Raises:
            ValueError: When an invalid mode is selected.
        """
        if mode == 'video':
            ydl_opts = self._get_video_options()
        elif mode == 'audio':
            ydl_opts = self._get_audio_options()
        else:
            raise ValueError("Invalid mode. Use either 'video' or 'audio'.")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])

    def _get_video_options(self) -> dict:
        """
        Returns the yt_dlp options for video mode.
        """
        return {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(self.output_folder, '%(title)s.%(ext)s'),
            'no-check-certificate': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'noprogress': False,
            'noplaylist': False,
            'ignoreerrors': False,
            'geo_bypass': True,
        }

    def _get_audio_options(self) -> dict:
        """
        Returns the yt_dlp options for audio mode.
        """
        return {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.output_folder, '%(title)s.%(ext)s'),
            'no-check-certificate': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noprogress': False,
            'noplaylist': False,
            'ignoreerrors': False,
            'geo_bypass': True,
        }


def main():
    # URL of the playlist to be downloaded
    playlist_url = 'https://www.youtube.com/playlist?list=PLCi3Q_-uGtdlCsFXHLDDHBSLyq4BkQ6gZ'

    # Kullanıcıdan indirme modunu al: video, audio veya both
    mode = input("Choose the mode you want to download (video, audio, both): ").strip().lower()

    if mode == 'both':
        # Her mod için ayrı klasör oluşturulur
        video_downloader = YouTubePlaylistDownloader(output_folder='video')
        audio_downloader = YouTubePlaylistDownloader(output_folder='audio')

        print("Downloading video mode...")
        video_downloader.download_playlist(playlist_url, mode='video')
        print("Downloading audio mode...")
        audio_downloader.download_playlist(playlist_url, mode='audio')
    elif mode in ('video', 'audio'):
        downloader = YouTubePlaylistDownloader(output_folder=mode)
        downloader.download_playlist(playlist_url, mode=mode)
    else:
        print("Invalid selection. Please use either 'video', 'audio' or 'both'.")


if __name__ == "__main__":
    main()
