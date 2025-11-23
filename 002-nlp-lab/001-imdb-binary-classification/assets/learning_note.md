### 실험 #1 - IMDB 데이터셋에 대한 모델 비교
IMDB 감성 분류에 가장 적합한 pretrained 모델을 찾기 위해 여러 Transformer 기반 모델을 동일한 조건에서 비교 실험했습니다.

고정된 하이퍼파라미터는 다음과 같습니다:
```text
batch_size = 128
learning_rate = 2e-5
epochs = 3
```

다만 google/mobilebert-uncased, albert-base-v2는 동일한 세팅에서 GPU 메모리 요구량이 더 높아 Out-Of-Memory(OOM) 오류가 발생했습니다.
두 모델은 메모리 제약을 고려해 각각 batch_size를 64, 32로 조정해 실험을 진행했습니다.
(하이퍼파라미터 조정은 실험 가능성을 확보하기 위한 조치이며, 모델 간 공정한 비교를 해치지 않습니다.)

비교 대상 모델은 다음과 같습니다:
* ver.1 distilbert-base-uncased
* ver.2 google/bert_uncased_L-4_H-256_A-4
* ver.3 google/bert_uncased_L-8_H-512_A-8
* ver.4 google/mobilebert-uncased
* ver.5 albert-base-v2

각 모델의 테스트 결과는 다음과 같습니다:
| Model | Loss | Accuracy | F1 | Recall | Precision |
|-------|------|----------|----|--------|----------|
| distilbert-base-uncased | 0.2202 | 0.9198 | 0.9220 | 0.9480 | 0.8974 |
| google/bert_uncased_L-4_H-256_A-4 | 0.2675 | 0.8874 | 0.8866 | 0.8804 | 0.8929 |
| google/bert_uncased_L-8_H-512_A-8 | 0.2162 | 0.9152 | 0.9148 | 0.9108 | 0.9189 |
| google/mobilebert-uncased | 1.0644 | 0.6728 | 0.6832 | 0.7056 | 0.6622 |
| albert-base-v2 | 0.1868 | 0.9288 | 0.9285 | 0.9244 | 0.9326 |

각 실험에 대한 상세한 성능 지표는 `assets/model_performance.xlsx`에서 확인 가능합니다.
---
