"""
Download images from keyboards.json, resize with ImageMagick, upload to S3,
and produce keyboards_s3.json with S3 URLs + thumbnail_url field.

Stdlib only. Uses ImageMagick and AWS CLI via subprocess.
"""

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

USER_AGENT = "clacker-fyi/0.1 by saad"
S3_BUCKET = "clacker-fyi-images"
S3_REGION = "us-east-1"
S3_BASE_URL = f"https://{S3_BUCKET}.s3.amazonaws.com"
MAX_LONG_SIDE = 2560
THUMB_LONG_SIDE = 768
JPEG_QUALITY = 85
SLEEP_BETWEEN = 1.0
MAX_RETRIES = 3
INPUT_PATH = "keyboards.json"
OUTPUT_PATH = "keyboards_s3.json"
SERVER_DATA_PATH = os.path.join("..", "server", "data", "keyboards.json")


def download_image(url, dest_path):
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                with open(dest_path, "wb") as f:
                    shutil.copyfileobj(resp, f)
            return True
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            if attempt < MAX_RETRIES - 1:
                print(f"    retry {attempt + 1}/{MAX_RETRIES} for {url}: {e}")
                time.sleep(2)
            else:
                print(f"    FAILED to download {url}: {e}")
                return False


def resize_image(input_path, output_path, max_side):
    cmd = [
        "magick", input_path,
        "-resize", f"{max_side}x{max_side}>",
        "-quality", str(JPEG_QUALITY),
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    magick error: {result.stderr.strip()}")
        return False
    return True


def s3_upload(local_path, s3_key):
    s3_uri = f"s3://{S3_BUCKET}/{s3_key}"
    cmd = [
        "aws", "s3", "cp", local_path, s3_uri,
        "--content-type", "image/jpeg",
        "--region", S3_REGION,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    s3 upload error: {result.stderr.strip()}")
        return False
    return True


def process_entry(entry, tmpdir):
    kb_id = entry["id"]
    image_urls = entry.get("image_urls", [])
    new_image_urls = []
    thumbnail_url = None

    for idx, url in enumerate(image_urls):
        raw_path = os.path.join(tmpdir, f"{kb_id}_{idx}_raw")
        resized_path = os.path.join(tmpdir, f"{kb_id}_{idx}.jpg")

        if not download_image(url, raw_path):
            new_image_urls.append(url)  # keep original on failure
            continue

        time.sleep(SLEEP_BETWEEN)

        if not resize_image(raw_path, resized_path, MAX_LONG_SIDE):
            new_image_urls.append(url)
            continue

        s3_key = f"images/{kb_id}/{idx}.jpg"
        if not s3_upload(resized_path, s3_key):
            new_image_urls.append(url)
            continue

        new_image_urls.append(f"{S3_BASE_URL}/{s3_key}")

        # thumbnail from first image only
        if idx == 0:
            thumb_path = os.path.join(tmpdir, f"{kb_id}_thumb.jpg")
            if resize_image(raw_path, thumb_path, THUMB_LONG_SIDE):
                thumb_key = f"thumbnails/{kb_id}.jpg"
                if s3_upload(thumb_path, thumb_key):
                    thumbnail_url = f"{S3_BASE_URL}/{thumb_key}"
                os.remove(thumb_path)

        os.remove(raw_path)
        os.remove(resized_path)

    # fallback thumbnail if processing failed
    if thumbnail_url is None and new_image_urls:
        thumbnail_url = new_image_urls[0]

    return new_image_urls, thumbnail_url


def main():
    with open(INPUT_PATH) as f:
        keyboards = json.load(f)

    total = len(keyboards)
    output = []
    failed = 0

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, entry in enumerate(keyboards):
            kb_id = entry["id"]
            n_images = len(entry.get("image_urls", []))
            print(f"[{i + 1}/{total}] {kb_id}: {n_images} image(s)...", end=" ", flush=True)

            try:
                new_urls, thumb_url = process_entry(entry, tmpdir)
                new_entry = copy.deepcopy(entry)
                new_entry["image_urls"] = new_urls
                new_entry["thumbnail_url"] = thumb_url
                output.append(new_entry)
                print("done")
            except Exception as e:
                print(f"ERROR: {e}")
                failed += 1
                fallback = copy.deepcopy(entry)
                fallback["thumbnail_url"] = entry["image_urls"][0] if entry.get("image_urls") else None
                output.append(fallback)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nWrote {OUTPUT_PATH}")

    shutil.copy2(OUTPUT_PATH, SERVER_DATA_PATH)
    print(f"Copied to {SERVER_DATA_PATH}")

    print(f"\nProcessed {total - failed}/{total} entries. {failed} failed.")


if __name__ == "__main__":
    main()
