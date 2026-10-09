# Primera Download Site

A small Django site for the Primera Android app download. The page uses the existing Primera wordmark, Quicksand fonts, and colors from the Android app theme.

## Run locally

From this directory:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DJANGO_DEBUG = "true"
py manage.py runserver
```

Open http://127.0.0.1:8000. The browser refreshes when you save template, CSS, or Python changes. The QR code is generated for the current site's `/download/` URL, so deployed scans resolve to the deployed host.

## Add the APK

Place the signed release package at `downloads/primera.apk`. The download button and QR both open `/download/`; until the APK exists, that endpoint responds with a clear 404 message. To store the APK elsewhere, set `PRIMERA_APK_PATH` to its absolute path.

## Deployment settings

Set `DJANGO_SECRET_KEY` to a long, random secret, `DJANGO_ALLOWED_HOSTS` to the deployed hostname(s), and `DJANGO_DEBUG=false`. Collect static assets with `py manage.py collectstatic --noinput`, then run with a production WSGI server, for example:

```powershell
gunicorn primera_download.wsgi:application
```

Serve the collected `staticfiles/` directory through the hosting platform or a static file server. The deployment must use HTTPS for reliable camera scanning and APK delivery.