import os
from pathlib import Path

def has_bom(file_path):
    """Check if file has UTF-8 BOM"""
    try:
        with open(file_path, 'rb') as f:
            first_bytes = f.read(3)
            return first_bytes == b'\xef\xbb\xbf'
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
        print("\n According to the Unicode Standard, BOM is generally neither required norrecommended for text files.")
        print(" see https://www.unicode.org/versions/Unicode5.0.0/ch02.pdf Page 36 for more information.")
        print("   To remove BOM, you can use:")
        print("   - sed -i '1s/^\xEF\xBB\xBF//' <file>")
        print("   - Or configure your editor to save without BOM")
        # Don't fail the build for BOM, just warn
    else:
        print("No UTF-8 BOM found in text files!")

if __name__ == "__main__":
    main()