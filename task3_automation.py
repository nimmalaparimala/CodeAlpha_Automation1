# ============================================================
#  CodeAlpha — Task 3: Task Automation with Python Scripts
#  Includes ALL three automation ideas:
#    A) Move .jpg files to a new folder
#    B) Extract email addresses from a .txt file
#    C) Scrape the title of a webpage and save it
#  Author : Your Name
#  Repo   : github.com/YourUsername/CodeAlpha_TaskAutomation
# ============================================================

import os
import re
import shutil

# ── Optional imports (used only if the user picks option C) ──
try:
    import urllib.request as _urllib
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# ════════════════════════════════════════════════════════════
#  A) Move all .jpg files from a folder to a new folder
# ════════════════════════════════════════════════════════════

def move_jpg_files(source_folder: str, dest_folder: str) -> None:
    """Move every .jpg / .jpeg file from source_folder into dest_folder."""
    if not os.path.isdir(source_folder):
        print(f"  ⚠  Source folder '{source_folder}' does not exist.")
        return

    os.makedirs(dest_folder, exist_ok=True)
    moved = 0

    for filename in os.listdir(source_folder):
        if filename.lower().endswith((".jpg", ".jpeg")):
            src = os.path.join(source_folder, filename)
            dst = os.path.join(dest_folder, filename)
            # Avoid overwrite conflicts
            if os.path.exists(dst):
                base, ext = os.path.splitext(filename)
                dst = os.path.join(dest_folder, f"{base}_copy{ext}")
            shutil.move(src, dst)
            print(f"  ✅ Moved: {filename}")
            moved += 1

    if moved == 0:
        print("  ℹ  No .jpg files found in the source folder.")
    else:
        print(f"\n  🎉 Done! {moved} file(s) moved to '{dest_folder}'.")


# ════════════════════════════════════════════════════════════
#  B) Extract all email addresses from a .txt file
# ════════════════════════════════════════════════════════════

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")


def extract_emails(input_file: str, output_file: str) -> None:
    """Read input_file, find all e-mail addresses, write unique ones to output_file."""
    if not os.path.isfile(input_file):
        print(f"  ⚠  File '{input_file}' not found.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    emails = sorted(set(EMAIL_REGEX.findall(content)))

    if not emails:
        print("  ℹ  No email addresses found in the file.")
        return

    with open(output_file, "w", encoding="utf-8") as f:
        for email in emails:
            f.write(email + "\n")

    print(f"  ✅ Found {len(emails)} unique email(s).")
    for email in emails:
        print(f"     • {email}")
    print(f"\n  💾 Saved to '{output_file}'.")


# ════════════════════════════════════════════════════════════
#  C) Scrape the title of a webpage and save it
# ════════════════════════════════════════════════════════════

TITLE_REGEX = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def fetch_page_title(url: str, output_file: str) -> None:
    """Download the HTML at url, extract the <title>, and save it."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print(f"  🌐 Fetching: {url}")
    try:
        req = _urllib.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with _urllib.urlopen(req, timeout=10) as response:
            html = response.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ⚠  Could not fetch page: {e}")
        return

    match = TITLE_REGEX.search(html)
    if not match:
        print("  ⚠  No <title> tag found on the page.")
        return

    title = re.sub(r"\s+", " ", match.group(1)).strip()
    print(f"  📌 Title: {title}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"URL   : {url}\n")
        f.write(f"Title : {title}\n")

    print(f"  💾 Saved to '{output_file}'.")


# ════════════════════════════════════════════════════════════
#  Main menu
# ════════════════════════════════════════════════════════════

def main() -> None:
    print("\n" + "=" * 50)
    print("   🤖 CodeAlpha — Task Automation Scripts")
    print("=" * 50)
    print("  Choose an automation task:")
    print("  [A] Move .jpg files to a new folder")
    print("  [B] Extract emails from a .txt file")
    print("  [C] Scrape webpage title and save it")
    print("  [Q] Quit")
    print()

    choice = input("  Your choice (A / B / C / Q): ").strip().upper()

    if choice == "A":
        src = input("  Source folder path: ").strip()
        dst = input("  Destination folder path (will be created if needed): ").strip()
        move_jpg_files(src, dst)

    elif choice == "B":
        inp = input("  Input .txt file path: ").strip()
        out = input("  Output file path [emails_found.txt]: ").strip() or "emails_found.txt"
        extract_emails(inp, out)

    elif choice == "C":
        url = input("  URL (e.g. https://www.python.org): ").strip()
        out = input("  Output file path [page_title.txt]: ").strip() or "page_title.txt"
        fetch_page_title(url, out)

    elif choice == "Q":
        print("  Goodbye! 👋")
    else:
        print("  ⚠  Invalid choice.")

    print()


if __name__ == "__main__":
    main()
