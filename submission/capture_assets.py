"""Capture UI screenshots and create demo video for submission."""
import asyncio
import subprocess
from pathlib import Path

from playwright.async_api import async_playwright

BASE = "http://localhost:3000"
OUT = Path(r"c:\Users\digital metro\Documents\Scanned Documents\aegis-resolve\submission\UI_Screenshots")
VIDEO = Path(r"c:\Users\digital metro\Documents\Scanned Documents\aegis-resolve\submission\Demo_Video.mp4")

PAGES = [
    ("01_landing_page.png", "/"),
    ("02_customer_dashboard.png", "/customer"),
    ("03_customer_case_detail.png", "/customer/disputes/AR-2026-002"),
    ("04_merchant_dashboard.png", "/merchant"),
    ("05_merchant_case_detail.png", "/merchant/cases/AR-2026-002"),
    ("06_admin_control_center.png", "/admin"),
    ("07_admin_courtroom_dossier.png", "/admin/cases/AR-2026-002"),
    ("08_file_dispute.png", "/customer/file-dispute"),
]


async def capture_screenshots():
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        for filename, route in PAGES:
            url = f"{BASE}{route}"
            print(f"Capturing {url} -> {filename}")
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            await page.wait_for_timeout(3000)
            await page.screenshot(path=str(OUT / filename), full_page=True)
        await browser.close()
    print(f"Screenshots saved to {OUT}")


def create_video_from_screenshots():
    """Create MP4 slideshow from screenshots using ffmpeg if available."""
    images = sorted(OUT.glob("*.png"))
    if not images:
        print("No screenshots found for video")
        return False

    list_file = OUT / "ffmpeg_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for img in images:
            f.write(f"file '{img.as_posix()}'\n")
            f.write("duration 3\n")
        f.write(f"file '{images[-1].as_posix()}'\n")

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x06182c",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        str(VIDEO),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"Demo video created: {VIDEO}")
            list_file.unlink(missing_ok=True)
            return True
        print(f"ffmpeg failed: {result.stderr[:500]}")
    except FileNotFoundError:
        print("ffmpeg not found, trying imageio fallback")
    except subprocess.TimeoutExpired:
        print("ffmpeg timed out")

    try:
        import imageio.v2 as imageio
        import numpy as np
        from PIL import Image

        frames = []
        for img_path in images:
            img = Image.open(img_path).convert("RGB")
            img.thumbnail((1280, 720), Image.LANCZOS)
            canvas = Image.new("RGB", (1280, 720), (6, 24, 44))
            x = (1280 - img.width) // 2
            y = (720 - img.height) // 2
            canvas.paste(img, (x, y))
            for _ in range(90):  # 3 sec at 30fps
                frames.append(np.array(canvas))

        imageio.mimwrite(str(VIDEO), frames, fps=30, codec="libx264", quality=8)
        print(f"Demo video created via imageio: {VIDEO}")
        return True
    except ImportError:
        print("Installing imageio for video generation...")
        subprocess.run(["pip", "install", "imageio", "imageio-ffmpeg", "pillow", "-q"], check=True)
        import imageio.v2 as imageio
        import numpy as np
        from PIL import Image
        frames = []
        for img_path in images:
            img = Image.open(img_path).convert("RGB")
            img.thumbnail((1280, 720), Image.LANCZOS)
            canvas = Image.new("RGB", (1280, 720), (6, 24, 44))
            x = (1280 - img.width) // 2
            y = (720 - img.height) // 2
            canvas.paste(img, (x, y))
            for _ in range(90):
                frames.append(np.array(canvas))
        imageio.mimwrite(str(VIDEO), frames, fps=30, codec="libx264", quality=8)
        print(f"Demo video created via imageio: {VIDEO}")
        return True


async def main():
    # Wait for servers
    import urllib.request
    for i in range(30):
        try:
            urllib.request.urlopen(BASE, timeout=2)
            print("Frontend is ready")
            break
        except Exception:
            await asyncio.sleep(2)
            print(f"Waiting for frontend... ({i+1}/30)")

    await capture_screenshots()
    create_video_from_screenshots()


if __name__ == "__main__":
    asyncio.run(main())
