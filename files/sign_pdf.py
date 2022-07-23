#!chapter_002/src/snippet_028.py
from pathlib import Path

from borb.pdf import Alignment
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.pdf import PDF
from borb.pdf.canvas.layout.image.image import Image
import typing

from decimal import Decimal


def sign_pdf_file(pdf_name, pdf_file, signature_url, page_num):
    print(pdf_file)
    doc: typing.Optional[Document] = None
    with open(pdf_file, "rb") as pdf_file_handle:
        doc = PDF.loads(pdf_file_handle)

    assert doc is not None

    # check if page_num was not specified or less that zero
    if page_num < 0 or page_num > len(doc.items()):
        page_num = 0
    # pagenum-1 because count starts from zero
    page: Page = doc.get_page(page_num - 1)

    # add Page to Document
    doc.add_page(page)

    # set a PageLayout
    layout: PageLayout = SingleColumnLayout(page)

    # add an Image
    layout.add(
        Image(
            signature_url,
            width=Decimal(100),
            height=Decimal(50),
            horizontal_alignment=Alignment.RIGHT,
            vertical_alignment=Alignment.BOTTOM
        )
    )

    # store
    with open(f"media/signed_documents/{pdf_name}.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)
