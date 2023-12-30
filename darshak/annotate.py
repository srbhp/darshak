import popplerqt5


def extract(fn):
    doc = popplerqt5.Poppler.Document.load(fn)
    annotations = []
    for i in range(doc.numPages()):
        page = doc.page(i)
        for annot in page.annotations():
            contents = annot.contents()
            if contents:
                annotations.append(contents)
                print(f"page={i + 1} {contents}")

    print(f"{len(annotations)} annotation(s) found")
    return annotations


# annotate the pdf Document
def annotate(fn, annotations):
    doc = popplerqt5.Poppler.Document.load(fn)
    for i in range(doc.numPages()):
        page = doc.page(i)
        for annot in page.annotations():
            contents = annot.contents()
            if contents:
                annot.setContents(annotations[i])
                print(f"page={i + 1} {contents}")
    doc.save(fn)
    print(f"{fn} saved")
    return True


# Draw a Square on the page
def draw_square(page, x, y, width, height, color):
    annot = popplerqt5.Poppler.Annotation.create(popplerqt5.Poppler.Annotation.Square)
    annot.setContents(color)
    annot.setGeometry(x, y, width, height)
    page.addAnnotation(annot)
    return annot


# Draw a Circle on the page
def draw_circle(page, x, y, width, height, color):
    annot = popplerqt5.Poppler.Annotation.create(popplerqt5.Poppler.Annotation.Circle)
    annot.setContents(color)
    annot.setGeometry(x, y, width, height)
    page.addAnnotation(annot)
    return annot


# Draw a Line on the page
def draw_line(page, x, y, width, height, color):
    annot = popplerqt5.Poppler.Annotation.create(popplerqt5.Poppler.Annotation.Line)
    annot.setContents(color)
    annot.setGeometry(x, y, width, height)
    page.addAnnotation(annot)
    return annot
