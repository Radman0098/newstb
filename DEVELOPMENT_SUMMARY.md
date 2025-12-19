# خلاصه پیشرفت سیستم Ultra Max v2 - از STB1 تا STB فعلی

## 📊 آمار کلی سیستم

- **تعداد فایل‌های Python**: 51 فایل در `src/` + 21 اسکریپت
- **تعداد مدل‌های ذخیره‌شده**: 71+ مدل (XGBoost, LSTM, PatchTST, BlindSpot)
- **نسخه فعلی**: Ultra Max v2.1.0
- **وضعیت**: ✅ آماده برای معامله‌گری زنده

---

## 🚀 پیشرفت‌های کلیدی از STB1 تا الان

### 1️⃣ **STB1 - نسخه پایه**
- ✅ استخراج ویژگی‌های Atomic و Sequential
- ✅ مدل XGBoost با K-Means برای Market State
- ✅ LSTM پایه (بدون Attention)
- ✅ Backtesting ساده
- ✅ Meta-Labeling اولیه

### 2️⃣ **STB2 - بهبودهای معماری**
- ✅ LSTM با Attention Mechanism
- ✅ HMM (Hidden Markov Model) برای Market State Encoding
- ✅ بهبود Feature Engineering
- ✅ بهینه‌سازی Backtesting

### 3️⃣ **STB3 - افزودن تکنولوژی‌های پیشرفته**
- ✅ RL Exit Agent (Double DQN)
- ✅ PatchTST (Transformer-based Time Series)
- ✅ Online Learning (یادگیری تدریجی)
- ✅ CatBoost و LightGBM (Multi-Boosting Ensemble)
- ✅ Graph Topology Features

### 4️⃣ **STB5 - سیستم کامل و Production-Ready (نسخه فعلی)**

#### 🎯 **بهینه‌سازی سخت‌افزار**
- ✅ `STB_MAX_HW=1` برای حداکثر استفاده از GPU/CPU
- ✅ بهینه‌سازی CUDA و PyTorch (TF32, cudnn.benchmark)
- ✅ DataLoader بهینه برای LSTM (zero-copy, pin_memory)
- ✅ Auto-batching برای PatchTST (جلوگیری از OOM)
- ✅ Mixed Precision Training (AMP)
- ✅ XGBoost روی GPU با Fallback به CPU

#### 🧠 **یادگیری از شکست‌ها (Learning from Failures)**
- ✅ `BlindSpotFilter` - فیلتر یادگیری از معاملات ناموفق
- ✅ Replay Buffer برای ذخیره معاملات
- ✅ Auto-training از Trade Logs
- ✅ Integration با Live Trading

#### 🔌 **اتصال به MetaTrader 5**
- ✅ `PythonBridge.mq5` - Expert Advisor برای ارتباط
- ✅ `MT5Bridge` - Python-side communication
- ✅ دستورات: `GET_HISTORY`, `GET_CURRENT_PRICE`, `EXECUTE_TRADE`, `CLOSE_POSITION`, `GET_POSITIONS`, `GET_ACCOUNT`, `GET_SYMBOL_INFO`, `MODIFY`
- ✅ `cmd_id` برای correlation و atomic operations
- ✅ Logging معاملات به `stb_trade_events.csv`

#### 🤖 **معامله‌گری خودکار (Live Trading)**
- ✅ `mt5_auto_trader.py` - اسکریپت معامله‌گری زنده
- ✅ Dynamic Position Sizing بر اساس Equity و Confidence
- ✅ Dynamic SL/TP بر اساس ATR و Broker Rules
- ✅ `max_stop_pct` برای محدود کردن فاصله SL/TP
- ✅ `max_hold_bars` برای بستن خودکار معاملات قدیمی
- ✅ Instance Locking (جلوگیری از اجرای همزمان)
- ✅ Kill-Switch برای توقف اضطراری
- ✅ Reverse Logic برای حساب‌های Hedging
- ✅ Auto-modify برای تنظیم SL/TP معاملات باز

#### 🔍 **بهبودهای مدل**
- ✅ تشخیص و رفع مدل‌های PatchTST خراب (NaN/Inf)
- ✅ Feature Selection بر اساس Importance
- ✅ Conformal Prediction برای Calibration
- ✅ Isotonic Calibration
- ✅ Walk-Forward Optimization

#### 🛡️ **سخت‌افزاری و امنیت**
- ✅ Code Audit با `py_compile` و `pytest`
- ✅ Error Handling جامع
- ✅ Retry Logic برای MT5 Communication
- ✅ Validation برای SL/TP (بر اساس Broker Rules)

---

## 📈 نتایج ارزیابی فعلی

### آخرین نتایج Backtest (XAUUSD):
```
Total Trades: 670
Win Rate: 81.64%
Return %: 32.94%
Max DD %: 4.04%
Profit Factor: 31.84
Sharpe Ratio: 15.44
```

### وضعیت PatchTST:
```
patchtst_conf: mean=0.638, p95=0.741, max=0.749
>0 signals: 19919/19979 (99.7%)
```

