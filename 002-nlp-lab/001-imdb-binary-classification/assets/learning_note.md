### 실험 #1 - IMDB 데이터셋에 대한 모델 비교
IMDB 감성 분류에 가장 적합한 pretrained 모델을 찾기 위해 여러 Transformer 기반 모델을 동일한 조건에서 비교 실험했습니다.

고정된 하이퍼파라미터는 다음과 같습니다:
```text
batch_size = 128
learning_rate = 2e-5
epochs = 3
```

비교 대상 모델은 다음과 같습니다:
* ver.1 distilbert-base-uncased
* ver.2 google/bert_uncased_L-4_H-256_A-4
* ver.3 google/bert_uncased_L-8_H-512_A-8
* ver.4 google/mobilebert-uncased
* ver.5 albert-base-v2

각 실험에 대한 상세한 성능 지표는 `assets/model_performance.xlsx`에서 확인 가능합니다.
---