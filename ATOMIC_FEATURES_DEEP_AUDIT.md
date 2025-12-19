# 🔍 تحلیل عمیق Atomic Feature Extractor - نقاط قابل ارتقا

## 📊 وضعیت فعلی

### ✅ نقاط قوت موجود

1. **Morphology Features**: خوب (body_rel, shadows, CLV)
2. **Dynamics**: خوب (log_ret, norm_range, gap)
3. **Derivatives**: خوب (1st, 2nd, 3rd order)
4. **Advanced Indicators**: خوب (ATR, RSI, Stochastic, Williams %R)
5. **Robustness**: خوب (z-scores, outlier detection)

### ⚠️ نقاط ضعف و فرصت‌های ارتقا

---

## 🎯 1. Momentum Indicators (مفقود)

### مشکل:
- **MACD** (Moving Average Convergence Divergence) وجود ندارد
- **CCI** (Commodity Channel Index) وجود ندارد
- **ROC** (Rate of Change) وجود ندارد
- **Momentum** (Price Momentum) وجود ندارد

### تأثیر:
- **MACD**: برای تشخیص تغییر روند و momentum بسیار مهم است
- **CCI**: برای تشخیص overbought/oversold و momentum
- **ROC**: برای اندازه‌گیری سرعت تغییر قیمت

### راه حل:
```python
# MACD: EMA(12) - EMA(26)
# CCI: (Price - SMA) / (0.015 * Mean Deviation)
# ROC: (Close - Close[n]) / Close[n] * 100
# Momentum: Close - Close[n]
```

---

## 🎯 2. Volume Indicators (محدود)

### مشکل:
- فقط **vol_density** و **vol_dir** وجود دارد
- **OBV** (On-Balance Volume) وجود ندارد
- **VWAP** (Volume Weighted Average Price) وجود ندارد
- **Volume Oscillator** وجود ندارد
- **Volume Rate of Change** وجود ندارد

### تأثیر:
- **OBV**: برای تأیید روند و تشخیص divergence
- **VWAP**: برای تشخیص fair value و support/resistance
- **Volume Oscillator**: برای تشخیص تغییرات volume

### راه حل:
```python
# OBV: Cumulative volume based on price direction
# VWAP: Sum(Price * Volume) / Sum(Volume)
# Volume Oscillator: (Fast MA - Slow MA) / Slow MA
```

---

## 🎯 3. Price Action Patterns (مفقود)

### مشکل:
- فقط **wick_strength** وجود دارد
- **Inside Bars** وجود ندارد
- **Outside Bars** وجود ندارد
- **Pin Bars** وجود ندارد
- **Engulfing Patterns** وجود ندارد (در technical_patterns است، اما باید در atomic هم باشد)

### تأثیر:
- **Inside Bars**: برای تشخیص consolidation
- **Outside Bars**: برای تشخیص volatility expansion
- **Pin Bars**: برای تشخیص rejection

### راه حل:
```python
# Inside Bar: High < High[-1] and Low > Low[-1]
# Outside Bar: High > High[-1] and Low < Low[-1]
# Pin Bar: Long wick, small body
```

---

## 🎯 4. Higher-order Moments (مفقود)

### مشکل:
- فقط **mean** و **std** وجود دارد
- **Skewness** وجود ندارد
- **Kurtosis** وجود ندارد

### تأثیر:
- **Skewness**: برای تشخیص asymmetry در توزیع returns
- **Kurtosis**: برای تشخیص tail risk و extreme events

### راه حل:
```python
# Skewness: E[(X - μ)³] / σ³
# Kurtosis: E[(X - μ)⁴] / σ⁴
```

---

## 🎯 5. Fractal Features (مفقود)

### مشکل:
- **Fractal Dimension** وجود ندارد
- **Self-similarity** وجود ندارد
- **Hurst Exponent** در sequential است، اما باید در atomic هم باشد

### تأثیر:
- **Fractal Dimension**: برای اندازه‌گیری complexity
- **Self-similarity**: برای تشخیص patterns در مقیاس‌های مختلف

---

## 🎯 6. Entropy Features (مفقود)

### مشکل:
- **Shannon Entropy** وجود ندارد
- **Sample Entropy** وجود ندارد
- **Approximate Entropy** وجود ندارد

### تأثیر:
- **Entropy**: برای اندازه‌گیری randomness و predictability
- **Sample Entropy**: برای تشخیص regularity در time series

---

## 🎯 7. Market Microstructure (محدود)

### مشکل:
- فقط **vol_density** وجود دارد
- **Bid-Ask Spread Proxy** وجود ندارد
- **Price Impact** وجود ندارد
- **Order Flow Imbalance** در microstructure است، اما باید در atomic هم باشد