### وضعیت Hybrid Signals:
```
pre-meta signals nonzero: 9698/19979
conf>0: 19960/19979
conf q50=0.369, q90=0.847, q95=0.856, q99=0.864
```

---

## 🏗️ معماری سیستم

### **Feature Extraction (345 ویژگی)**
- ✅ Atomic Features (Statistical)
- ✅ Sequential Features (Time-based)
- ✅ Topological Features (Persistent Homology)
- ✅ Graph Topology Features
- ✅ Pattern Mining
- ✅ Microstructure Features
- ✅ Technical Patterns
- ✅ Multi-Timeframe (MTF) Features
- ✅ Feature Interactions
- ✅ Wavelet Features

### **Market State Encoding**
- ✅ HMM (Hidden Markov Model) - 4 Regimes
- ✅ OOD (Out-Of-Distribution) Detection
- ✅ Regime-based Model Training

### **Model Ensemble**
- ✅ XGBoost (Deep Ensemble, Per-Regime)
- ✅ LSTM (با Attention Mechanism)
- ✅ PatchTST (Transformer-based)
- ✅ CatBoost (Optional)
- ✅ LightGBM (Optional)
- ✅ Meta-Labeling (Second-layer Filtering)
- ✅ BlindSpotFilter (Learning from Failures)

### **Signal Generation**
- ✅ Hybrid Mode: Consensus Voting (2of3 یا 3of3)
- ✅ Confidence Aggregation (mean/max)
- ✅ Threshold-based Filtering
- ✅ BlindSpot Penalization

### **Risk Management**
- ✅ Dynamic Position Sizing
- ✅ Dynamic SL/TP (ATR-based)
- ✅ Max Stop Percentage
- ✅ Time-based Exit (max_hold_bars)
- ✅ Max Drawdown Stop
- ✅ Risk per Trade

---

## 📁 ساختار فایل‌ها

```
stb/
├── src/
│   ├── data/          # Data loading
│   ├── features/      # Feature extraction (13 module)
│   ├── models/        # ML models (10 module)
│   ├── strategies/    # Trading strategies
│   ├── execution/     # Order management (MT5 Bridge, RL Exit)
│   ├── backtest/      # Backtesting engine
│   ├── analysis/      # Analysis tools
│   ├── services/      # Services (Failure Analysis)
│   └── utils/         # Utilities
├── scripts/           # 21 اسکریپت (Training, Optimization, Live Trading)
├── mql5/              # MetaTrader 5 Expert Advisor
├── models/            # 71+ مدل ذخیره‌شده
├── config/            # Configuration files
└── versions/          # نسخه‌های قبلی (stb1, stb2, stb3)
```

---

## 🔧 تنظیمات فعلی (`settings.hybrid.tuned.yaml`)

### Strategy:
- `signal_mode: hybrid` (XGBoost + LSTM + PatchTST)
- `consensus: 2of3`
- `confidence_threshold: 0.35`
- `risk_per_trade: 0.01`
- `max_dd_stop_pct: 35.0`

### BlindSpot:
- `auto_train: true`
- `min_trades: 300`
- `max_replay: 50000`
- `p_loss_block: 0.65`
- `surprise_block: 0.55`

### Hybrid Models:
- `use_lstm: 1`
- `use_patchtst: 1`
- `lstm_conf_thr: 0.45`
- `patchtst_conf_thr: 0.59`

---

## ✅ چک‌لیست آماده‌سازی Production

- ✅ تمام مدل‌ها آموزش دیده و ذخیره شده
- ✅ PatchTST فعال و در حال کار
- ✅ BlindSpotFilter فعال و یادگیری از شکست‌ها
- ✅ MT5 Bridge کامپایل و در حال اجرا
- ✅ Live Trading Script آماده (`mt5_auto_trader.py`)
- ✅ Dynamic SL/TP و Position Sizing
- ✅ Time-based Exit (max_hold_bars)
- ✅ Instance Locking و Kill-Switch
- ✅ Error Handling و Retry Logic
- ✅ Logging جامع

---

## 🎯 مراحل بعدی (پیشنهادی)

1. **بهینه‌سازی بیشتر**:
   - Fine-tuning Hyperparameters
   - Walk-Forward Optimization روی داده‌های جدید
   - Portfolio Optimization (Multi-Symbol)

2. **مانیتورینگ**:
   - Dashboard برای Live Trading
   - Alert System برای خطاها
   - Performance Tracking

3. **بهبود مدل**:
   - Continual Learning از Live Trades
   - A/B Testing برای Strategies
   - Ensemble Weight Optimization

---

## 📝 یادداشت‌های مهم

- سیستم بر اساس **استانداردهای صنعتی-نظامی** طراحی شده است
- معماری **Modular** برای قابلیت توسعه
- تمام محاسبات **بهینه‌سازی** شده (zero-copy, GPU acceleration)
- **یادگیری مداوم** از معاملات زنده
- **امنیت و پایداری** در اولویت

---

**تاریخ آخرین به‌روزرسانی**: 2025-12-16
**نسخه**: Ultra Max v2.1.0 (STB5)
**وضعیت**: ✅ Production-Ready

