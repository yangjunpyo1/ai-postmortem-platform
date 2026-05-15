# 🚨 AI 기반 장애 Postmortem 자동화 플랫폼

![GitHub stars](https://img.shields.io/github/stars/yangjunpyo1/ai-postmortem-platform)
![GitHub issues](https://img.shields.io/github/issues/yangjunpyo1/ai-postmortem-platform)
![GitHub last commit](https://img.shields.io/github/last-commit/yangjunpyo1/ai-postmortem-platform)

> 슬랙 대화를 AI가 분석하여 Postmortem 문서를 자동으로 생성하는 경량 자동화 플랫폼

---

## 1. 프로젝트 소개

슬랙 대화를 Claude AI가 분석하여
Postmortem 문서를 자동으로 생성하고
웹 대시보드에서 장애 히스토리를
체계적으로 관리할 수 있는
경량 자동화 플랫폼입니다.

### 목표
- AWS CloudWatch로 장애 자동 감지
- 심각도별 슬랙 알림으로 불필요한 온콜 호출 최소화
- 장애 종료 시 슬랙 대화 자동 수집
- Claude AI가 Postmortem 문서 자동 생성
- 유사 장애 자동 검색으로 반복 장애 예방
- Grafana로 장애 메트릭 시각화
- 웹 대시보드에서 장애 히스토리 조회/관리
- Terraform IaC로 누구든 동일한 환경 즉시 구축

### 프로젝트 선택 이유

인프라 구축 및 실습 과정에서 트러블슈팅이 발생할 때마다
원인과 해결 과정을 수동으로 정리해야 하는 불편함을 직접 경험했습니다.
기업 엔지니어들도 서비스 장애 시 동일한 과정을 반복해야 한다는 점에서
AI를 활용한 자동화의 필요성을 느껴 이 프로젝트를 시작했습니다.

---

## 2. 주요 기능

| 기능 | 설명 |
|---|---|
| 🔍 장애 자동 감지 | CloudWatch가 CPU, 메모리, 에러율 임계치 초과 시 자동 감지 |
| 🔔 심각도별 슬랙 알림 | Critical / Warning / Info 단계별 알림 자동 전송 |
| 💬 슬랙 대화 자동 수집 | 장애 종료 명령어 입력 시 대화 자동 수집 |
| 🤖 AI Postmortem 생성 | Claude AI가 슬랙 대화 분석 후 문서 자동 생성 |
| 📊 Grafana 시각화 | 장애 메트릭 실시간 대시보드 |
| 🖥️ 웹 대시보드 | 장애 목록, 문서 조회, 통계 한눈에 확인 |

---

## 3. 시스템 아키텍처

> 🚧 다이어그램 추후 업데이트 예정

[장애 발생] 서버 CPU/메모리/에러율 임계치 초과
↓
[AWS CloudWatch] 장애 자동 감지
↓
[SNS + SQS] 메시지 유실 없이 전달
↓
[AWS Lambda] 슬랙 알림 전송 + 대화 수집
↓
[Claude API] 슬랙 대화 분석 → Postmortem 문서 자동 생성
↓
[AWS RDS] 문서 저장
↓
[웹 대시보드] 장애 목록 / 문서 조회 / 통계

---

## 4. 기술 스택

### Cloud
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonaws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat&logo=terraform&logoColor=white)

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)

### Frontend
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)

### Monitoring
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat&logo=grafana&logoColor=white)
![CloudWatch](https://img.shields.io/badge/CloudWatch-FF4F8B?style=flat&logo=amazonaws&logoColor=white)

### AI
![Claude](https://img.shields.io/badge/Claude_API-000000?style=flat&logo=anthropic&logoColor=white)

### Communication
![Slack](https://img.shields.io/badge/Slack-4A154B?style=flat&logo=slack&logoColor=white)

---

## 5. 시연 시나리오

1. 서버 CPU 90% 초과 장애 발생
   └── 테스트: CloudWatch Alarm 강제 트리거

2. CloudWatch 자동 감지
   └── 설정된 임계치 초과 시 SNS 발행

3. 슬랙으로 🔴 Critical 알림 수신
   └── SQS → Lambda → 슬랙 채널 알림 전송

4. 엔지니어들 슬랙에서 장애 대응
   └── 원인 파악, 해결 과정 슬랙에서 대화

5. 복구 완료 후 /종료 명령어 입력
   └── 슬랙 봇이 명령어 감지

6. 슬랙 대화 자동 수집
   └── Lambda가 장애 채널 대화 전체 수집

7. Claude AI가 Postmortem 문서 자동 생성
   └── 슬랙 대화 분석 → 문서 초안 자동 작성

8. 웹 대시보드에서 문서 확인 및 수정
   └── AI 생성 문서 검토 후 최종 저장

---

## 6. 기대 효과

| 기존 방식 | 이 플랫폼 |
|---|---|
| 수동으로 로그 확인 후 정리 | AI가 자동 분석 및 문서 생성 |
| 형식 없이 노션/구글 docs 기록 | 일관된 형식 자동 유지 |
| 개인 보관으로 히스토리 누락 | 자동 누적 관리 |
| 반복 장애 발생 위험 | 히스토리 기반 재발 방지 |

---

## 7. 폴더 구조

ai-postmortem-platform/
├── docs/                   # 설계 문서
│   ├── 01_기획서.md
│   ├── 02_요구사항정의서.md
│   ├── 03_ERD.md
│   ├── 04_API명세서.md
│   └── 05_기술스택.md
├── src/                    # 백엔드 코드 (예정)
├── frontend/               # 프론트엔드 코드 (예정)
└── terraform/              # 인프라 코드 (예정)

---

## 8. 문서

| 문서 | 링크 |
|---|---|
| 기획서 | [01_기획서.md](docs/01_기획서.md) |
| 요구사항 정의서 | [02_요구사항정의서.md](docs/02_요구사항정의서.md) |
| ERD | [03_ERD.md](docs/03_ERD.md) |
| API 명세서 | [04_API명세서.md](docs/04_API명세서.md) |
| 기술 스택 | [05_기술스택.md](docs/05_기술스택.md) |
