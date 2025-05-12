
---

## سلام دانشجوهای عزیز دانشگاه قم! 👋

همون‌طور که خودتون بهتر می‌دونید، بخش تمدید کتاب‌های کتابخانه‌ی مرکزی واقعاً اذیت‌کننده‌ست.
تو گوشی که عملاً باز نمی‌شه، تو ویندوز هم وقتی باز بشه، باید هی کلیک کنی، هی دکمه به خودش نگیره، هی دوباره کلیک کنی، باز نگیره... خلاصه یه مصیبته! 😩

برای همین یه اسکریپت نوشتم که کل این کارو به‌صورت خودکار براتون انجام می‌ده.
نه اعصاب می‌خواد، نه وقت — فقط یه بار راهش بندازید، خودش همه‌ی کتاب‌هاتون رو تمدید می‌کنه ✌️

---

## ✨ چی کار می‌کنه؟

* به صورت خودکار وارد سایت کتابخانه می‌شه
* لیست کتاب‌هایی که امانت گرفتین رو می‌خونه
* هر کدوم که قابل تمدید باشن رو خودش تمدید می‌کنه
* لاگ همه‌ی این کارها رو هم توی فایل `library_extension.log` می‌نویسه

---

## ⚙️ چطوری استفاده کنم؟

### 1. اگه حوصله نصب پیش‌نیازها رو نداری، فقط فایل exe رو دانلود کن:

📥 [دانلود فایل exe](https://github.com/Matin-Talkhabi/qom-library-renewer/tree/main/exe)
فقط بخش `config.txt` داخل فایل رو ویرایش کن و اطلاعاتت رو وارد کن (کد عضویت و رمز عبور). بعد برنامه رو اجرا کن و خودش تمام کتاب‌ها رو تمدید می‌کنه.

### 2. اگر می‌خوای به صورت دستی اسکریپت رو اجرا کنی، این مراحل رو دنبال کن:

1. **اول Geckodriver رو دانلود کن:**
   📥 [دانلود Geckodriver از گیت‌هاب](https://github.com/mozilla/geckodriver/releases)
   📥 [همچنین می‌تونی نسخه‌ی مناسب رو از سایت PlatformBoy دریافت کنی (راحت‌تر)](https://platformboy.com/firefox-webdriver/)

   نسخه‌ای که با سیستم‌عاملت سازگاره رو بگیر (مثلاً ویندوز 64 بیت) و در همون پوشه‌ای که فایل `main.py` رو گذاشتی قرار بده.

2. **پیش‌نیازها رو نصب کن:**

   ```bash
   pip install -r requirements.txt
   ```

3. **یه فایل `config.txt` بساز و اطلاعاتت رو بذار توش:**

   ```txt
   member_code=کد عضویت شما
   password=رمز عبور شما
   ```

4. **فایل‌های زیر رو کنار هم بذار:**

   * `main.py`
   * `config.txt`
   * `geckodriver.exe`

5. **اجراش کن:**

   ```bash
   python main.py
   ```

---

## 📝 نکات مهم

* مطمئن شو فایروال یا آنتی‌ویروست مانع اجرای `geckodriver.exe` نباشه.
* این برنامه فقط برای سایت کتابخانه‌ی دانشگاه قم طراحی شده و ممکنه برای سایت‌های دیگه کار نکنه.
* اطلاعات ورود شما در فایل `config.txt` باقی می‌مونه، حواست باشه اونو توی جایی مثل GitHub آپلود نکنی.

---

## 🛠 توسعه و همکاری

خوشحال می‌شم اگر پیشنهاد بهتری داری، با من درمیون بذاری یا Pull Request بزنی.
همه‌مون درد تمدید کتاب رو کشیدیم، بیاید یه بار برای همیشه حلش کنیم 😁

---

**لایسنس:** MIT
پروژه آزاد برای استفاده و تغییر هست.

---

### Hello Qom University students! 👋

As you probably already know, the book renewal section of the university library website is... well, a pain.
On mobile, it barely opens. On Windows, if it opens at all, you have to keep clicking and clicking until maybe — just maybe — the button decides to work. 😩
Long story short: it’s a frustrating mess.

So, I wrote a simple script that does all the hard work for you — automatically!
No hassle, no stress. Just run it once and it renews all your borrowed books like magic ✌️

---

## ✨ What does it do?

* Automatically logs into the library system
* Reads your list of borrowed books
* Renews any books that are eligible for renewal
* Logs all these actions in a file called `library_extension.log`

---

## ⚙️ How to use it?

### 1. If you don't feel like setting things up, just download the exe file:

📥 [Download exe file](https://github.com/Matin-Talkhabi/qom-library-renewer/tree/main/exe)
Simply edit the `config.txt` file with your credentials (member code and password), then run the program, and it will renew all your books for you.

### 2. If you prefer to run the script manually, follow these steps:

1. **Download Geckodriver:**

   📥 [Download Geckodriver from GitHub](https://github.com/mozilla/geckodriver/releases)
   📥 [Or from PlatformBoy (easier)](https://platformboy.com/firefox-webdriver/)
   Get the version that matches your OS (e.g., Windows 64-bit), and put it in the same folder as `main.py`.

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `config.txt` file with your credentials:**

   ```txt
   member_code=your_member_code
   password=your_password
   ```

4. **Make sure you have the following files in one folder:**

   * `main.py`
   * `config.txt`
   * `geckodriver.exe`

5. **Run the script:**

   ```bash
   python main.py
   ```

---

## 📝 Important Notes

* Make sure your firewall or antivirus isn’t blocking `geckodriver.exe`
* This script is specifically designed for Qom University’s library system
* Your login info stays in `config.txt` — be careful not to upload that file to public places like GitHub

---

## 🛠 Want to help improve it?

Feel free to fork the repo, open issues, or send pull requests.
We’ve all suffered through renewing books — let’s fix it once and for all 😁

---

**License:** MIT
Free to use and modify.

---
