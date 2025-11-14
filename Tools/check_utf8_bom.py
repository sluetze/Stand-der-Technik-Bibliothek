import os
from pathlib import Path
from codecs import BOM_UTF8

def has_bom(file_path):
    """Check if file has UTF-8 BOM"""
    try:
        with open(file_path, 'rb') as f:
            first_bytes = f.read(3)
            return first_bytes == BOM_UTF8
    except:
        return False

def main():
    repo_root = Path('.')
    bom_files = []

    # Text file extensions
    text_extensions = {
        '.bat', '.cfg', '.conf', '.css', '.csv', '.html', '.ini', '.js',
        '.json', '.md', '.ps1', '.py', '.scss', '.sh', '.sql', '.toml',
        '.ts', '.txt', '.xml', '.yaml', '.yml'
    }

    print("Checking for UTF-8 BOM in text files...")
    print("=" * 50)

    for file_path in repo_root.rglob('*'):
        if (file_path.is_file() and
            file_path.suffix.lower() in text_extensions and
            not any(pattern in str(file_path) for pattern in ['.git', 'node_modules', '__pycache__'])):

            if has_bom(file_path):
                print(f"{file_path}: Contains UTF-8 BOM")
                bom_files.append(file_path)
            else:
                print(f"{file_path}: No BOM")

    if bom_files:
        print(f"\nFound {len(bom_files)} files with UTF-8 BOM:")
        for file_path in bom_files:
            print(f"  - {file_path}")
        # Software developers:
        # If consuming UTF-8, recognize and discard a BOM.
        # If producing UTF-8, include a BOM only if explicitly directed to do so, or if a BOM is known to be required by a protocol.
        # Text authors:
        # Do not use U+FEFF to function as a zero width no-break space character; use U+2060 WORD JOINER instead.
        # Include a BOM if one is known to be required by a targeted protocol.
        # Otherwise, include a BOM when authoring a UTF-8 text file that contains non-ASCII characters, is not targeting a specific protocol, but which may be opened by applications that will not assume UTF-8 by default. (This is useful on systems like Microsoft Windows where some applications assume text files to be encoded with the Active Code Page.)
        # Otherwise, do not include a BOM.
        # Source: https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-23/#G23824
        # Source: https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-2/#G19274
        # Don't fail the build for BOM, just warn
    else:
        print("No UTF-8 BOM found in text files!")

if __name__ == "__main__":
    main()