# راهنمای بات معاملاتی Ultra Max v2 (STB5)

## 🚀 شروع سریع

### 1. اجرای بات در حالت DRY-RUN (بدون معامله واقعی)
```bash
cd /home/asr/Desktop/stb
SYMBOL=XAUUSD LIVE_MODE=false ./scripts/start_trading_bot_daemon.sh
```

### 2. اجرای بات در حالت LIVE (معامله واقعی)
```bash
cd /home/asr/Desktop/stb
SYMBOL=XAUUSD LIVE_MODE=true ./scripts/start_trading_bot_daemon.sh
```

### 3. بررسی وضعیت بات
```bash
./scripts/check_trading_bot.sh
```

### 4. توقف بات
```bash
./scripts/stop_trading_bot.sh
```

---

## 📋 دستورات مفید

### مشاهده لاگ زنده
```bash
tail -f logs/mt5_auto_trader_daemon.log
```

### بررسی PID و وضعیت
```bash
cat models/locks/trading_bot.pid
ps -p $(cat models/locks/trading_bot.pid)
```

### توقف اضطراری (kill switch)
```bash
touch models/STOP_TRADING
```

### حذف kill switch (برای شروع مجدد)
```bash
rm models/STOP_TRADING
```

---

## ⚙️ تنظیمات

### متغیرهای محیطی

- `SYMBOL`: نماد معاملاتی (پیش‌فرض: `XAUUSD`)
- `CONFIG`: فایل کانفیگ (پیش‌فرض: `config/settings.hybrid.tuned.yaml`)
- `TIMEFRAME`: تایم‌فریم (پیش‌فرض: `M1`)
- `POLL_SECONDS`: فاصله بررسی سیگنال (پیش‌فرض: `2.0`)
- `MAX_POSITIONS`: حداکثر تعداد پوزیشن همزمان (پیش‌فرض: `1`)
- `VOLUME`: حجم معامله (پیش‌فرض: `0.01`)
- `LIVE_MODE`: حالت live (`true`/`false`)

### مثال: اجرا با تنظیمات سفارشی
```bash
SYMBOL=XAGUSD TIMEFRAME=M5 POLL_SECONDS=5.0 MAX_POSITIONS=2 \
  ./scripts/start_trading_bot_daemon.sh
```

---

## 🔄 چرخه دائمی

بات به صورت خودکار:
1. ✅ به متاتریدر متصل می‌شود
2. ✅ داده‌های بازار را دریافت می‌کند
3. ✅ سیگنال‌های مدل را تولید می‌کند
4. ✅ در صورت نیاز، معامله انجام می‌دهد
5. ✅ از معاملات بسته شده یاد می‌گیرد (BlindSpot Filter)
6. ✅ در صورت crash، دوباره restart می‌شود

### ویژگی‌های چرخه دائمی:

- **Auto-restart**: در صورت crash، بات دوباره شروع می‌شود
- **Watchdog**: نظارت بر سلامت ارتباط با MT5
- **Kill Switch**: امکان توقف ایمن با فایل `STOP_TRADING`
- **Instance Lock**: جلوگیری از اجرای همزمان چندین instance
- **Online Learning**: یادگیری خودکار از معاملات واقعی

---

## 📊 نظارت و مانیتورینگ

### بررسی وضعیت اتصال MT5
```bash
./scripts/check_trading_bot.sh
```

خروجی شامل:
- وضعیت پروسه (در حال اجرا/متوقف)
- وضعیت فایل‌های IPC (stb_command.txt, stb_response.txt, stb_market.txt)
- آخرین لاگ‌ها

### بررسی لاگ‌ها
```bash
# آخرین 50 خط
tail -n 50 logs/mt5_auto_trader_daemon.log

# جستجو در لاگ
grep "ERROR\|WARNING\|SUCCESS" logs/mt5_auto_trader_daemon.log

# فیلتر سیگنال‌ها
grep "Signal\|Trade\|Position" logs/mt5_auto_trader_daemon.log
```

---

## 🛡️ ایمنی

### قبل از اجرای LIVE:

1. ✅ مطمئن شوید که `PythonBridge.mq5` در متاتریدر کامپایل و فعال است
2. ✅ اتصال به متاتریدر را تست کنید
3. ✅ در حالت DRY-RUN تست کنید
4. ✅ حجم معامله را بررسی کنید (`--volume`)
5. ✅ حداکثر تعداد پوزیشن را تنظیم کنید (`--max-positions`)

### Kill Switch

برای توقف فوری بات:
```bash
touch models/STOP_TRADING
```

بات در چرخه بعدی متوقف می‌شود (graceful shutdown).

---

## 🔧 عیب‌یابی

### مشکل: بات اجرا نمی‌شود

1. بررسی کنید که فایل `STOP_TRADING` وجود ندارد:
   ```bash
   rm models/STOP_TRADING
   ```

2. بررسی کنید که instance قبلی متوقف شده:
   ```bash
   ./scripts/stop_trading_bot.sh
   ```

3. بررسی لاگ‌ها برای خطا:
   ```bash
   tail -n 100 logs/mt5_auto_trader_daemon.log
   ```

### مشکل: اتصال به MT5 برقرار نمی‌شود

1. بررسی کنید که `PythonBridge.mq5` در متاتریدر فعال است
2. بررسی مسیر فایل‌های IPC:
   ```bash
   ls -la ~/.wine/drive_c/Users/$USER/AppData/Roaming/MetaQuotes/Terminal/*/MQL5/Files/stb_*
   ```

3. بررسی لاگ‌های MT5 در متاتریدر

### مشکل: بات crash می‌کند

1. بررسی لاگ برای خطا:
   ```bash
   tail -n 200 logs/mt5_auto_trader_daemon.log | grep -i error
   ```

2. بررسی مدل‌ها:
   ```bash
   ls -lh models/*.joblib models/*/*.pt
   ```

3. بررسی داده‌ها:
   ```bash
   ls -lh data/raw/*.csv
   ```

---

## 📝 یادداشت‌ها

- بات به صورت دائمی در background اجرا می‌شود
- لاگ‌ها در `logs/mt5_auto_trader_daemon.log` ذخیره می‌شوند
- PID در `models/locks/trading_bot.pid` ذخیره می‌شود
- برای توقف، از `./scripts/stop_trading_bot.sh` استفاده کنید
- برای مشاهده وضعیت، از `./scripts/check_trading_bot.sh` استفاده کنید

---

## 🎯 خلاصه دستورات

```bash
# شروع (DRY-RUN)
SYMBOL=XAUUSD LIVE_MODE=false ./scripts/start_trading_bot_daemon.sh

# شروع (LIVE)
SYMBOL=XAUUSD LIVE_MODE=true ./scripts/start_trading_bot_daemon.sh

# بررسی وضعیت
./scripts/check_trading_bot.sh

# توقف
./scripts/stop_trading_bot.sh

# مشاهده لاگ
tail -f logs/mt5_auto_trader_daemon.log
```

