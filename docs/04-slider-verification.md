# Slider Captcha Login

Example: `examples/sldier_verification/`

Some login pages show a **slider captcha** after you click login: drag a puzzle piece to the gap in the background image. This example automates that flow with **Selenium + OpenCV**.

Target site: [pickmall login](https://pc-b2b2c.pickmall.cn/login)

---

## Dependencies

```bash
pip install selenium opencv-python
```

Chrome browser + matching ChromeDriver must be installed.

Run:

```bash
cd examples/sldier_verification
python slider.py
```

---

## Overall flow

```
1. Selenium opens login page, enters username/password, clicks login
2. Slider captcha appears
3. Grab background image + puzzle piece (base64 from <img src>)
4. OpenCV finds where the piece fits → drag distance (pixels)
5. Selenium drags the slider by that distance
6. Check if login succeeded
```

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  slider.py  │ ──► │  s_login.py  │ ──► │ drag slider │
│  (Selenium) │     │  (OpenCV)    │     │  (Selenium) │
└─────────────┘     └──────────────┘     └─────────────┘
   login + screenshot    calc distance       ActionChains
```

---

## slider.py — browser automation

| Step | What it does |
|------|----------------|
| Open page | `webdriver.Chrome()` → login URL |
| Fill form | username, password , click login |
| Get images | `img[1]` = background, `img[2]` = puzzle piece; `src` is base64 |
| Save files | decode → `pic.png`, `pic2.png` |
| Calc distance | `match('pic.png', 'pic2.png')` |
| Drag | `ActionChains`: click slider → `move_by_offset(distance)` → release |
| Verify | check page text for welcome message |

Key code:

```python
lk = base64.b64decode(s.split(",")[1])   # strip "data:image/png;base64,"
with open("pic2.png", "wb") as f:
    f.write(lk2)                           # background → pic.png, piece → pic2.png

ActionChains(driver).click_and_hold(slider).perform()
ActionChains(driver).move_by_offset(xoffset=distance, yoffset=0).perform()
ActionChains(driver).release().perform()
```

---

## scripts/s_login.py — find the gap

**Goal:** return how many pixels to drag the slider horizontally.

### 1. Preprocess (`handle_img`)

Convert both images to **edge maps** so matching compares shapes, not colors:

```
color image → grayscale → Gaussian blur → Canny edges
```

### 2. Template match (`match`)

- **Large image** (`pic.png`) = background with a gap  
- **Small image** (`pic2.png`) = puzzle piece  

`cv2.matchTemplate` slides the small image over every **integer pixel position** on the large image and scores similarity (`TM_CCOEFF_NORMED`).

The position with the **highest score** is where the piece belongs:

```python
res = cv2.matchTemplate(bg_edges, piece_edges, cv2.TM_CCOEFF_NORMED)
_, _, _, max_loc = cv2.minMaxLoc(res)
return max_loc[0]   # x offset = drag distance
```

Example: if the best match is at x = 120, drag the slider **120 pixels** to the right.

---

## Project layout

```
sldier_verification/
├── slider.py           # Selenium: login, capture, drag
├── scripts/
│   └── s_login.py      # OpenCV: compute drag distance
├── pic.png             # generated: background (debug)
└── pic2.png            # generated: puzzle piece (debug)
```

---

## Notes

- **Selenium** handles pages that need clicks and JS; **OpenCV** solves “where is the gap” — each tool does one job.
- Real captchas may add noise, rotation, or rate limits; this demo targets a fixed training site.
