# راهنمای رفع مشکل وای‌فای

## وضعیت فعلی
- ✅ درایور `ath12k` بارگذاری شده است
- ✅ Firmware وای‌فای نصب است (`linux-firmware`)
- ✅ رادیو وای‌فای فعال است
- ❌ دستگاه وای‌فای در PCI شناسایی نمی‌شود
- ❌ اینترفیس `wlp8s0` وجود ندارد

## مشکل شناسایی شده
بر اساس لاگ‌های سیستم، وای‌فای قبلاً کار می‌کرده (`wlp8s0` به شبکه `ali-5G` متصل بوده)، اما اکنون دستگاه در سطح سخت‌افزاری شناسایی نمی‌شود.

## راه‌حل‌های پیشنهادی

### 1. بررسی و فعال‌سازی وای‌فای در BIOS (اولویت اول)

مادربرد شما: **MSI X870 GAMING PLUS WIFI**

1. سیستم را ریستارت کنید
2. هنگام بوت، کلید `Delete` یا `F2` را فشار دهید تا وارد BIOS شوید
3. به بخش **Advanced** یا **Integrated Peripherals** بروید
4. گزینه **WiFi** یا **Wireless LAN** را پیدا کنید
5. آن را **Enabled** کنید
6. تغییرات را ذخیره کنید و خارج شوید (F10)

### 2. بررسی اتصال فیزیکی (در صورت وجود کارت وای‌فای جداگانه)

اگر کارت وای‌فای جداگانه دارید:
- اطمینان حاصل کنید که کارت به درستی در اسلات PCIe قرار گرفته است
- کارت را خارج و دوباره نصب کنید

### 3. بررسی ماژول‌های کرنل

```bash
# بررسی ماژول‌های بارگذاری شده
lsmod | grep ath12k

# بارگذاری مجدد ماژول
sudo modprobe -r ath12k
sudo modprobe ath12k

# بررسی پیام‌های کرنل
sudo dmesg | grep -i ath12k
```

### 4. بررسی PCI Devices

```bash
# بررسی دستگاه‌های PCI
lspci -nn | grep -i "network\|wireless\|wifi"

# بررسی کامل PCI
lspci -v | grep -A 10 -i "wireless\|wifi"
```

### 5. بررسی ACPI و Power Management

```bash
# بررسی وضعیت ACPI
sudo dmesg | grep -i acpi | grep -i wifi

# غیرفعال‌سازی power saving برای وای‌فای (اگر دستگاه پیدا شد)
sudo iwconfig wlp8s0 power off
```

### 6. نصب/به‌روزرسانی Firmware

```bash
# به‌روزرسانی firmware
sudo apt update
sudo apt install --reinstall linux-firmware

# بررسی فایل‌های firmware
ls -la /lib/firmware/ath12k/
```

### 7. بررسی Kernel Parameters

اگر وای‌فای در BIOS فعال است اما هنوز کار نمی‌کند، ممکن است نیاز به پارامترهای کرنل باشد:

```bash
# بررسی پارامترهای فعلی کرنل
cat /proc/cmdline

# در صورت نیاز، می‌توانید پارامترهای زیر را به GRUB اضافه کنید:
# acpi=on pcie_aspm=off
```

### 8. استفاده از اسکریپت رفع مشکل

اسکریپت خودکار برای بررسی و رفع مشکلات:

```bash
sudo /home/asr/Desktop/stb/scripts/fix_wifi.sh
```

## بررسی نهایی

پس از اعمال تغییرات:

```bash
# بررسی دستگاه‌های شبکه
nmcli device status

# بررسی اینترفیس‌های شبکه
ip link show

# بررسی PCI devices
lspci | grep -i network

# بررسی ماژول‌های وای‌فای
lsmod | grep ath12k
```

## لاگ‌های مفید برای دیباگ

```bash
# لاگ‌های NetworkManager
journalctl -u NetworkManager --no-pager | grep -i wifi | tail -20

# لاگ‌های کرنل
sudo dmesg | grep -i "ath12k\|wifi\|wlan" | tail -30

# لاگ‌های سیستم
sudo journalctl --no-pager | grep -i "wifi\|wlan\|wireless" | tail -30
```

## نکات مهم

1. **اولویت اول**: بررسی BIOS - در 90% موارد مشکل از اینجا است
2. اگر وای‌فای در BIOS فعال است اما کار نمی‌کند، ممکن است نیاز به به‌روزرسانی BIOS باشد
3. برخی مادربردها نیاز به نصب آنتن‌های وای‌فای دارند - بررسی کنید که آنتن‌ها به درستی وصل شده‌اند
4. در صورت عدم موفقیت، می‌توانید از USB WiFi Adapter استفاده کنید

## پشتیبانی

اگر مشکل حل نشد، اطلاعات زیر را جمع‌آوری کنید:

```bash
# اطلاعات سیستم
uname -a
lspci -nn
lsusb
sudo dmesg > wifi_dmesg.log
journalctl -u NetworkManager > wifi_nm.log
```