### تأثیر:
- **Spread Proxy**: برای تشخیص liquidity
- **Price Impact**: برای اندازه‌گیری market impact

---

## 🎯 8. Regime-aware Features (مفقود)

### مشکل:
- **Volatility Regime** وجود ندارد
- **Trend Regime** وجود ندارد
- **Market State Encoding** در HMM است، اما باید در atomic هم باشد

### تأثیر:
- **Regime Features**: برای تشخیص market state در سطح atomic

---

## 🎯 9. Information-theoretic Features (مفقود)

### مشکل:
- **Mutual Information** وجود ندارد
- **Transfer Entropy** وجود ندارد
- **Granger Causality** وجود ندارد

### تأثیر:
- **Mutual Information**: برای اندازه‌گیری dependency
- **Transfer Entropy**: برای تشخیص causality

---

## 🎯 10. Multi-scale Features (محدود)

### مشکل:
- فقط **vol_10, vol_30, vol_100** وجود دارد
- **Multi-scale Volatility** وجود ندارد
- **Multi-scale Momentum** وجود ندارد

### تأثیر:
- **Multi-scale Features**: برای تشخیص patterns در مقیاس‌های مختلف

---

## 🎯 11. Advanced Statistical Features (محدود)

### مشکل:
- فقط **z-scores** وجود دارد
- **Percentile Ranks** وجود ندارد
- **Quantile Features** وجود ندارد
- **Rank Features** وجود ندارد

### تأثیر:
- **Percentile Ranks**: برای normalization robust
- **Quantile Features**: برای تشخیص extreme values

---

## 🎯 12. Time-based Features (مفقود)

### مشکل:
- **Time of Day** وجود ندارد
- **Day of Week** وجود ندارد
- **Hour of Day** وجود ندارد

### تأثیر:
- **Time Features**: برای تشخیص intraday patterns

---

## 📈 اولویت‌بندی ارتقا

### 🔴 اولویت بالا (High Impact, Low Complexity)

1. **Momentum Indicators** (MACD, CCI, ROC, Momentum)
2. **Volume Indicators** (OBV, VWAP, Volume Oscillator)
3. **Price Action Patterns** (Inside/Outside/Pin Bars)
4. **Higher-order Moments** (Skewness, Kurtosis)
5. **Percentile Ranks** (برای normalization)

### 🟡 اولویت متوسط (High Impact, Medium Complexity)

6. **Fractal Features** (Fractal Dimension)
7. **Entropy Features** (Shannon, Sample Entropy)
8. **Regime-aware Features** (Volatility/Trend Regime)
9. **Multi-scale Features** (Multi-scale Volatility/Momentum)

### 🟢 اولویت پایین (Medium Impact, High Complexity)

10. **Information-theoretic Features** (Mutual Information, Transfer Entropy)
11. **Time-based Features** (Time of Day, Day of Week)
12. **Advanced Microstructure** (Spread Proxy, Price Impact)

---

## 💡 پیشنهادات پیاده‌سازی

### Phase 1: Momentum & Volume (سریع و مؤثر)

```python
def _add_momentum_indicators(self, df: pl.DataFrame) -> pl.DataFrame:
    # MACD, CCI, ROC, Momentum
    pass

def _add_volume_indicators(self, df: pl.DataFrame) -> pl.DataFrame:
    # OBV, VWAP, Volume Oscillator
    pass
```

### Phase 2: Price Action & Statistics (متوسط)

```python
def _add_price_action_patterns(self, df: pl.DataFrame) -> pl.DataFrame:
    # Inside/Outside/Pin Bars
    pass

def _add_higher_order_moments(self, df: pl.DataFrame) -> pl.DataFrame:
    # Skewness, Kurtosis
    pass
```

### Phase 3: Advanced Features (پیشرفته)

```python
def _add_entropy_features(self, df: pl.DataFrame) -> pl.DataFrame:
    # Shannon, Sample Entropy
    pass

def _add_fractal_features(self, df: pl.DataFrame) -> pl.DataFrame:
    # Fractal Dimension
    pass
```

---

## 🎯 نتیجه‌گیری

**نقاط قابل ارتقا شناسایی شده: 12 مورد**

- **اولویت بالا**: 5 مورد (Momentum, Volume, Price Action, Moments, Percentiles)
- **اولویت متوسط**: 4 مورد (Fractal, Entropy, Regime, Multi-scale)
- **اولویت پایین**: 3 مورد (Information-theoretic, Time-based, Microstructure)

**تأثیر پیش‌بینی شده**: 
- افزایش **5-10%** در accuracy با Phase 1
- افزایش **10-15%** با Phase 1 + Phase 2
- افزایش **15-20%** با تمام Phases

