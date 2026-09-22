"""File upload component with preview and progress."""
import os
import json
import base64
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class UploadStatus(str, Enum):
    """Upload status."""
    IDLE = "idle"
    UPLOADING = "uploading"
    SUCCESS = "success"
    ERROR = "error"


class FileType(str, Enum):
    """File type categories."""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    ARCHIVE = "archive"
    ANY = "any"


MIME_TYPES = {
    FileType.IMAGE: ["image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml", "image/bmp", "image/tiff"],
    FileType.VIDEO: ["video/mp4", "video/webm", "video/ogg", "video/quicktime"],
    FileType.AUDIO: ["audio/mpeg", "audio/wav", "audio/ogg", "audio/webm", "audio/mp3"],
    FileType.DOCUMENT: ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                         "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                         "text/plain", "text/csv"],
    FileType.ARCHIVE: ["application/zip", "application/x-rar-compressed", "application/x-7z-compressed", "application/gzip"],
}

EXTENSION_MAP = {
    ".jpg": FileType.IMAGE, ".jpeg": FileType.IMAGE, ".png": FileType.IMAGE, ".gif": FileType.IMAGE,
    ".webp": FileType.IMAGE, ".svg": FileType.IMAGE, ".bmp": FileType.IMAGE, ".tiff": FileType.IMAGE,
    ".mp4": FileType.VIDEO, ".webm": FileType.VIDEO, ".mov": FileType.VIDEO,
    ".mp3": FileType.AUDIO, ".wav": FileType.AUDIO, ".ogg": FileType.AUDIO,
    ".pdf": FileType.DOCUMENT, ".doc": FileType.DOCUMENT, ".docx": FileType.DOCUMENT,
    ".xls": FileType.DOCUMENT, ".xlsx": FileType.DOCUMENT, ".txt": FileType.DOCUMENT, ".csv": FileType.DOCUMENT,
    ".zip": FileType.ARCHIVE, ".rar": FileType.ARCHIVE, ".7z": FileType.ARCHIVE, ".gz": FileType.ARCHIVE,
}


@dataclass
class UploadedFile:
    """Uploaded file information."""
    name: str
    size: int
    type: str
    data: Any = None
    url: Optional[str] = None
    preview_url: Optional[str] = None
    status: UploadStatus = UploadStatus.IDLE
    progress: float = 0
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_image(self) -> bool:
        return self.type.startswith("image/")
    
    @property
    def is_video(self) -> bool:
        return self.type.startswith("video/")
    
    @property
    def is_audio(self) -> bool:
        return self.type.startswith("audio/")
    
    @property
    def extension(self) -> str:
        _, ext = os.path.splitext(self.name)
        return ext.lower()
    
    @property
    def file_type(self) -> FileType:
        return EXTENSION_MAP.get(self.extension, FileType.ANY)
    
    @property
    def size_formatted(self) -> str:
        """Format file size."""
        for unit in ["B", "KB", "MB", "GB"]:
            if self.size < 1024:
                return f"{self.size:.1f} {unit}"
            self.size /= 1024
        return f"{self.size:.1f} TB"
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "size": self.size,
            "type": self.type,
            "url": self.url,
            "previewUrl": self.preview_url,
            "status": self.status.value,
            "progress": self.progress,
            "error": self.error,
            "metadata": self.metadata,
        }


@dataclass
class UploadConfig:
    """Upload configuration."""
    accept: List[str] = field(default_factory=list)
    multiple: bool = False
    max_files: int = 0
    max_size: int = 10 * 1024 * 1024  # 10MB
    file_types: List[FileType] = field(default_factory=lambda: [FileType.ANY])
    auto_upload: bool = False
    upload_url: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    with_credentials: bool = False
    
    @property
    def accept_string(self) -> str:
        """Generate accept attribute string."""
        if self.accept:
            return ",".join(self.accept)
        
        extensions = []
        for ft in self.file_types:
            if ft in MIME_TYPES:
                extensions.extend(MIME_TYPES[ft])
        
        return ",".join(extensions)


