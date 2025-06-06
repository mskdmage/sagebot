import os
import glob
from pathlib import Path
from typing import Optional, List


def get_user_download_paths() -> List[Path]:
    user_home = Path.home()
    download_paths = [
        user_home / "Downloads",
        user_home / "Descargas",
    ]
    return [path for path in download_paths if path.exists() and path.is_dir()]


def get_latest_file(extension: str, search_paths: Optional[List[Path]] = None) -> Optional[str]:
    """Devuelve la ruta del archivo más reciente con la extensión especificada"""
    extension = extension.lower().lstrip('.')
    
    if search_paths is None:
        search_paths = get_user_download_paths()
    
    latest_file = None
    latest_time = 0
    
    for search_path in search_paths:
        try:
            pattern = str(search_path / f"*.{extension}")
            files = glob.glob(pattern)
            
            pattern_subdir = str(search_path / "*" / f"*.{extension}")
            files.extend(glob.glob(pattern_subdir))
            
            for file_path in files:
                try:
                    file_path_obj = Path(file_path)
                    if file_path_obj.is_file():
                        mod_time = file_path_obj.stat().st_mtime
                        if mod_time > latest_time:
                            latest_time = mod_time
                            latest_file = file_path_obj
                except (OSError, IOError):
                    continue
        except (OSError, IOError):
            continue
    
    return str(latest_file) if latest_file else None


if __name__ == "__main__":
    print(get_latest_file('exe'))
