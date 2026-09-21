"""File upload handling for ontaic."""
import os
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
import mimetypes


@dataclass
class UploadedFile:
    """Uploaded file representation."""
    filename: str
    content_type: str
    size: int
    path: str
    data: bytes = b""
    
    def save(self, destination: str):
        """Save the file to a destination."""
        dest_path = Path(destination)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.data:
            dest_path.write_bytes(self.data)
        elif self.path:
            import shutil
            shutil.copy2(self.path, dest_path)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "content_type": self.content_type,
            "size": self.size,
        }


class FileUploader:
    """File upload handler."""
    
    def __init__(
        self,
        upload_dir: str = "uploads",
        max_size: int = 10 * 1024 * 1024,  # 10MB
        allowed_types: List[str] = None,
        generate_filename: bool = True,
    ):
        self.upload_dir = Path(upload_dir)
        self.max_size = max_size
        self.allowed_types = allowed_types or [
            "image/jpeg", "image/png", "image/gif", "image/webp",
            "application/pdf", "text/plain",
        ]
        self.generate_filename = generate_filename
        self._validators: List[Callable] = []
        self._processors: List[Callable] = []
    
    def validate(self, validator: Callable):
        """Add a validator function."""
        self._validators.append(validator)
    
    def process(self, processor: Callable):
        """Add a processor function."""
        self._processors.append(processor)
    
    def is_valid_type(self, content_type: str) -> bool:
        """Check if the content type is allowed."""
        if not self.allowed_types:
            return True
        return content_type in self.allowed_types
    
    def is_valid_size(self, size: int) -> bool:
        """Check if the file size is within limits."""
        return size <= self.max_size
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename."""
        ext = Path(original_filename).suffix
        unique_name = f"{uuid.uuid4().hex}{ext}"
        return unique_name
    
    def save_file(self, file_data: bytes, filename: str, content_type: str = None) -> UploadedFile:
        """Save a file and return the UploadedFile object."""
        # Determine content type
        if not content_type:
            content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        
        # Check file type
        if not self.is_valid_type(content_type):
            raise ValueError(f"File type {content_type} is not allowed")
        
        # Check file size
        if not self.is_valid_size(len(file_data)):
            raise ValueError(f"File size exceeds maximum of {self.max_size} bytes")
        
        # Generate unique filename if needed
        if self.generate_filename:
            save_filename = self.generate_unique_filename(filename)
        else:
            save_filename = filename
        
        # Create upload directory
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = self.upload_dir / save_filename
        file_path.write_bytes(file_data)
        
        # Create UploadedFile object
        uploaded = UploadedFile(
            filename=save_filename,
            content_type=content_type,
            size=len(file_data),
            path=str(file_path),
            data=file_data,
        )
        
        # Run processors
        for processor in self._processors:
            uploaded = processor(uploaded)
        
        return uploaded
    
    def delete_file(self, filename: str) -> bool:
        """Delete a file."""
        file_path = self.upload_dir / filename
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    
    def get_file_path(self, filename: str) -> Optional[Path]:
        """Get the full path to a file."""
        file_path = self.upload_dir / filename
        if file_path.exists():
            return file_path
        return None
    
    def list_files(self) -> List[str]:
        """List all uploaded files."""
        if not self.upload_dir.exists():
            return []
        return [f.name for f in self.upload_dir.iterdir() if f.is_file()]


class ImageUploader(FileUploader):
    """Image-specific uploader with processing."""
    
    def __init__(self, upload_dir: str = "uploads/images", **kwargs):
        allowed_types = kwargs.pop("allowed_types", [
            "image/jpeg", "image/png", "image/gif", "image/webp",
        ])
        super().__init__(upload_dir=upload_dir, allowed_types=allowed_types, **kwargs)
        
        # Add image processing
        self.process(self._process_image)
    
    def _process_image(self, file: UploadedFile) -> UploadedFile:
        """Process image file (resize, compress, etc.)."""
        # This is a placeholder - in production, you'd use Pillow or similar
        return file
    
    def create_thumbnail(self, filename: str, size: tuple = (200, 200)) -> Optional[UploadedFile]:
        """Create a thumbnail of an image."""
        # Placeholder for thumbnail creation
        return None


class DocumentUploader(FileUploader):
    """Document-specific uploader."""
    
    def __init__(self, upload_dir: str = "uploads/documents", **kwargs):
        allowed_types = kwargs.pop("allowed_types", [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
            "text/csv",
        ])
        super().__init__(upload_dir=upload_dir, allowed_types=allowed_types, **kwargs)


# JavaScript code for client-side file uploads
def generate_upload_js_code() -> str:
    """Generate JavaScript code for file uploads."""
    return """
    // File Upload Handler
    const fileUploader = {
        uploadDir: 'uploads',
        
        async uploadFile(file, endpoint = '/api/upload') {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData,
            });
            
            if (!response.ok) {
                throw new Error('Upload failed');
            }
            
            return await response.json();
        },
        
        validateFile(file, options = {}) {
            const { maxSize = 10 * 1024 * 1024, allowedTypes = [] } = options;
            
            if (file.size > maxSize) {
                throw new Error('File size exceeds limit');
            }
            
            if (allowedTypes.length > 0 && !allowedTypes.includes(file.type)) {
                throw new Error('File type not allowed');
            }
            
            return true;
        },
        
        previewFile(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsDataURL(file);
            });
        },
        
        createDropZone(element, onDrop) {
            element.addEventListener('dragover', (e) => {
                e.preventDefault();
                element.classList.add('drag-over');
            });
            
            element.addEventListener('dragleave', () => {
                element.classList.remove('drag-over');
            });
            
            element.addEventListener('drop', (e) => {
                e.preventDefault();
                element.classList.remove('drag-over');
                const files = Array.from(e.dataTransfer.files);
                onDrop(files);
            });
        }
    };
    
    // Example usage
    async function handleFileUpload(inputElement) {
        const file = inputElement.files[0];
        if (!file) return;
        
        try {
            fileUploader.validateFile(file, {
                maxSize: 5 * 1024 * 1024,
                allowedTypes: ['image/jpeg', 'image/png', 'image/gif'],
            });
            
            const result = await fileUploader.uploadFile(file);
            console.log('Upload successful:', result);
        } catch (error) {
            console.error('Upload failed:', error.message);
        }
    }
    """


# Example upload component
class UploadComponent:
    """Example upload component for forms."""
    
    def __init__(
        self,
        name: str = "file",
        multiple: bool = False,
        accept: str = "*/*",
        max_size: int = 10 * 1024 * 1024,
        class_name: str = "",
    ):
        self.name = name
        self.multiple = multiple
        self.accept = accept
        self.max_size = max_size
        self.class_name = class_name
    
    def render(self) -> str:
        multiple_attr = "multiple" if self.multiple else ""
        return f"""
        <div class="upload-container {self.class_name}">
            <input 
                type="file" 
                name="{self.name}" 
                accept="{self.accept}"
                {multiple_attr}
                class="hidden"
                id="upload-{self.name}"
                onchange="handleFileUpload(this)"
            />
            <label 
                for="upload-{self.name}"
                class="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100"
            >
                <div class="flex flex-col items-center justify-center pt-5 pb-6">
                    <svg class="w-8 h-8 mb-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                    </svg>
                    <p class="mb-2 text-sm text-gray-500"><span class="font-semibold">Click to upload</span> or drag and drop</p>
                    <p class="text-xs text-gray-500">SVG, PNG, JPG or GIF (MAX. {self.max_size // (1024 * 1024)}MB)</p>
                </div>
            </label>
        </div>
        """
