import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def render_terminal():
    html = Path(r"D:\workspace\steplog\examples\terminal.html").resolve()
    out = Path(r"D:\workspace\steplog\assets\terminal-preview.png")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(f"file:///{html.as_posix()}", wait_until="networkidle")
        await page.wait_for_timeout(2000)
        term = page.locator(".term")
        box = await term.bounding_box()
        await page.screenshot(path=str(out), clip={"x": box["x"]-40, "y": box["y"]-40, "width": box["width"]+80, "height": box["height"]+80})
        await browser.close()
    print(f"Terminal: {out} ({out.stat().st_size} bytes)")

async def render_arch():
    mermaid = """flowchart TD
    S1["step()"] --> F["forge output"]
    S2["spinner()"] --> F
    O["output.* helpers"] --> F
    F --> T["Terminal"]
    S1 -.->|"exception"| E["✗ failure indicator"]
    """
    import urllib.request
    req = urllib.request.Request(
        "https://kroki.io/mermaid/png",
        data=mermaid.encode("utf-8"),
        headers={"Content-Type": "text/plain"},
    )
    try:
        resp = urllib.request.urlopen(req)
        out = Path(r"D:\workspace\steplog\assets\architecture.png")
        out.write_bytes(resp.read())
        print(f"Kroki arch: {out} ({out.stat().st_size} bytes)")
    except Exception as e:
        print(f"Kroki failed ({e}), rendering via Playwright")
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400">
  <rect width="800" height="400" fill="#0f172a" rx="8"/>
  <text x="400" y="50" text-anchor="middle" fill="#e2e8f0" font-family="sans-serif" font-size="20" font-weight="bold">steplog Architecture</text>
  <rect x="50" y="100" width="160" height="60" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <text x="130" y="135" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="14">step()</text>
  <rect x="320" y="100" width="160" height="60" rx="6" fill="#1e293b" stroke="#22c55e" stroke-width="2"/>
  <text x="400" y="135" text-anchor="middle" fill="#22c55e" font-family="monospace" font-size="14">spinner()</text>
  <rect x="590" y="100" width="160" height="60" rx="6" fill="#1e293b" stroke="#f472b6" stroke-width="2"/>
  <text x="670" y="135" text-anchor="middle" fill="#f472b6" font-family="monospace" font-size="14">output.*</text>
  <rect x="250" y="240" width="300" height="60" rx="6" fill="#1e293b" stroke="#e2e8f0" stroke-width="2"/>
  <text x="400" y="275" text-anchor="middle" fill="#e2e8f0" font-family="monospace" font-size="14">Terminal Output</text>
  <line x1="130" y1="160" x2="350" y2="240" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="400" y1="160" x2="400" y2="240" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="670" y1="160" x2="450" y2="240" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="50" y="300" width="160" height="50" rx="6" fill="#2d1b1b" stroke="#ef4444" stroke-width="1" stroke-dasharray="4"/>
  <text x="130" y="330" text-anchor="middle" fill="#ef4444" font-family="monospace" font-size="12">✗ failure branch</text>
  <line x1="130" y1="160" x2="130" y2="300" stroke="#ef4444" stroke-width="1" stroke-dasharray="4"/>
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/></marker></defs>
</svg>'''
        html = f"<!DOCTYPE html><html><body style='margin:0;background:#0f172a;'>{svg}</body></html>"
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": 800, "height": 420})
            await page.set_content(html, wait_until="networkidle")
            await page.wait_for_timeout(1000)
            out = Path(r"D:\workspace\steplog\assets\architecture.png")
            await page.screenshot(path=str(out))
            await browser.close()
        print(f"Playwright arch: {out} ({out.stat().st_size} bytes)")

async def main():
    await render_terminal()
    await render_arch()

asyncio.run(main())
