# AI 기반 장애 Postmortem 자동화 플랫폼

![GitHub stars](https://img.shields.io/github/stars/yangjunpyo1/ai-postmortem-platform)
![GitHub issues](https://img.shields.io/github/issues/yangjunpyo1/ai-postmortem-platform)
![GitHub last commit](https://img.shields.io/github/last-commit/yangjunpyo1/ai-postmortem-platform)

> CloudWatch 장애 자동 감지 → 슬랙 알림 → Claude AI가 Postmortem 문서 자동 생성

---

## 주요 기능

| 기능 | 설명 |
|---|---|
| 장애 자동 감지 | CloudWatch가 CPU, 메모리, 에러율 임계치 초과 시 자동 감지 |
| 장애 자동 등록 | CloudWatch 알람 발생 시 RDS에 장애 자동 등록 |
| 심각도별 슬랙 알림 | Critical / Warning / Info 단계별 알림 자동 전송 |
| AI Postmortem 생성 | Claude AI가 슬랙 대화 + CloudWatch 로그 분석 후 문서 자동 생성 |
| 유사 장애 검색 | 과거 유사 장애 자동 매칭 |
| Grafana 시각화 | 장애 메트릭 실시간 대시보드 |
| CI/CD 자동화 | GitHub Actions로 Lambda/프론트엔드 자동 배포 |

---

## 아키텍처

![시스템 아키텍처](https://github.com/user-attachments/assets/d98c981e-d890-43e3-822b-15c129d1e4a3)

```
CloudWatch → SNS → SQS → Lambda(알림 전송 + RDS 장애 자동 등록) → Slack
                                                                     ↓
                                                               /resolve 명령어
                                                                     ↓
                                                     Lambda(슬랙 대화 + 로그 수집)
                                                                     ↓
                                                              Claude API 분석
                                                                     ↓
                                                            RDS 저장 → 웹 대시보드
```

---

## 기술 스택

![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonaws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat&logo=terraform&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat&logo=grafana&logoColor=white)
![Claude](https://img.shields.io/badge/Claude_API-000000?style=flat&logo=anthropic&logoColor=white)
![Slack](https://img.shields.io/badge/Slack-4A154B?style=flat&logo=slack&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)

---

## 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/yangjunpyo1/ai-postmortem-platform.git
cd ai-postmortem-platform
```

### 2. terraform.tfvars 작성
```hcl
rds_password           = "your-password"
slack_bot_token        = "xoxb-your-token"
slack_channel_id       = "C0XXXXXXX"
claude_api_key         = "sk-ant-your-key"
grafana_admin_password = "your-password"
```

### 3. 인프라 배포
```bash
cd terraform
terraform init
terraform apply
```

### 4. 프론트엔드 배포
```bash
.\scripts\update-config.ps1
```

또는 GitHub Actions → Deploy Frontend → Run workflow

### 5. Slack 앱 설정
- Event Subscriptions: `{API Gateway URL}/slack/events`
- Slash Command `/resolve`: `{API Gateway URL}/slack/commands`
- Bot Token Scopes: `channels:history`, `chat:write`, `commands`, `users:read`

---

## 시연 시나리오

1. CloudWatch 알람 발생 → 슬랙 알림 수신 + RDS 자동 장애 등록
2. 슬랙에서 장애 대응 대화
3. `/resolve` 명령어 입력
4. Claude AI가 슬랙 대화 + 로그 분석 → Postmortem 자동 생성
5. 웹 대시보드에서 문서 확인

---

## 문서

| 문서 | 링크 |
|---|---|
| 기획서 | [01_기획서.md](docs/01_기획서.md) |
| ERD | [03_ERD.md](docs/03_ERD.md) |
| API 명세서 | [04_API명세서.md](docs/04_API명세서.md) |
| 시스템 아키텍처 | [06_시스템아키텍처.md](docs/06_시스템아키텍처.md) |
