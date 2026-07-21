#  AI 기반 장애 Postmortem 자동화 플랫폼

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
- CloudWatch 알람 발생 시 RDS에 장애 자동 등록
- 심각도별 슬랙 알림으로 불필요한 온콜 호출 최소화
- 장애 종료 시 슬랙 대화 자동 수집
- Claude AI가 Postmortem 문서 자동 생성
- 카테고리/심각도 기반 유사 장애 조회로 반복 장애 예방
- Grafana로 장애 메트릭 시각화
- 웹 대시보드에서 장애 히스토리 조회/관리
- Terraform IaC로 누구든 동일한 환경 즉시 구축
- GitHub Actions CI/CD로 코드 변경 시 자동 배포

### 프로젝트 선택 이유

인프라 구축 및 실습 과정에서 트러블슈팅이 발생할 때마다
원인과 해결 과정을 수동으로 정리해야 하는 불편함을 직접 경험했습니다.
기업 엔지니어들도 서비스 장애 시 동일한 과정을 반복해야 한다는 점에서
AI를 활용한 자동화의 필요성을 느껴 이 프로젝트를 시작했습니다.

---

## 2. 주요 기능

| 기능 | 설명 |
|---|---|
|  장애 자동 감지 | CloudWatch가 CPU, 메모리, 에러율 임계치 초과 시 자동 감지 |
|  장애 자동 등록 | CloudWatch 알람 발생 시 RDS에 장애 자동 등록 |
|  심각도별 슬랙 알림 | Critical / Warning / Info 단계별 알림 자동 전송 |
|  슬랙 대화 자동 수집 | 장애 종료 명령어 입력 시 대화 자동 수집 |
|  AI Postmortem 생성 | Claude AI가 슬랙 대화 분석 후 문서 자동 생성 |
|  유사 장애 검색 | 카테고리/심각도 기반 유사 장애 조회 |
|  Grafana 시각화 | 장애 메트릭 실시간 대시보드 |
|  웹 대시보드 | 장애 목록, 문서 조회, 통계 한눈에 확인 |

---

## 3. 시스템 아키텍처

![시스템 아키텍처](https://github.com/user-attachments/assets/d98c981e-d890-43e3-822b-15c129d1e4a3)

### 처리 흐름

```
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
```

### 네트워크 구성 (VPC)

```
VPC (10.0.0.0/16)

Public Subnet
├── AZ-a (10.0.10.0/24)  → NAT Gateway
└── AZ-c (10.0.100.0/24)

Private Subnet 1 (App Layer)
├── AZ-a (10.0.20.0/24)  → Lambda(FastAPI), Lambda(알림 전송), EC2(Grafana)
└── AZ-c (10.0.120.0/24) → Lambda(Postmortem 자동화)

Private Subnet 2 (DB Layer)
├── AZ-a (10.0.30.0/24)  → RDS (Primary)
└── AZ-c (10.0.130.0/24) → RDS (Standby)
```

세 개의 독립된 Lambda 함수로 구성되어 있습니다.

| Lambda | 트리거 | 역할 |
|---|---|---|
| `yp-lambda-fastapi` | API Gateway | 웹 대시보드용 REST API (FastAPI + Mangum) |
| `yp-lambda-alarm` | SQS (SNS 경유) | CloudWatch 알람을 심각도별 슬랙 메시지로 전송 |
| `yp-lambda-postmortem` | Slack `/resolve` 명령어 (비동기 호출) | 슬랙 대화 + CloudWatch 로그/메트릭 수집 → Claude API 분석 → RDS 저장 |

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

### CI/CD
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)

---

## 5. 설치 및 실행 방법

### 사전 요구사항

- Node.js 18 이상, npm
- Python 3.11
- Terraform 1.0 이상
- 자격 증명이 설정된 AWS CLI
- Slack Workspace 관리자 권한 (Bot Token 발급용)
- Claude API 키

