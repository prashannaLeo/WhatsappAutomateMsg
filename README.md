# WhatsApp Bulk Messenger

A Python automation tool that sends WhatsApp messages, images, and videos to multiple contacts using Selenium WebDriver. It leverages your existing Chrome profile to stay logged into WhatsApp Web and includes built-in logging, duplicate prevention, and failure tracking.

---

## ⚠️ Disclaimer

This tool is intended for **educational and personal use only**. Automated messaging on WhatsApp may violate their [Terms of Service](https://www.whatsapp.com/legal/terms-of-service). Excessive or unsolicited automated messaging can get your number flagged or banned. Use responsibly, on your own contacts, and at your own risk. The authors are not responsible for any account bans, data loss, or misuse.

---

## ✨ Features

- 📱 Send text messages to multiple contacts
- 🖼️ Send images with captions
- 🎥 Send videos with captions
- 🔐 Uses your existing Chrome profile — no repeated QR scans
- 📝 Logs all sent messages to `sent_messages_log.csv`
- ❌ Logs failed attempts to `failed_contacts_<timestamp>.csv`
- 🔁 Prevents duplicate sends (skips contacts already logged as sent)
- 📄 Supports contacts loaded from a CSV file or a hardcoded list
- ⏱️ Configurable wait times to handle slow page loads or large media files

---

## 📋 Prerequisites

- **Python 3.8+**
- **Google Chrome** installed
- A **WhatsApp account** linked to WhatsApp Web
- **Chrome profile** with an active WhatsApp Web session (optional, but avoids scanning the QR code every run)

---

## 🚀 Installation

1. **Clone or download** this project.

2. **(Optional) Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### `requirements.txt`

```
attrs==25.3.0
certifi==2025.1.31
cffi==1.17.1
charset-normalizer==3.4.1
colorama==0.4.6
decorator==5.2.1
h11==0.14.0
idna==3.10
outcome==1.3.0.post0
packaging==24.2
pillow==10.4.0
proglog==0.1.10
pycparser==2.22
PySocks==1.7.1
python-dotenv==1.0.1
requests==2.32.3
selenium==4.29.0
sniffio==1.3.1
sortedcontainers==2.4.0
tqdm==4.67.1
trio==0.29.0
trio-websocket==0.12.2
typing_extensions==4.12.2
urllib3==2.3.0
webdriver-manager==4.0.2
websocket-client==1.8.0
wsproto==1.2.0
```

#### Key package roles

| Package | Purpose |
|---|---|
| `selenium` | Core browser automation — drives Chrome, locates elements, sends input |
| `webdriver-manager` | Automatically downloads and manages the correct ChromeDriver version |
| `python-dotenv` | Loads configuration/environment variables from a `.env` file (optional) |
| `requests` | HTTP requests, used by dependency chains and available for custom extensions |
| `pillow` | Image handling/validation (useful if you extend media pre-processing) |
| `proglog` | Progress logging, useful if media processing is extended (e.g., with `moviepy`) |
| `trio`, `trio-websocket`, `sniffio`, `outcome`, `wsproto` | Async/networking support pulled in by Selenium's WebSocket-based browser protocol (BiDi) |
| `cffi`, `pycparser` | Native bindings used by lower-level networking/crypto packages |
| `PySocks` | SOCKS proxy support for `requests`/`urllib3` |
| `colorama` | Cross-platform colored terminal output (mainly relevant on Windows) |
| `certifi`, `charset-normalizer`, `idna`, `urllib3` | Core HTTP/SSL support used by `requests` and `webdriver-manager` |
| `attrs`, `sortedcontainers`, `typing_extensions`, `packaging`, `decorator`, `tqdm`, `websocket-client` | Supporting utility libraries required by Selenium, Trio, and related tooling |

> These versions are pinned for reproducibility. If you hit a Selenium/Chrome compatibility issue, try updating `selenium` and `webdriver-manager` to their latest releases.

---

## ⚙️ Configuration

Before running, edit the script (`import_csv.py`) to match your environment.

### 1. Chrome Profile Path

Update the `--user-data-dir` and `--profile-directory` arguments with your own paths so the script reuses your logged-in WhatsApp Web session:

**Windows:**
```python
chrome_options.add_argument("--user-data-dir=C:\\Users\\<YourName>\\AppData\\Local\\Google\\Chrome\\User Data")
chrome_options.add_argument("--profile-directory=Default")
```

**Linux:**
```python
chrome_options.add_argument("--user-data-dir=/home/<username>/.config/google-chrome")
chrome_options.add_argument("--profile-directory=Default")
```

**macOS:**
```python
chrome_options.add_argument("--user-data-dir=/Users/<username>/Library/Application Support/Google/Chrome")
chrome_options.add_argument("--profile-directory=Default")
```

> 💡 **Tip:** To find your profile name, open `chrome://version` in Chrome and check the **Profile Path** field. If you use multiple Chrome profiles, it may be `Profile 1`, `Profile 2`, etc., instead of `Default`.

### 2. Contacts

**Option A — Hardcoded list:**
```python
contacts = [
    "+9779842724655",
    "+1234567890",
]
```

**Option B — CSV file (`contacts.csv`):**
```csv
Phone Number
+9779842724655
+1234567890
```

The script prompts you at startup to choose between the two:
```
Do you want to use a CSV file for contacts? (yes/no):
```

> **Note:** Phone numbers must include the country code with a leading `+` (e.g., `+977` for Nepal, `+1` for the US/Canada).

### 3. Message & Media

```python
message = "Hello! This is an automated message."
image_path = "C:/path/to/image.jpg"
video_path = "C:/path/to/video.mp4"
image_caption_message = "Image caption here"
video_caption_message = "Video caption here"
```

If a media path doesn't exist on disk, that step is skipped automatically and logged to the console — the script won't crash.

---

## ▶️ Usage

```bash
python import_csv.py
```

### Workflow

1. Chrome opens using your existing profile and navigates to WhatsApp Web.
2. If WhatsApp Web isn't already open in a tab, the script opens a new one.
3. You'll be prompted to scan the QR code (skip this if your profile is already logged in):
   ```
   Press Enter after scanning QR Code and logging in:
   ```
4. Choose your contact source:
   ```
   Do you want to use a CSV file for contacts? (yes/no):
   ```
5. The script loops through each contact and sends, in order:
   - Text message
   - Image (if the path exists)
   - Video (if the path exists)
6. Results are logged as each send completes.
7. The browser closes automatically once all contacts are processed.

---

## 📁 Output Files

| File | Description |
|---|---|
| `sent_messages_log.csv` | Every successful message/media send, used to prevent duplicate sends |
| `failed_contacts_<timestamp>.csv` | Contacts that failed during this run, with a timestamp |

**`sent_messages_log.csv` format:**
```csv
Phone Number,Message,Timestamp
+9779842724655,Hello!,2025-01-15 10:23:45
```

**Failed contacts format:**
```csv
Phone Number,Timestamp
+9779842724655,2025-01-15 10:24:12
```

---

## 🧠 How It Works

1. **WebDriver Init** — Launches Chrome with your user profile directory so cookies and session data persist between runs, avoiding repeated logins.
2. **WhatsApp Web Detection** — Scans all open browser tabs for `web.whatsapp.com`; opens a new tab only if none is found.
3. **Send Text** — Navigates directly to a chat via a pre-filled URL (`/send?phone=...&text=...`), waits for the message box to load, types the message, and clicks **Send**.
4. **Send Media** — Opens the chat, clicks the attachment (`+`) button, injects the local file path into the hidden `<input type="file">` element, waits for the upload preview, adds a caption, and clicks **Send**.
5. **Logging & Deduplication** — Before sending anything, checks `sent_messages_log.csv` for a matching phone number + message/file pair; after a successful send, appends a new row so reruns don't resend the same content.

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| `SessionNotCreatedException` | Update Chrome and let `webdriver-manager` fetch a matching ChromeDriver automatically. |
| QR code doesn't load | Close all running Chrome instances (including background processes), then rerun the script. |
| `Element not found` / `TimeoutException` | WhatsApp Web's UI changes periodically — inspect the page and update the relevant XPaths. |
| Messages not sending | Your account may be temporarily rate-limited or flagged by WhatsApp — pause and retry later. |
| Send button not clickable | Increase the `WebDriverWait` timeout values (e.g., from 20–30s to 45–60s). |
| Large media uploads time out | Increase the `time.sleep(10)` delay after `file_input.send_keys(file_path)` to allow more upload time. |

Add or increase delays if you hit rate limits:
```python
time.sleep(10)  # Increase from 5s if needed
```

---

## ⚡ Tips for Responsible Use

- Keep contact lists small — WhatsApp actively monitors for bulk/automated sending patterns.
- Add randomized delays between sends, e.g. `time.sleep(random.uniform(15, 45))`, instead of a fixed interval.
- Avoid running multiple instances of the script simultaneously on the same account.
- Only message people who expect to hear from you — don't use this for unsolicited bulk outreach or spam.
- Monitor `failed_contacts_*.csv` for signs your account may be getting rate-limited, and stop if failures spike.

---

## 🧩 Customization Ideas

- Load per-contact messages/captions from a CSV for personalization.
- Add retry logic for failed contacts using `failed_contacts_*.csv` as input for a second pass.
- Store configuration (Chrome profile path, message text, delays) in a `.env` file via `python-dotenv` instead of hardcoding it.
- Switch to Playwright for faster, more modern browser automation.
- Add structured logging (e.g., Python's `logging` module) alongside the CSV logs.

---

## 📜 License

This project is provided as-is for educational purposes. No warranty is provided. Use at your own discretion.

---

## 🙌 Acknowledgments

- [Selenium](https://www.selenium.dev/)
- [webdriver-manager](https://pypi.org/project/webdriver-manager/)
- WhatsApp Web

Happy (responsible) messaging! 🎉
