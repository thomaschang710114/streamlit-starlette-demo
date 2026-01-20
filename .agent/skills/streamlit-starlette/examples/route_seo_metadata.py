# Capability: SEO Endpoints
# Use when: You need to serve robots.txt, sitemap.xml, or manifest.json.

from streamlit.starlette import App
from starlette.routing import Route
from starlette.responses import PlainTextResponse, Response, JSONResponse


async def robots_txt(request):
    """Serve robots.txt for search engine crawlers."""
    return PlainTextResponse(
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        "Sitemap: https://myapp.com/sitemap.xml"
    )


async def sitemap_xml(request):
    """Serve sitemap.xml for search engine indexing."""
    sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://myapp.com/</loc></url>
  <url><loc>https://myapp.com/dashboard</loc></url>
</urlset>"""
    return Response(sitemap, media_type="application/xml")


async def manifest_json(request):
    """Serve manifest.json for PWA support."""
    return JSONResponse(
        {
            "name": "My Analytics App",
            "short_name": "Analytics",
            "description": "Interactive data dashboard",
            "icons": [{"src": "/static/icon-192.png", "sizes": "192x192"}],
            "theme_color": "#ff4b4b",
            "background_color": "#ffffff",
            "display": "standalone",
        }
    )


app = App(
    "dashboard.py",
    routes=[
        Route("/robots.txt", robots_txt),
        Route("/sitemap.xml", sitemap_xml),
        Route("/manifest.json", manifest_json),
    ],
)

# Run: uvicorn app:app --reload
