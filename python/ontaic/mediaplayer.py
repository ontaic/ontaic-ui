"""Media player component for audio and video."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class MediaType(str, Enum):
    """Media type."""
    VIDEO = "video"
    AUDIO = "audio"


class PlayerSize(str, Enum):
    """Player size."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    FULLSCREEN = "fullscreen"


@dataclass
class MediaSource:
    """Media source."""
    url: str
    type: str = ""
    label: str = ""
    default: bool = False
    
    def to_dict(self) -> dict:
        return {"url": self.url, "type": self.type, "label": self.label, "default": self.default}


@dataclass
class Caption:
    """Media caption/subtitle."""
    label: str
    srclang: str
    url: str
    default: bool = False
    
    def to_dict(self) -> dict:
        return {"label": self.label, "srclang": self.srclang, "url": self.url, "default": self.default}


class MediaPlayer:
    """Media player component for audio and video."""
    
    def __init__(self, src: str = "", media_type: MediaType = MediaType.VIDEO):
        self.src = src
        self.media_type = media_type
        self._sources: List[MediaSource] = []
        self._captions: List[Caption] = []
        self._size: PlayerSize = PlayerSize.MEDIUM
        self._autoplay: bool = False
        self._loop: bool = False
        self._muted: bool = False
        self._controls: bool = True
        self._preload: str = "metadata"
        self._poster: str = ""
        self._width: int = 0
        self._height: int = 0
        self._volume: float = 1
        self._playback_rate: float = 1
        self._show_controls: bool = True
        self._show_time: bool = True
        self._show_volume: bool = True
        self._show_fullscreen: bool = True
        self._show_playback_rate: bool = False
        self._show_picture_in_picture: bool = False
        self._show_download: bool = False
        self._show_sharing: bool = False
        self._custom_controls: List[Dict[str, Any]] = field(default_factory=list)
        self._on_play: Optional[Callable] = None
        self._on_pause: Optional[Callable] = None
        self._on_ended: Optional[Callable] = None
        self._on_time_update: Optional[Callable] = None
        self._on_volume_change: Optional[Callable] = None
        self._on_error: Optional[Callable] = None
        self._on_ready: Optional[Callable] = None
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
        self._disabled: bool = False
    
    def source(self, url: str, media_type: str = "", label: str = "", default: bool = False) -> "MediaPlayer":
        """Add a source."""
        self._sources.append(MediaSource(url=url, type=media_type, label=label, default=default))
        return self
    
    def caption(self, label: str, srclang: str, url: str, default: bool = False) -> "MediaPlayer":
        """Add a caption."""
        self._captions.append(Caption(label=label, srclang=srclang, url=url, default=default))
        return self
    
    def size(self, size: PlayerSize) -> "MediaPlayer":
        """Set player size."""
        self._size = size
        return self
    
    def autoplay(self, autoplay: bool = True) -> "MediaPlayer":
        """Enable autoplay."""
        self._autoplay = autoplay
        return self
    
    def loop(self, loop: bool = True) -> "MediaPlayer":
        """Enable loop."""
        self._loop = loop
        return self
    
    def muted(self, muted: bool = True) -> "MediaPlayer":
        """Enable muted."""
        self._muted = muted
        return self
    
    def poster(self, url: str) -> "MediaPlayer":
        """Set poster image."""
        self._poster = url
        return self
    
    def volume(self, volume: float) -> "MediaPlayer":
        """Set volume (0-1)."""
        self._volume = max(0, min(1, volume))
        return self
    
    def playback_rate(self, rate: float) -> "MediaPlayer":
        """Set playback rate."""
        self._playback_rate = rate
        return self
    
    def on_play(self, callback: Callable) -> "MediaPlayer":
        """Set play handler."""
        self._on_play = callback
        return self
    
    def on_pause(self, callback: Callable) -> "MediaPlayer":
        """Set pause handler."""
        self._on_pause = callback
        return self
    
    def on_ended(self, callback: Callable) -> "MediaPlayer":
        """Set ended handler."""
        self._on_ended = callback
        return self
    
    def on_time_update(self, callback: Callable) -> "MediaPlayer":
        """Set time update handler."""
        self._on_time_update = callback
        return self
    
    def on_error(self, callback: Callable) -> "MediaPlayer":
        """Set error handler."""
        self._on_error = callback
        return self
    
    def on_ready(self, callback: Callable) -> "MediaPlayer":
        """Set ready handler."""
        self._on_ready = callback
        return self
    
    def class_name(self, class_name: str) -> "MediaPlayer":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "MediaPlayer":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "MediaPlayer":
        """Set help text."""
        self._help_text = text
        return self
    
    def disabled(self) -> "MediaPlayer":
        """Make disabled."""
        self._disabled = True
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "src": self.src,
            "mediaType": self.media_type.value,
            "sources": [s.to_dict() for s in self._sources],
            "captions": [c.to_dict() for c in self._captions],
            "size": self._size.value,
            "autoplay": self._autoplay,
            "loop": self._loop,
            "muted": self._muted,
            "controls": self._controls,
            "preload": self._preload,
            "poster": self._poster,
            "width": self._width,
            "height": self._height,
            "volume": self._volume,
            "playbackRate": self._playback_rate,
            "showTime": self._show_time,
            "showVolume": self._show_volume,
            "showFullscreen": self._show_fullscreen,
            "showPlaybackRate": self._show_playback_rate,
            "showDownload": self._show_download,
            "disabled": self._disabled,
            "className": self._class_name,
            "label": self._label,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<label class="player-label">{self._label}</label>' if self._label else ""
        help_html = f'<p class="player-help">{self._help_text}</p>' if self._help_text else ""
        disabled_class = " disabled" if self._disabled else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        size_class = f" player-{self._size.value}"
        
        # Sources
        sources_html = ""
        if self.src:
            sources_html = f'<source src="{self.src}">'
        for src in self._sources:
            type_attr = f' type="{src.type}"' if src.type else ""
            sources_html += f'<source src="{src.url}"{type_attr}>'
        
        # Captions
        tracks_html = ""
        for cap in self._captions:
            default = " default" if cap.default else ""
            tracks_html += f'<track kind="captions" label="{cap.label}" srclang="{cap.srclang}" src="{cap.url}"{default}>'
        
        # Poster
        poster_attr = f' poster="{self._poster}"' if self._poster else ""
        
        # Size
        width_attr = f' width="{self._width}"' if self._width else ""
        height_attr = f' height="{self._height}"' if self._height else ""
        
        # Attributes
        autoplay_attr = " autoplay" if self._autoplay else ""
        loop_attr = " loop" if self._loop else ""
        muted_attr = " muted" if self._muted else ""
        preload_attr = f' preload="{self._preload}"'
        controls_attr = " controls" if self._controls else ""
        
        if self.media_type == MediaType.VIDEO:
            media_html = f'''<video class="player-media"{poster_attr}{width_attr}{height_attr}{autoplay_attr}{loop_attr}{muted_attr}{preload_attr}{controls_attr}>
                {sources_html}
                {tracks_html}
                Your browser does not support the video tag.
            </video>'''
        else:
            media_html = f'''<audio class="player-media"{width_attr}{autoplay_attr}{loop_attr}{muted_attr}{preload_attr}{controls_attr}>
                {sources_html}
                Your browser does not support the audio element.
            </audio>'''
        
        # Custom controls
        controls_html = ""
        if self._show_controls:
            play_btn = '<button type="button" class="player-btn player-play">&#9654;</button>'
            time_html = '<span class="player-time">0:00 / 0:00</span>' if self._show_time else ""
            volume_html = '<input type="range" class="player-volume" min="0" max="1" step="0.1" value="1">' if self._show_volume else ""
            fullscreen_html = '<button type="button" class="player-btn player-fullscreen">&#x26F6;</button>' if self._show_fullscreen else ""
            download_html = '<a href="" download class="player-btn player-download">&#8681;</a>' if self._show_download else ""
            
            controls_html = f'''<div class="player-controls">
                {play_btn}
                <div class="player-progress">
                    <div class="player-progress-bar"></div>
                </div>
                {time_html}
                {volume_html}
                {fullscreen_html}
                {download_html}
            </div>'''
        
        return f'''<div class="media-player{size_class}{disabled_class}{class_attr}">
            {label_html}
            <div class="player-container">
                {media_html}
                {controls_html}
            </div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // Media Player
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const player = document.querySelector('.media-player');
            if (!player) return;
            
            const media = player.querySelector('.player-media');
            const playBtn = player.querySelector('.player-play');
            const progressBar = player.querySelector('.player-progress-bar');
            const progress = player.querySelector('.player-progress');
            const timeDisplay = player.querySelector('.player-time');
            const volumeSlider = player.querySelector('.player-volume');
            const fullscreenBtn = player.querySelector('.player-fullscreen');
            
            if (!media) return;
            
            // Play/Pause
            function togglePlay() {{
                if (media.paused) {{
                    media.play();
                    if (playBtn) playBtn.innerHTML = '&#9646;&#9646;';
                }} else {{
                    media.pause();
                    if (playBtn) playBtn.innerHTML = '&#9654;';
                }}
            }}
            
            if (playBtn) {{
                playBtn.addEventListener('click', togglePlay);
            }}
            
            if (media) {{
                media.addEventListener('click', togglePlay);
            }}
            
            // Progress
            if (media && progressBar) {{
                media.addEventListener('timeupdate', () => {{
                    const percent = (media.currentTime / media.duration) * 100;
                    progressBar.style.width = percent + '%';
                    
                    if (timeDisplay) {{
                        timeDisplay.textContent = formatTime(media.currentTime) + ' / ' + formatTime(media.duration);
                    }}
                }});
            }}
            
            // Progress click
            if (progress && media) {{
                progress.addEventListener('click', (e) => {{
                    const rect = progress.getBoundingClientRect();
                    const pos = (e.clientX - rect.left) / rect.width;
                    media.currentTime = pos * media.duration;
                }});
            }}
            
            // Volume
            if (volumeSlider && media) {{
                volumeSlider.value = media.volume;
                volumeSlider.addEventListener('input', (e) => {{
                    media.volume = e.target.value;
                }});
            }}
            
            // Fullscreen
            if (fullscreenBtn) {{
                fullscreenBtn.addEventListener('click', () => {{
                    const container = player.querySelector('.player-container');
                    if (document.fullscreenElement) {{
                        document.exitFullscreen();
                    }} else {{
                        container.requestFullscreen();
                    }}
                }});
            }}
            
            // Keyboard
            player.addEventListener('keydown', (e) => {{
                switch (e.key) {{
                    case ' ':
                    case 'k':
                        e.preventDefault();
                        togglePlay();
                        break;
                    case 'ArrowLeft':
                        media.currentTime -= 10;
                        break;
                    case 'ArrowRight':
                        media.currentTime += 10;
                        break;
                    case 'ArrowUp':
                        media.volume = Math.min(1, media.volume + 0.1);
                        break;
                    case 'ArrowDown':
                        media.volume = Math.max(0, media.volume - 0.1);
                        break;
                    case 'f':
                        fullscreenBtn.click();
                        break;
                    case 'm':
                        media.muted = !media.muted;
                        break;
                }}
            }});
            
            function formatTime(seconds) {{
                if (isNaN(seconds)) return '0:00';
                const mins = Math.floor(seconds / 60);
                const secs = Math.floor(seconds % 60);
                return mins + ':' + (secs < 10 ? '0' : '') + secs;
            }}
        }})();
        """


def create_video_player(src: str = "") -> MediaPlayer:
    """Create a video player."""
    return MediaPlayer(src, MediaType.VIDEO)


def create_audio_player(src: str = "") -> MediaPlayer:
    """Create an audio player."""
    return MediaPlayer(src, MediaType.AUDIO)


MEDIA_PLAYER_CSS = """
.media-player {
    display: inline-block;
}

.player-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #374151;
}

.player-container {
    position: relative;
    background: #000;
    border-radius: 0.5rem;
    overflow: hidden;
}

.player-media {
    display: block;
    width: 100%;
}

.player-small .player-media {
    max-width: 400px;
}

.player-medium .player-media {
    max-width: 640px;
}

.player-large .player-media {
    max-width: 960px;
}

.player-fullscreen .player-media {
    width: 100vw;
    height: 100vh;
}

.player-controls {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
    color: white;
}

.player-btn {
    background: transparent;
    border: none;
    color: white;
    font-size: 1.25rem;
    cursor: pointer;
    padding: 0.25rem;
}

.player-btn:hover {
    color: #3b82f6;
}

.player-progress {
    flex: 1;
    height: 4px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 2px;
    cursor: pointer;
}

.player-progress:hover {
    height: 6px;
}

.player-progress-bar {
    height: 100%;
    background: #3b82f6;
    border-radius: 2px;
    width: 0%;
}

.player-time {
    font-size: 0.875rem;
    font-family: monospace;
}

.player-volume {
    width: 80px;
}

.player-download {
    text-decoration: none;
}

.player-help {
    margin-top: 0.5rem;
    font-size: 0.875rem;
    color: #6b7280;
}

.media-player.disabled {
    opacity: 0.5;
    pointer-events: none;
}

/* Audio player specific */
.media-player.audio .player-container {
    background: #f3f4f6;
    border-radius: 2rem;
    padding: 1rem 1.5rem;
}

.media-player.audio .player-controls {
    position: static;
    background: transparent;
    padding: 0;
}

.media-player.audio .player-btn {
    color: #374151;
}

.media-player.audio .player-progress {
    background: #d1d5db;
}

.media-player.audio .player-progress-bar {
    background: #3b82f6;
}

.media-player.audio .player-time {
    color: #6b7280;
}
"""