### 1) 저장소 클론

```bash
git clone https://github.com/yangjunpyo1/ai-postmortem-platform.git
cd ai-postmortem-platform
```

### 2) 인프라 배포 (Terraform)

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

VPC, RDS(MySQL), Lambda 3종, API Gateway, SNS/SQS, CloudWatch 알람, EC2(Grafana)가 생성됩니다.
실행 전 `terraform.tfvars`에 필요한 값을 채워야 합니다 (아래 [환경변수 설정](#6-환경변수-설정) 참고).

### 3) 백엔드 설정

```bash
cd backend
pip install -r requirements.txt
```

`.env` 파일을 생성한 뒤(아래 환경변수 참고), DB 마이그레이션을 적용합니다.

```bash
alembic upgrade head
```

로컬에서 API를 직접 확인하고 싶다면 다음과 같이 실행할 수 있습니다 (개발/테스트 용도).

```bash
uvicorn app.main:app --reload
```

실제 운영 환경에서는 로컬 서버 대신 AWS Lambda(Mangum)로 배포됩니다. Lambda 배포용 zip은 다음과 같이 패키징하여 `terraform/modules/lambda/lambda_fastapi.zip` 경로에 위치시킵니다.

```bash
pip install -r requirements.txt -t package
# app/ 코드와 package/ 내 의존성을 함께 압축하여 lambda_fastapi.zip 생성
```

### 4) 프론트엔드 설정

```bash
cd frontend
npm install
```

`.env` 파일에 `REACT_APP_API_URL`을 설정한 뒤 개발 서버를 실행합니다.

```bash
npm start          # http://localhost:3000
npm run build        # 프로덕션 빌드 (S3/CloudFront 배포용)
```

### 5) Slack 앱 연동

1. Slack API 사이트에서 앱을 생성하고 Bot Token(`xoxb-...`)을 발급받습니다.
2. Event Subscriptions Request URL: `{API Gateway 주소}/slack/events`
3. Slash Command `/resolve` 등록, Request URL: `{API Gateway 주소}/slack/commands`
4. 발급받은 토큰/채널 ID를 `terraform.tfvars`에 입력 후 재배포합니다.

---

## 6. 환경변수 설정

민감한 값이 포함된 `.env`, `.env.production`, `terraform.tfvars` 파일은 모두 `.gitignore`에 등록되어 있습니다. 저장소를 클론한 뒤 아래 내용을 참고해 각자 로컬에 새로 생성해야 합니다.

### `backend/.env`

```env
DB_HOST=your-rds-endpoint
DB_NAME=postmortem
DB_USER=your-db-username
DB_PASSWORD=your-db-password
SECRET_KEY=change-this-to-a-random-secret-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- `SECRET_KEY`는 JWT 서명에 사용되며, 운영 환경에서는 반드시 예측 불가능한 값으로 변경해야 합니다.

### `frontend/.env` / `frontend/.env.production`

```env
REACT_APP_API_URL=https://{API_GATEWAY_ID}.execute-api.ap-northeast-2.amazonaws.com/dev
```

- 개발용(`.env`)과 배포용(`.env.production`)에 각각 대응하는 API Gateway 스테이지 URL을 입력합니다.

### `terraform/terraform.tfvars`

```hcl
aws_region   = "ap-northeast-2"
project_name = "yp"
environment  = "dev"

rds_password            = "your-rds-master-password"
slack_bot_token         = "xoxb-your-slack-bot-token"
slack_channel_id        = "C0XXXXXXX"
claude_api_key          = "sk-ant-your-claude-api-key"
grafana_admin_password  = "your-grafana-admin-password"
```

- `rds_password`, `slack_bot_token`, `claude_api_key`, `grafana_admin_password`는 Terraform 변수에서 `sensitive = true`로 표시되어 있습니다.
- 이 값들은 `terraform apply` 시 각 Lambda(`yp-lambda-alarm`, `yp-lambda-postmortem`)의 환경변수와 EC2(Grafana) `user_data`에 자동으로 주입되므로, Lambda/EC2에는 별도로 설정할 필요가 없습니다.
- 네트워크 CIDR, 인스턴스 타입 등 나머지 변수는 `terraform/variables.tf`의 기본값을 그대로 사용하거나 필요에 맞게 덮어쓸 수 있습니다.

---

## 7. 시연 시나리오

1. 서버 CPU 90% 초과 장애 발생
   └── 테스트: CloudWatch Alarm 강제 트리거

2. CloudWatch 자동 감지
   └── 설정된 임계치 초과 시 SNS 발행

3. 슬랙으로 🔴 Critical 알림 수신
   └── SQS → Lambda → 슬랙 채널 알림 전송

4. 엔지니어들 슬랙에서 장애 대응
   └── 원인 파악, 해결 과정 슬랙에서 대화

5. 복구 완료 후 `/resolve` 명령어 입력
   └── 슬랙 봇이 명령어 감지

6. 슬랙 대화 자동 수집
   └── Lambda가 장애 채널 대화 전체 수집

7. Claude AI가 Postmortem 문서 자동 생성
   └── 슬랙 대화 분석 → 문서 초안 자동 작성

8. 웹 대시보드에서 문서 확인 및 수정
   └── AI 생성 문서 검토 후 최종 저장

---

## 8. 기대 효과

| 기존 방식 | 이 플랫폼 |
|---|---|
| 수동으로 로그 확인 후 정리 | AI가 자동 분석 및 문서 생성 |
| 형식 없이 노션/구글 docs 기록 | 일관된 형식 자동 유지 |
| 개인 보관으로 히스토리 누락 | 자동 누적 관리 |
| 반복 장애 발생 위험 | 히스토리 기반 재발 방지 |

---

## 9. 폴더 구조

```
ai-postmortem-platform/
├── docs/                   # 설계 문서
│   ├── 01_기획서.md
│   ├── 02_요구사항정의서.md
│   ├── 03_ERD.md
│   ├── 04_API명세서.md
│   ├── 05_기술스택.md
│   └── 06_시스템아키텍처.md
├── backend/                 # FastAPI 백엔드 (Lambda 배포)
│   ├── app/
│   │   ├── api/              # 라우터 (auth, incidents, postmortems, similar, statistics, slack)
│   │   ├── models/            # SQLAlchemy 모델
│   │   ├── schemas/            # Pydantic 스키마
│   │   └── core/               # 설정, 보안(JWT/bcrypt)
│   └── alembic/               # DB 마이그레이션
├── lambda/                  # 알림/Postmortem 자동화 Lambda
│   ├── alarm/                 # CloudWatch 알람 → 슬랙 알림
│   └── postmortem/             # 슬랙 대화 수집 → Claude API → RDS 저장
├── frontend/                # React 대시보드
│   └── src/
│       ├── pages/              # Dashboard, IncidentList, PostmortemDetail, Statistics 등
│       ├── components/          # PrivateRoute 등 공통 컴포넌트
│       └── api/                 # axios 클라이언트
└── terraform/                # 인프라 코드 (VPC, RDS, Lambda, API Gateway, CloudWatch, EC2 등)
```

---

## 10. 문서

| 문서 | 링크 |
|---|---|
| 기획서 | [01_기획서.md](docs/01_기획서.md) |
| 요구사항 정의서 | [02_요구사항정의서.md](docs/02_요구사항정의서.md) |
| ERD | [03_ERD.md](docs/03_ERD.md) |
| API 명세서 | [04_API명세서.md](docs/04_API명세서.md) |
| 기술 스택 | [05_기술스택.md](docs/05_기술스택.md) |
| 시스템 아키텍처 | [06_시스템아키텍처.md](docs/06_시스템아키텍처.md) |
