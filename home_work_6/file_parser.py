import sys
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUMENT = []
DOCX_DOCUMENT = []
TXT_DOCUMENT = []
PDF_DOCUMENT = []
XLSX_DOCUMENT = []
PPTX_DOCUMENT = []
OTHER = []
ARCHIVES = []

REGISTER_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_DOCUMENT,
    'DOCX': DOCX_DOCUMENT,
    'TXT': TXT_DOCUMENT,
    'PDF': PDF_DOCUMENT,
    'XLSX': XLSX_DOCUMENT,
    'PPTX': PPTX_DOCUMENT,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    # перетворюємо розширення файла в назві папки .jpg -> JPG
    return Path(filename).suffix[1:].upper()


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        # якщо папка то додаємо її у список FOLDERS і переходимо до наступного елементу папки
        if item.is_dir():
            # перевіряємо щоб це не була папка у яку ми вже складаємо файли
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'OTHER'):
                FOLDERS.append(item)
                #  скануємо цю вкладену папку - рекурсія
                scan(item)
            #  переходимо о наступного елементу у скануємій папці
            continue

        #  робота з файлом
        ext = get_extension(item.name)  # взяти розширення
        fullname = folder / item.name  # повний шлях до файлу
        if not ext:  # нема розширення - додати до невідомих
            OTHER.append(fullname)
        else:
            try:
                # беремо список у кий покладемо весь шлях до файлу
                container = REGISTER_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(fullname)
            except KeyError:
                # Если мы не регистрировали расширение в REGISTER_EXTENSIONS, то добавить в другое
                UNKNOWN.add(ext)
                OTHER.append(fullname)


if __name__ == '__main__':
    folder_for_scan = sys.argv[1]
    print(f'Start in folder {folder_for_scan}')

    scan(Path(folder_for_scan))
    print(f'Images jpeg: {JPEG_IMAGES}')
    print(f'Images jpg: {JPG_IMAGES}')
    print(f'Images png: {PNG_IMAGES}')
    print(f'Images svg: {SVG_IMAGES}')

    print(f'Audio mp3: {MP3_AUDIO}')
    print(f'Audio wav: {WAV_AUDIO}')
    print(f'Audio amr: {AMR_AUDIO}')
    print(f'Audio ogg: {OGG_AUDIO}')

    print(f'Video avi: {AVI_VIDEO}')
    print(f'Video mp4: {MP4_VIDEO}')
    print(f'Video mov: {MOV_VIDEO}')
    print(f'Video mkv: {MKV_VIDEO}')

    print(f'Document doc: {DOC_DOCUMENT}')
    print(f'Document docx: {DOCX_DOCUMENT}')
    print(f'Document txt: {TXT_DOCUMENT}')
    print(f'Document pdf: {PDF_DOCUMENT}')
    print(f'Document xlsx: {XLSX_DOCUMENT}')
    print(f'Document pptx: {PPTX_DOCUMENT}')

    print(f'Archives: {ARCHIVES}')

    print(f'Types of files in folder: {EXTENSIONS}')
    print(f'Unknown files of types: {UNKNOWN}')

    print(FOLDERS[::-1])
