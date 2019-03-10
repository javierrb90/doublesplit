import sys
from pathlib import Path
from . import comicparser, settings
# import comicparser, settings

for target in settings.targets:
    comicparser.parseComic(target,config=settings.config)

# try:
#     path_package = sys.argv[1]
#     new_path = Path(sys.argv[1])

#     comicparser.parseComic(new_path)
# except IndexError:
#     print("ERROR: Si no me das el path del archivo comprimido entonces no podemos hacer nada")