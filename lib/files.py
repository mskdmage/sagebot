"""File handling and manipulation classes for automation workflows."""

import glob
import shutil
from pathlib import Path
from typing import Optional, List

from .bot import BotContext

class FileStep:
    """Base class for all file manipulation steps."""
    
    @staticmethod
    def get_user_download_paths() -> List[Path]:
        """Get list of common download directories that exist on the system.
        
        Returns:
            List of Path objects representing existing download directories.
        """
        user_home = Path.home()
        download_paths = [
            user_home / "Downloads",
            user_home / "Descargas",  # Spanish downloads folder
        ]
        return [path for path in download_paths if path.exists() and path.is_dir()]
    
    @staticmethod
    def get_latest_file(extension: str, reference_name: Optional[str] = None, search_paths: Optional[List[Path]] = None) -> Optional[str]:
        """Find the most recently modified file with the given extension.
        
        Args:
            extension: File extension to search for (with or without dot).
            reference_name: Optional string that must be present in the filename. 
                          If None or empty, returns the newest file with the extension.
            search_paths: Optional list of paths to search. If None, uses default download paths.
            
        Returns:
            Path to the latest matching file as string, or None if no matching file found.
        """
        extension = extension.lower().lstrip('.')
        
        if search_paths is None:
            search_paths = FileStep.get_user_download_paths()
        
        if not search_paths:
            return None
            
        latest_file = None
        latest_time = 0
        
        for search_path in search_paths:
            try:
                # Search in main directory
                pattern = str(search_path / f"*.{extension}")
                files = glob.glob(pattern)
                
                # Search in immediate subdirectories
                pattern_subdir = str(search_path / "*" / f"*.{extension}")
                files.extend(glob.glob(pattern_subdir))
                
                for file_path in files:
                    try:
                        file_path_obj = Path(file_path)
                        if file_path_obj.is_file():
                            # If reference_name is provided and not empty, check if it's in the filename
                            if reference_name and reference_name.strip():
                                if reference_name.lower() not in file_path_obj.name.lower():
                                    continue
                            
                            mod_time = file_path_obj.stat().st_mtime
                            if mod_time > latest_time:
                                latest_time = mod_time
                                latest_file = file_path_obj
                    except (OSError, IOError, AttributeError):
                        continue
            except (OSError, IOError):
                continue
        
        return str(latest_file) if latest_file else None

class CopyLatestFileInFolder(FileStep):
    """Copy the latest file with a specific extension from download folders."""
    
    def __init__(self, extension: str, destination_dir: str, reference_name: Optional[str] = None, new_name: Optional[str] = None, search_paths: Optional[List[Path]] = None) -> None:
        """Initialize copy latest file step.
        
        Args:
            extension: File extension to search for.
            destination_dir: Directory to copy the file to.
            reference_name: Optional reference string that must be in filename. Defaults to None.
            new_name: Optional new name for the copied file. Defaults to None.
            search_paths: Optional list of paths to search. Defaults to None.
        """
        self.extension = extension
        self.destination_dir = destination_dir
        self.reference_name = reference_name
        self.new_name = f"{new_name}_{BotContext.generate_timestamp()}.{extension}" if new_name else f"file_{BotContext.generate_timestamp()}.{extension}"
        self.search_paths = search_paths
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the copy latest file step.
        
        Args:
            context: The bot context for logging.
            
        Returns:
            The bot context (unchanged).
        """
        try:
            latest_file = self.get_latest_file(
                extension=self.extension,
                reference_name=self.reference_name,
                search_paths=self.search_paths
            )
            
            if not latest_file:
                BotContext.log_action(context, f"No file found with extension .{self.extension}", "❌")
                return context
            
            source_path = Path(latest_file)
            dest_dir = Path(self.destination_dir)
            
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            dest_path = dest_dir / self.new_name
            
            shutil.copy2(source_path, dest_path)
            BotContext.log_action(context, f"Copied {source_path.name} to {dest_path}", "📁")
            
        except Exception as e:
            BotContext.log_action(context, f"Error copying file: {e}", "❌")
        
        return context

class CopyFile(FileStep):
    """Copy a file from source to destination path."""
    
    def __init__(self, source_path: str, destination_path: str, preserve_metadata: bool = True) -> None:
        """Initialize file copy step.
        
        Args:
            source_path: Path to the source file.
            destination_path: Path to the destination file.
            preserve_metadata: Whether to preserve file metadata. Defaults to True.
        """
        self.source_path = Path(source_path)
        self.destination_path = Path(destination_path)
        self.preserve_metadata = preserve_metadata
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the file copy step.
        
        Args:
            context: The bot context for logging.
            
        Returns:
            The bot context (unchanged).
        """
        try:
            if not self.source_path.exists():
                BotContext.log_action(context, f"Source file does not exist: {self.source_path}", "❌")
                return context
            
            # Create destination directory if it doesn't exist
            self.destination_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy the file
            if self.preserve_metadata:
                shutil.copy2(self.source_path, self.destination_path)
            else:
                shutil.copy(self.source_path, self.destination_path)
            
            BotContext.log_action(context, f"Copied {self.source_path.name} to {self.destination_path}", "📁")
            
        except Exception as e:
            BotContext.log_action(context, f"Error copying file: {e}", "❌")
        
        return context

class MoveFile(FileStep):
    """Move a file from source to destination path."""
    
    def __init__(self, source_path: str, destination_path: str) -> None:
        """Initialize file move step.
        
        Args:
            source_path: Path to the source file.
            destination_path: Path to the destination file.
        """
        self.source_path = Path(source_path)
        self.destination_path = Path(destination_path)
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the file move step.
        
        Args:
            context: The bot context for logging.
            
        Returns:
            The bot context (unchanged).
        """
        try:
            if not self.source_path.exists():
                BotContext.log_action(context, f"Source file does not exist: {self.source_path}", "❌")
                return context
            
            # Create destination directory if it doesn't exist
            self.destination_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move the file
            shutil.move(str(self.source_path), str(self.destination_path))
            BotContext.log_action(context, f"Moved {self.source_path.name} to {self.destination_path}", "🚚")
            
        except Exception as e:
            BotContext.log_action(context, f"Error moving file: {e}", "❌")
        
        return context

class DeleteFile(FileStep):
    """Delete a file at the specified path."""
    
    def __init__(self, file_path: str, force: bool = False) -> None:
        """Initialize file deletion step.
        
        Args:
            file_path: Path to the file to delete.
            force: Whether to force deletion by removing read-only attributes. Defaults to False.
        """
        self.file_path = Path(file_path)
        self.force = force
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the file deletion step.
        
        Args:
            context: The bot context for logging.
            
        Returns:
            The bot context (unchanged).
        """
        try:
            if not self.file_path.exists():
                BotContext.log_action(context, f"File does not exist: {self.file_path}", "⚠️")
                return context
            
            if not self.file_path.is_file():
                BotContext.log_action(context, f"Path is not a file: {self.file_path}", "❌")
                return context
            
            if self.force:
                # Remove read-only attribute if it exists
                self.file_path.chmod(0o777)
            
            self.file_path.unlink()
            BotContext.log_action(context, f"Deleted {self.file_path.name}", "🗑️")
            
        except Exception as e:
            BotContext.log_action(context, f"Error deleting file: {e}", "❌")
        
        return context