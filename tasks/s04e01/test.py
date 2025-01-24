import os
import sys
from pathlib import Path
import logging

# Get the absolute path to the project root directory
project_root = Path(__file__).resolve().parents[2]

# Add the project root to sys.path
sys.path.append(str(project_root))

from src.api.aidevs3.uploader import Uploader

taskname = "photos"
uploader = Uploader(taskname)


description = """Biała kobieta o jasnej karnacji. Posiada długie, proste, czarne włosy opadające za ramiona. Twarz jest owalna, z wyraźnie zarysowanymi rysami i jasną karnacją. Oczy są jasne, niebieskie.  Kobieta ma na sobie duże, prostokątne okulary z czarnymi oprawami. Kobieta posiada tatuaż na lewym ramieniu. Tatuaż na ramieniu jest czarny, kształt przypomina owada, pszczołę, muchę albo pajaka. Kobieta ubrana jest w szarką koszulkę z krótkim rękawem. Kobieta ma szczupłe dłonie. Kobieta na lewym nadgarstku lewej ręki nosi czarną opaskę sportową lub smartwatch. Kobieta ma szczupłą sylwetkę."""
r = uploader.send_data_as_conversation(description)
print(r)