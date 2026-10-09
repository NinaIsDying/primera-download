from io import BytesIO

import qrcode
from qrcode.image.svg import SvgPathImage
from django.conf import settings
from django.http import FileResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse


def home(request):
    return render(request, "index.html")


def download_apk(request):
    if not settings.APK_PATH.is_file():
        return HttpResponseNotFound(
            "The Primera APK has not been added yet. Add it at "
            "web-download/downloads/primera.apk and try again.",
            content_type="text/plain; charset=utf-8",
        )
    return FileResponse(
        settings.APK_PATH.open("rb"),
        as_attachment=True,
        filename="Primera.apk",
        content_type="application/vnd.android.package-archive",
    )


def download_qr(request):
    download_url = request.build_absolute_uri(reverse("download_apk"))
    image = qrcode.make(download_url, image_factory=SvgPathImage, box_size=10, border=4)
    image_bytes = BytesIO()
    image.save(image_bytes)
    response = HttpResponse(image_bytes.getvalue(), content_type="image/svg+xml")
    response["Cache-Control"] = "public, max-age=300"
    return response