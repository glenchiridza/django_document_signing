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

from .models import Document,Signature



def sign_pdf_file(pdf_file_handle,signature):
    doc: typing.Optional[Document] = None
    doc = PDF.loads(pdf_file_handle)

    assert doc is not None

    # create Page
    page: Page = doc.get_page(0)

    # add Page to Document
    doc.add_page(page)

    # set a PageLayout
    layout: PageLayout = SingleColumnLayout(page)

    # add an Image
    layout.add(
        Image(
            Path("static/signature.png"),
            width=Decimal(100),
            height=Decimal(50),
            horizontal_alignment=Alignment.RIGHT,
            vertical_alignment=Alignment.BOTTOM
        )
    )

    # store
    with open("output.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)
