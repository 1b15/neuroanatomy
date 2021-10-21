import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import minecart

RELEVANT_COLORS = [(0.573, 0.816, 0.314),
                   (0.773, 0.878, 0.706),
                   (0.663, 0.82, 0.557),
                   (0.98, 0.753, 0.565)]

def same_color(c1, c2):
    for i in range(3):
        if abs(c1[i] - c2[i]) > 0.01:
            return False
    return True

def relevant_color(c):
    return any([same_color(c, rc) for rc in RELEVANT_COLORS])

pdf_files = list(filter(lambda s: s.endswith('.pdf'),
                        os.listdir()))

for filename in pdf_files:
    print(f'Processing {filename}...')
    pdf = minecart.Document(open(filename, "rb"))
    relevant_pages = set()
    for i, page in enumerate(pdf.iter_pages()):
        for shape in page.shapes:
            for marker in (shape.fill, shape.stroke):
                if marker and relevant_color(marker.color.as_rgb()):
                    relevant_pages.add(i)

    pdf_reader = PdfFileReader(open(filename, "rb"))
    pdf_writer = PdfFileWriter()
    for i in sorted(list(relevant_pages)):
        pdf_writer.addPage(pdf_reader.getPage(i))
    if not os.path.isdir('relevant'):
        os.mkdir('relevant')
    with open('relevant/' + filename.split('.')[0] \
              + '_relevant.pdf', 'wb') as out:
        pdf_writer.write(out)
