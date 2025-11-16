# Mental Health Chat Helper

A mental health chatbot using a 3-model hierarchical detection system (Suicide → Emotion → Mental Health) with empathetic response templates and crisis intervention capabilities.

## Features

- **Crisis Detection**: Hybrid keyword-based + ML model for suicide risk detection with 95% keyword confidence
- **Emotion Analysis**: 6-class emotion detection (joy, sadness, anger, fear, love, surprise) using fine-tuned RoBERTa
- **Mental Health Assessment**: Detects Anxiety, Depression, Stress, Bipolar, and Personality disorders
- **Structured Responses**: Template-based empathetic responses with condition-specific self-help activities
- **Safety Features**: Automatic chat locking and crisis resource display on suicide detection

## Setup Instructions

### Prerequisites
- **Python**: 3.10 or higher
- **RAM**: Minimum 8GB (required for loading 3 RoBERTa-base models)
- **Storage**: ~2GB for models and dependencies
- **GPU**: Optional (CPU inference supported, ~2-3s response time)

### Installation Steps

1. **Clone/Navigate to Project**
```bash
cd mental-health-sentiment-app
```

2. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Add models**
```bash
ls models/
# Expected output: emotion_model/ mh_model/ suicide_model/
```

Each model directory must contain:
- `config.json` - Model architecture configuration
- `pytorch_model.bin` - Trained model weights
- `tokenizer_config.json` - Tokenizer settings
- `vocab.json` - Vocabulary file
- `merges.txt` - BPE merges
- `label_mapping.json` - Class label mappings

### Running the Application

```bash
streamlit run app/main.py
```

The application will automatically open in your browser at `http://localhost:8501`

## Model Training

Models were trained in `emotion_detection.ipynb` (Google Colab):

| Model | Accuracy | Training Samples | Architecture |
|-------|----------|------------------|--------------|
| Suicide | 99.23% | 232K | RoBERTa-base |
| Emotion | 93.75% | 16K | RoBERTa-base |
| Mental Health | 93.30% | 40K | RoBERTa-base |

**Training Notebook**: `emotion_detection.ipynb` contains all preprocessing, training, and evaluation code.

## Architecture

```
app/
├── main.py                     # Entry point
├── chat_ui.py                  # Streamlit chat interface
├── decision_tree.py            # Decision logic + keyword fallback
├── detection.py                # Model inference
├── model_loader.py             # Model loading with caching
└── data/
    ├── response_templates.py   # Response text
    └── cures.py               # Self-help activities
```

## How It Works

1. **Suicide Check** (every message)
   - Keywords checked first → 95% confidence if matched
   - ML model as fallback → 40% threshold
   - If detected → Lock chat, show crisis resources

2. **Emotion Detection**
   - Positive → Supportive listening
   - Negative → Proceed to mental health check

3. **Mental Health Assessment** (after 2 negative messages)
   - If condition detected → Show targeted strategies
   - If normal → Show emotion-based coping

## Future Improvements

   - Enhanced Empathy & Responses
   - Improved Suicide Model
   - Better Coping Strategies
   - Safety & Monitoring

## Crisis Resources

**iCall Helpline**: 9152987821
**Hours**: Monday-Saturday, 10:00 AM - 8:00 PM

## Author

Yaswitha Boppana