class FileUpload:
    """File upload component with preview."""
    
    def __init__(self, name: str = "files", config: UploadConfig = None):
        self.name = name
        self.config = config or UploadConfig()
        self._files: List[UploadedFile] = []
        self._on_change: Optional[Callable] = None
        self._on_upload: Optional[Callable] = None
        self._on_remove: Optional[Callable] = None
        self._on_error: Optional[Callable] = None
        self._drag_active: bool = False
        self._class_name: str = ""
        self._label: str = ""
        self._help_text: str = ""
        self._disabled: bool = False
        self._show_preview: bool = True
        self._show_progress: bool = True
        self._preview_size: int = 120
        self._list_type: str = "text"  # text, picture, picture-card
    
    def set_files(self, files: List[UploadedFile]):
        """Set files."""
        self._files = files
    
    def add_file(self, file: UploadedFile):
        """Add a file."""
        if self.config.max_files and len(self._files) >= self.config.max_files:
            return
        
        if file.size > self.config.max_size:
            file.status = UploadStatus.ERROR
            file.error = f"File too large. Maximum size: {self.config.max_size // 1024 // 1024}MB"
        
        self._files.append(file)
    
    def remove_file(self, index: int):
        """Remove a file."""
        if 0 <= index < len(self._files):
            removed = self._files.pop(index)
            if self._on_remove:
                self._on_remove(removed)
    
    def on_change(self, callback: Callable) -> "FileUpload":
        """Set change handler."""
        self._on_change = callback
        return self
    
    def on_upload(self, callback: Callable) -> "FileUpload":
        """Set upload handler."""
        self._on_upload = callback
        return self
    
    def on_remove(self, callback: Callable) -> "FileUpload":
        """Set remove handler."""
        self._on_remove = callback
        return self
    
    def on_error(self, callback: Callable) -> "FileUpload":
        """Set error handler."""
        self._on_error = callback
        return self
    
    def class_name(self, class_name: str) -> "FileUpload":
        """Set CSS class."""
        self._class_name = class_name
        return self
    
    def label(self, label: str) -> "FileUpload":
        """Set label."""
        self._label = label
        return self
    
    def help_text(self, text: str) -> "FileUpload":
        """Set help text."""
        self._help_text = text
        return self
    
    def disabled(self) -> "FileUpload":
        """Make disabled."""
        self._disabled = True
        return self
    
    def show_preview(self, show: bool = True) -> "FileUpload":
        """Show file preview."""
        self._show_preview = show
        return self
    
    def show_progress(self, show: bool = True) -> "FileUpload":
        """Show upload progress."""
        self._show_progress = show
        return self
    
    def preview_size(self, size: int) -> "FileUpload":
        """Set preview size."""
        self._preview_size = size
        return self
    
    def list_type(self, list_type: str) -> "FileUpload":
        """Set list type (text, picture, picture-card)."""
        self._list_type = list_type
        return self
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "config": {
                "accept": self.config.accept,
                "multiple": self.config.multiple,
                "maxFiles": self.config.max_files,
                "maxSize": self.config.max_size,
                "fileTypes": [ft.value for ft in self.config.file_types],
                "autoUpload": self.config.auto_upload,
                "uploadUrl": self.config.upload_url,
            },
            "files": [f.to_dict() for f in self._files],
            "class_name": self._class_name,
            "label": self._label,
            "helpText": self._help_text,
            "disabled": self._disabled,
            "showPreview": self._show_preview,
            "showProgress": self._show_progress,
            "previewSize": self._preview_size,
            "listType": self._list_type,
        }
    
    def to_html(self) -> str:
        """Generate HTML."""
        label_html = f'<label class="upload-label">{self._label}</label>' if self._label else ""
        help_html = f'<p class="upload-help">{self._help_text}</p>' if self._help_text else ""
        disabled_class = " disabled" if self._disabled else ""
        class_attr = f" {self._class_name}" if self._class_name else ""
        
        accept = self.config.accept_string
        multiple = " multiple" if self.config.multiple else ""
        
        files_html = ""
        for i, file in enumerate(self._files):
            preview = ""
            if self._show_preview and file.preview_url:
                preview = f'<img src="{file.preview_url}" alt="{file.name}" class="upload-preview-img">'
            elif self._show_preview and file.is_image and file.data:
                preview = f'<img src="{file.data}" alt="{file.name}" class="upload-preview-img">'
            elif self._show_preview:
                ext = file.extension.lstrip(".").upper() or "?"
                preview = f'<div class="upload-preview-icon">{ext}</div>'
            
            progress = ""
            if self._show_progress and file.status == UploadStatus.UPLOADING:
                progress = f'<div class="upload-progress"><div class="upload-progress-bar" style="width: {file.progress}%"></div></div>'
            
            status_class = f" upload-file-{file.status.value}"
            
            files_html += f'''<div class="upload-file{status_class}" data-index="{i}">
                {preview}
                <div class="upload-file-info">
                    <span class="upload-file-name">{file.name}</span>
                    <span class="upload-file-size">{file.size_formatted}</span>
                    {progress}
                </div>
                <button type="button" class="upload-file-remove" data-index="{i}">&times;</button>
            </div>'''
        
        return f'''<div class="upload-container{disabled_class}{class_attr}">
            {label_html}
            <div class="upload-dragger">
                <input type="file" id="{self.name}" name="{self.name}" class="upload-input"{accept}{multiple}{' disabled' if self._disabled else ''}>
                <div class="upload-dragger-content">
                    <svg class="upload-icon" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                    <p class="upload-text">Drag & drop files here, or <span class="upload-browse">browse</span></p>
                    <p class="upload-hint">Max file size: {self.config.max_size // 1024 // 1024}MB</p>
                </div>
            </div>
            <div class="upload-list">{files_html}</div>
            {help_html}
        </div>'''
    
    def generate_js_code(self) -> str:
        """Generate JavaScript."""
        config = self.to_dict()
        return f"""
        // File Upload
        (function() {{
            const config = {str(config).replace("'", '"')};
            
            const container = document.querySelector('.upload-container');
            if (!container) return;
            
            const input = container.querySelector('.upload-input');
            const dragger = container.querySelector('.upload-dragger');
            const list = container.querySelector('.upload-list');
            
            // Click to browse
            dragger.addEventListener('click', (e) => {{
                if (e.target === dragger || e.target.classList.contains('upload-dragger-content')) {{
                    input.click();
                }}
            }});
            
            // File selection
            input.addEventListener('change', (e) => {{
                const files = Array.from(e.target.files);
                handleFiles(files);
            }});
            
            // Drag and drop
            dragger.addEventListener('dragover', (e) => {{
                e.preventDefault();
                dragger.classList.add('drag-over');
            }});
            
            dragger.addEventListener('dragleave', (e) => {{
                dragger.classList.remove('drag-over');
            }});
            
            dragger.addEventListener('drop', (e) => {{
                e.preventDefault();
                dragger.classList.remove('drag-over');
                const files = Array.from(e.dataTransfer.files);
                handleFiles(files);
            }});
            
            function handleFiles(files) {{
                files.forEach(file => {{
                    if (config.config.maxFiles > 0 && list.children.length >= config.config.maxFiles) {{
                        alert('Maximum files reached');
                        return;
                    }}
                    
                    if (file.size > config.config.maxSize) {{
                        alert('File too large: ' + file.name);
                        return;
                    }}
                    
                    const reader = new FileReader();
                    reader.onload = (e) => {{
                        const preview = file.type.startsWith('image/') ? e.target.result : null;
                        addFileToList(file, preview);
                    }};
                    reader.readAsDataURL(file);
                }});
            }}
            
            function addFileToList(file, preview) {{
                const item = document.createElement('div');
                item.className = 'upload-file';
                item.innerHTML = `
                    ${{preview ? `<img src="${{preview}}" class="upload-preview-img">` : `<div class="upload-preview-icon">${{file.name.split('.').pop().toUpperCase()}}</div>`}}
                    <div class="upload-file-info">
                        <span class="upload-file-name">${{file.name}}</span>
                        <span class="upload-file-size">${{formatSize(file.size)}}</span>
                    </div>
                    <button type="button" class="upload-file-remove">&times;</button>
                `;
                
                item.querySelector('.upload-file-remove').addEventListener('click', () => {{
                    item.remove();
                }});
                
                list.appendChild(item);
            }}
            
            function formatSize(bytes) {{
                const units = ['B', 'KB', 'MB', 'GB'];
                let i = 0;
                while (bytes >= 1024 && i < units.length - 1) {{
                    bytes /= 1024;
                    i++;
                }}
                return bytes.toFixed(1) + ' ' + units[i];
            }}
        }})();
        """


