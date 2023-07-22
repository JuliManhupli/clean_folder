import os
import shutil
import sys
from string import ascii_letters

CATEGORIES = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'videos': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'music': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR'),
    'other': (),
}

TRANSLITERATION = {
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z',
    'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
    'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
    'Ю': 'Yu', 'Я': 'Ya',
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ye', 'ж': 'zh', 'з': 'z',
    'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
    'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ю': 'yu', 'я': 'ya'
}


def normalize(file: str) -> str:
    """
    This function takes a filename as input and normalizes it using transliteration and replacing illegal characters

    :param file: filename to normalize
    :return: normalized filename
    """
    file_name, extension = os.path.splitext(file)
    normalized_file = ''
    for char in file_name:
        if char.isdigit() or char in ascii_letters:
            normalized_file += char
        elif char in TRANSLITERATION:
            normalized_file += TRANSLITERATION[char]
        else:
            normalized_file += '_'
    return normalized_file + extension


def delete_empty_folders(folder_path: str) -> None:
    """
    This function checks all directories of the specified folder and deletes empty folders

    :param folder_path: base directory
    :return: None
    """
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            path = os.path.join(root, dir)
            if not os.listdir(path):
                os.rmdir(path)


def extract_archive(source_path: str, target_path: str) -> None:
    """
    This function extracts the archive at the source path to the target path

    :param source_path: path to the archive file
    :param target_path: path to extract the archive contents
    :return: None
    """
    try:
        shutil.unpack_archive(source_path, target_path)
    except shutil.ReadError:
        print('It is not archive')


def print_information(folder_path: str, known_extensions: set, unknown_extensions: set) -> None:
    """
        This function prints information about the sorted files

        :param folder_path: base directory
        :param known_extensions: set of known file extensions
        :param unknown_extensions: set of unknown file extensions
        :return: None
    """
    for category in CATEGORIES:
        category_folder = os.path.join(folder_path, category)
        print(f"{category}:")
        if os.path.exists(category_folder):
            category_files = os.listdir(category_folder)
            if category_files:
                for file in category_files:
                    print(f"  - {file}")
            else:
                print("  - No files")
        else:
            print("  - No folder")
        print()

    print("Known extensions:")
    print(known_extensions)

    print("\nUnknown extensions:")
    print(unknown_extensions)


def process_folder(folder_path: str) -> None:
    """
    This function processes the files in the specified folder, categorizes them, renames them, and moves them to
    their respective category folders.

    :param folder_path: base directory
    :return: None
    """
    known_extensions = set()
    unknown_extensions = set()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            extension = os.path.splitext(file)[1][1:].upper()

            target_category = None
            for category, extensions in CATEGORIES.items():
                if extension in extensions:
                    target_category = category
                    known_extensions.add(extension)
                    break
            if target_category is None:
                target_category = 'other'
                unknown_extensions.add(extension)

            # Renaming the file
            source_path = os.path.join(root, file)
            normalized_file = normalize(file)
            target_path = os.path.join(root, normalized_file)
            os.rename(source_path, target_path)

            # Moving the file to the category folder
            target_category_folder = os.path.join(folder_path, target_category)
            if not os.path.exists(target_category_folder):
                os.makedirs(target_category_folder)
            target_file_path = os.path.join(target_category_folder, normalized_file)
            shutil.move(target_path, target_file_path)

            if target_category == 'archives':
                archive_path = os.path.join(target_category_folder, normalized_file)
                extract_folder = os.path.splitext(archive_path)[0]
                extract_archive(archive_path, extract_folder)

    print_information(folder_path, known_extensions, unknown_extensions)


def main() -> None:
    if len(sys.argv) != 2:
        print("Error! Usage: python sort.py <folder_path>")
        return

    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print("Folder not found")
        return

    process_folder(folder_path)
    delete_empty_folders(folder_path)

    print("Sorting completed.")


if __name__ == '__main__':
    main()
