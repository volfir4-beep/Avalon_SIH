# AVALON
### Intelligent Real-Time Anomaly Detection System for Temperature, Pressure & Humidity Sensors in Automatic Weather Stations (AWS)

> Detects sensor faults, spikes, frozen values, drift, and communication errors in AWS data streams — in real time, with explainable AI and confidence scoring.

---

## 1. Problem We're Solving

Automatic Weather Stations (AWS) feed real-time atmospheric data into forecasting, disaster management, aviation, and agriculture systems. But sensors fail silently: they drift, freeze, spike, lose comms, or produce readings that are internally inconsistent (e.g. high temperature + high humidity + no pressure drop, which physically shouldn't co-occur). Traditional fixed-threshold QC catches only the obvious cases and misses subtle, compound, or context-dependent faults — while also throwing false alarms during genuine extreme weather.

**Goal:** build a system that tells the difference between a *real* weather event and a *faulty sensor*, using only temperature, pressure, and humidity, and explains *why* it flagged something.

---

## 2. Our Solution — Architecture Overview

SkyGuard AI is a 4-layer pipeline, going from raw sensor data to an explained, actionable alert.

```
1. Data Acquisition  →  2. Feature Engineering  →  3. Hybrid Anomaly Detection  →  4. Reasoning & Explainability  →  5. Decision & Alerts  →  6. Human/System Action  →  7. Feedback Loop
```

### Layer 1 — Data Acquisition & Monitoring
Ingests live readings (MQTT/API/IoT) from AWS stations, neighboring stations (spatial context), and optionally satellite/model data (e.g. INSAT-3DR) for cross-checking. Feeds a real-time dashboard: live T/P/RH plots, historical trends (1h/24h/7d), station map, per-station health, and an alerts snapshot.

### Layer 2 — Hybrid Multi-Model Anomaly Detection Engine
No single model catches every fault type, so four detectors run in parallel on engineered features (raw values, rolling mean/std, 1h/24h deltas, neighbor stats, time-of-day/season features, station metadata):

| Model | Catches | Output |
|---|---|---|
| **Harmonic Regression** | Deviation from expected daily/seasonal baseline | Residual score |
| **LSTM Autoencoder** | Temporal pattern breaks — drift, frozen values, noise bursts | Reconstruction error |
| **Isolation Forest** | Unusual multivariate combinations across T/P/RH | Isolation score |
| **Spatial Consistency Check** | Single-station faults invisible when compared to neighbors | Spatial deviation score |

These four scores are combined via a **weighted ensemble** into a single **Final Anomaly Score (0–1)**. If score ≥ threshold → flagged as anomaly.

### Layer 3 — Reasoning & Explainability Engine
Takes the evidence (model scores, residuals, neighbor comparison, rate of change, historical pattern, satellite/weather context if available) and performs **root-cause inference** — is this a sensor drift, humidity sensor malfunction, pressure bias, communication error, environmental effect, or genuine extreme weather? Produces an explainability output: key contributing factors, SHAP/feature importance, temporal explanation, neighbor difference, and a human-readable reasoning summary.

### Layer 4 — Sensor Intelligence & Response Layer
Converts the diagnosis into something actionable:
- Anomaly result (normal / anomaly + type)
- Confidence score (0–100%)
- Severity level (Low/Medium/High/Critical)
- Sensor health score (0–100) with trend
- Optional corrected/imputed value
- Recommended maintenance action
- Real-time alert (SMS/Email/App/Dashboard)

### Supporting layers
- **Model Evaluation:** confusion matrix, precision/recall/F1, ROC-AUC/PR-AUC, false alarm rate, detection latency, per-station and per-anomaly-type performance.
- **Security & Data Privacy:** encryption in transit, secure storage at rest, ID hashing/pseudonymization, access control, audit logging.

---

## 3. Dataset — `synthetic_aws_data.csv`

We use a synthetic AWS dataset that mirrors real deployment characteristics: 5 stations, 10-minute sampling cadence, over a 30-day period, with realistic injected anomalies for training/evaluating the detectors.

| Property | Value |
|---|---|
| Stations | AWS-01 … AWS-05 |
| Time range | 2026-07-01 to 2026-07-30 |
| Sampling interval | 10 minutes |
| Total rows | 21,600 |
| Anomalous rows | 629 (≈2.9%) |
| Columns | `station_id`, `timestamp`, `temperature_c`, `pressure_hpa`, `humidity_pct`, `is_anomaly`, `anomaly_type` |

**Anomaly type breakdown (matches Layer 2's fault categories):**

| Anomaly Type | Count | Description |
|---|---|---|
| `drift` | 281 | Gradual sensor calibration drift over time |
| `noise_burst` | 155 | Short burst of high-variance noisy readings |
| `comm_gap` | 96 | Communication/reporting gap |
| `frozen` | 46 | Sensor stuck repeating the same value |
| `spike` | 31 | Sudden, isolated out-of-range reading |
| `multivariate_inconsistency` | 20 | T/P/RH combination that's physically implausible together (e.g. the "55°C reading" scenario from the PS) |
| `none` | 20,971 | Normal, clean observation |

This directly supports **all four Layer 2 detectors**: `drift`/`frozen` are best caught by the LSTM autoencoder, `spike`/`noise_burst` by harmonic regression residuals and Isolation Forest, `multivariate_inconsistency` by Isolation Forest + spatial consistency, and `comm_gap` by simple availability monitoring feeding into sensor health.

The `is_anomaly` and `anomaly_type` columns serve as **ground truth labels** for supervised evaluation (confusion matrix, precision/recall/F1) even though the core detection engine itself is designed to run unsupervised/self-learning in production, where such labels won't exist.

---

## 4. Why This Design Wins on the Evaluation Criteria

- **Innovation & Novelty:** hybrid ensemble (seasonal baseline + temporal DL + multivariate ML + spatial cross-check) rather than a single model or fixed thresholds.
- **Detection Accuracy:** four independent, complementary signals reduce blind spots any one method has.
- **Real-Time Capability:** streaming ingestion (MQTT/API/IoT) with per-window scoring.
- **Explainability:** dedicated reasoning layer with SHAP/feature importance and a plain-language root-cause summary, not just a binary flag.
- **Scalability:** stateless per-station scoring + shared spatial context, deployable across large networks.
- **Practical Deployability / Energy Efficiency:** lightweight models (harmonic regression, isolation forest) can run on constrained hardware (e.g. ESP32), with the LSTM autoencoder run centrally.
- **Visualization/UI:** Layer 1 dashboard gives live plots, map view, and alert snapshots out of the box.

---

## 5. Files in This Repo