def create_file_upload(name: str = "files", config: UploadConfig = None) -> FileUpload:
    """Create a file upload."""
    return FileUpload(name, config)


def create_image_upload(name: str = "images", multiple: bool = True) -> FileUpload:
    """Create an image upload."""
    config = UploadConfig(
        file_types=[FileType.IMAGE],
        multiple=multiple,
        max_size=10 * 1024 * 1024,
    )
    upload = FileUpload(name, config)
    upload.list_type("picture-card")
    return upload


FILE_UPLOAD_CSS = """
.upload-container {
    width: 100%;
}

.upload-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #374151;
}

.upload-dragger {
    border: 2px dashed #d1d5db;
    border-radius: 0.5rem;
    padding: 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    background: #fafafa;
}

.upload-dragger:hover {
    border-color: #9ca3af;
    background: #f9fafb;
}

.upload-dragger.drag-over {
    border-color: #3b82f6;
    background: #eff6ff;
}

.upload-input {
    display: none;
}

.upload-icon {
    color: #9ca3af;
    margin-bottom: 0.5rem;
}

.upload-text {
    color: #6b7280;
    margin: 0.5rem 0;
}

.upload-browse {
    color: #3b82f6;
    cursor: pointer;
    font-weight: 500;
}

.upload-browse:hover {
    text-decoration: underline;
}

.upload-hint {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-top: 0.25rem;
}

.upload-list {
    margin-top: 1rem;
}

.upload-file {
    display: flex;
    align-items: center;
    padding: 0.75rem;
    border: 1px solid #e5e7eb;
    border-radius: 0.375rem;
    margin-bottom: 0.5rem;
    background: white;
}

.upload-preview-img {
    width: 48px;
    height: 48px;
    object-fit: cover;
    border-radius: 0.375rem;
    margin-right: 0.75rem;
}

.upload-preview-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f3f4f6;
    border-radius: 0.375rem;
    margin-right: 0.75rem;
    font-weight: 600;
    font-size: 0.75rem;
    color: #6b7280;
}

.upload-file-info {
    flex: 1;
    min-width: 0;
}

.upload-file-name {
    display: block;
    font-weight: 500;
    color: #111827;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.upload-file-size {
    font-size: 0.75rem;
    color: #6b7280;
}

.upload-file-remove {
    padding: 0.25rem 0.5rem;
    background: transparent;
    border: none;
    color: #9ca3af;
    cursor: pointer;
    font-size: 1.25rem;
    line-height: 1;
}

.upload-file-remove:hover {
    color: #dc2626;
}

.upload-progress {
    margin-top: 0.5rem;
}

.upload-progress-bar {
    height: 4px;
    background: #3b82f6;
    border-radius: 2px;
    transition: width 0.3s ease;
}

.upload-file-success {
    border-color: #10b981;
}

.upload-file-error {
    border-color: #ef4444;
}

.upload-help {
    margin-top: 0.5rem;
    font-size: 0.875rem;
    color: #6b7280;
}

/* Picture card list type */
.upload-list.picture-card {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 1rem;
}

.upload-list.picture-card .upload-file {
    flex-direction: column;
    padding: 0;
    overflow: hidden;
}

.upload-list.picture-card .upload-preview-img {
    width: 100%;
    height: 120px;
    margin: 0;
    border-radius: 0;
}

.upload-list.picture-card .upload-preview-icon {
    width: 100%;
    height: 120px;
    margin: 0;
    border-radius: 0;
}

.upload-list.picture-card .upload-file-info {
    padding: 0.5rem;
}

.upload-list.picture-card .upload-file-remove {
    position: absolute;
    top: 0.25rem;
    right: 0.25rem;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}
"""
