from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import qrcode
from django.test import Client, SimpleTestCase, override_settings


class DownloadPageTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_has_download_and_android_instructions(self):
        response = self.client.get("/", HTTP_HOST="localhost")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Download Primera")
        self.assertContains(response, "Allow this installation")
        self.assertContains(response, "primera-wordmark.png")

    def test_qr_encodes_absolute_download_url(self):
        with patch("primera_download.views.qrcode.make", wraps=qrcode.make) as make_qr:
            with override_settings(ALLOWED_HOSTS=["downloads.example"]):
                response = self.client.get(
                    "/qr/", secure=True, HTTP_HOST="downloads.example"
                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/svg+xml")
        self.assertIn(b"<svg", response.content)
        self.assertEqual(make_qr.call_args.args[0], "https://downloads.example/download/")

    def test_missing_apk_returns_setup_message(self):
        with TemporaryDirectory() as temporary_directory:
            missing_apk = Path(temporary_directory) / "missing.apk"
            with override_settings(APK_PATH=missing_apk):
                response = self.client.get("/download/", HTTP_HOST="localhost")

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"has not been added yet", response.content)

    def test_existing_apk_is_served_as_download(self):
        with TemporaryDirectory() as temporary_directory:
            apk_path = Path(temporary_directory) / "primera.apk"
            apk_path.write_bytes(b"apk-test-payload")
            with override_settings(APK_PATH=apk_path):
                response = self.client.get("/download/", HTTP_HOST="localhost")
                body = b"".join(response.streaming_content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.android.package-archive")
        self.assertIn("filename=\"Primera.apk\"", response["Content-Disposition"])
        self.assertEqual(body, b"apk-test-payload")