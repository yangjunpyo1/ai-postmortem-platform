
Claude가 응답을 완료했습니다
terraform/backend.tf가 수정됐어. bucket 값 추가한 거 커밋해야 해.

git add terraform/backend.tf
git commit -m "fix: backend.tf bucket 이름 복원"
git push origin main
PS C:\Users\양준표\Documents\ai-postmortem-platform> git add terraform/backend.tf
>> git commit -m "fix: backend.tf bucket 이름 복원"
>> git push origin main
warning: in the working copy of 'terraform/backend.tf', LF will be replaced by CRLF the next time Git touches it
[main 77f9c65] fix: backend.tf bucket 이름 복원
 1 file changed, 1 insertion(+)
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 8 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 431 bytes | 431.00 KiB/s, done.
Total 4 (delta 3), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To https://github.com/yangjunpyo1/ai-postmortem-platform
   9ea8949..77f9c65  main -> main
PS C:\Users\양준표\Documents\ai-postmortem-platform>

더 보기
완료됐어. lambda/alarm/package/랑 response.json은 gitignore에 추가해야 해.

git add .gitignore
먼저 .gitignore 열어서 이거 추가해봐.

lambda/alarm/package/
response.json

# Byte-compiled / optimized / DLL files __pycache__/ *.py[codz] *$py.class # C extensions *.so # Distribution / packaging .Python build/ develop-eggs/ dist/ downloads/ eggs/ .eggs/ lib/ lib64/ parts/ sdist/ var/ wheels/ share/python-wheels/ *.egg-info/ .installed.cfg *.egg

pasted

이게 전체코드인데 수정해서 줘봐

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[codz]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py.cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

.pdm-python
.pdm-build/
.pixi
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# Redis
*.rdb
*.aof
*.pid

# RabbitMQ
mnesia/
rabbitmq/
rabbitmq-data/

# ActiveMQ
activemq-data/

# SageMath parsed files
*.sage.py

# Environments
.env
.envrc
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# Abstra
.abstra/

# Visual Studio Code
# .vscode/
# Temporary file for partial code execution
tempCodeRunnerFile.py

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Marimo
marimo/_static/
marimo/_lsp/
__marimo__/

# Streamlit
.streamlit/secrets.toml

# Terraform
*.tfvars
*.tfstate
*.tfstate.backup
.terraform/
*.zip
backend/package/
backend/lambda_fastapi.zip
lambda/postmortem/package/
lambda/alarm/package/
response.json
저장하고 커밋해봐.

git add .gitignore
git commit -m "chore: gitignore에 alarm package, response.json 추가"
git push origin main
PS C:\Users\양준표\Documents\ai-postmortem-platform> git add .gitignore
>> git commit -m "chore: gitignore에 alarm package, response.json 추가"
>> git push origin main
[main d128885] chore: gitignore에 alarm package, response.json 추가
 1 file changed, 3 insertions(+), 57 deletions(-)
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 423 bytes | 423.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/yangjunpyo1/ai-postmortem-platform
   77f9c65..d128885  main -> main

더 보기
완료됐어. 이제 정말 마무리됐어.

오늘 한 것들 정리하면

CI/CD 구축 (Lambda, 프론트엔드 자동 배포)
Terraform Remote Backend
EC2 ID, URL 동적 참조 자동화
UI 전면 재설계 (다크 모드, 사이드바)
KST 시간 표시
Postmortem 프롬프트 개선
CloudWatch 알람 → RDS 자동 장애 등록
각종 버그 수정
수고했어.


# AI 기반 장애 Postmortem 자동화 플랫폼 ![GitHub stars](https://img.shields.io/github/stars/yangjunpyo1/ai-postmortem-platform) ![GitHub issues](https://img.shields.io/github/issues/yangjunpyo1/ai-postmortem-platform) ![GitHub last commit](https://img.shields.io/github/last-commit/yangjunpyo1/ai-postmortem-

pasted

여기서 내용 수정해야될 거 있어?

추가해야 할 것들이 있어.

주요 기능 섹션에 추가

CloudWatch 알람 발생 시 RDS 자동 장애 등록
설치 및 실행 방법에 추가

CI/CD 섹션 (GitHub Actions)
scripts/update-config.ps1 실행 방법
처리 흐름에 수정

[AWS CloudWatch] 장애 자동 감지
↓
[SNS + SQS] 메시지 유실 없이 전달
↓
[AWS Lambda] 슬랙 알림 전송 + RDS 자동 장애 등록  ← 추가
전체 수정해서 줄까?

전체수정해서 줘봐

markdown
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
- 유사 장애 자동 검색으로 반복 장애 예방
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

|
 기능 
|
 설명 
|
|
---
|
---
|
|
  장애 자동 감지 
|
 CloudWatch가 CPU, 메모리, 에러율 임계치 초과 시 자동 감지 
|
|
  장애 자동 등록 
|
 CloudWatch 알람 발생 시 RDS에 장애 자동 등록 
|
|
  심각도별 슬랙 알림 
|
 Critical / Warning / Info 단계별 알림 자동 전송 
|
|
  슬랙 대화 자동 수집 
|
 장애 종료 명령어 입력 시 대화 자동 수집 
|
|
  AI Postmortem 생성 
|
 Claude AI가 슬랙 대화 분석 후 문서 자동 생성 
|
|
  유사 장애 검색 
|
 카테고리/심각도 기반으로 과거 유사 장애 자동 매칭 
|
|
  Grafana 시각화 
|
 장애 메트릭 실시간 대시보드 
|
|
  웹 대시보드 
|
 장애 목록, 문서 조회, 통계 한눈에 확인 
|
|
  CI/CD 자동화 
|
 GitHub Actions로 Lambda/프론트엔드 자동 배포 
|

---

## 3. 시스템 아키텍처

![시스템 아키텍처](https://github.com/user-attachments/assets/d98c981e-d890-43e3-822b-15c129d1e4a3)

### 처리 흐름
[장애 발생] 서버 CPU/메모리/에러율 임계치 초과
↓
[AWS CloudWatch] 장애 자동 감지
↓
[SNS + SQS] 메시지 유실 없이 전달
↓
[AWS Lambda] 슬랙 알림 전송 + RDS 장애 자동 등록
↓
[슬랙] 엔지니어 장애 대응 대화
↓
[/resolve 명령어] 장애 종료 처리
↓
[AWS Lambda] 슬랙 대화 + CloudWatch 로그/메트릭 수집
↓
[Claude API] 슬랙 대화 분석 → Postmortem 문서 자동 생성
↓
[AWS RDS] 문서 저장
↓
[웹 대시보드] 장애 목록 / 문서 조회 / 통계


### 네트워크 구성 (VPC)
VPC (10.0.0.0/16)

Public Subnet
├── AZ-a (10.0.10.0/24) → NAT Gateway
└── AZ-c (10.0.100.0/24)

Private Subnet 1 (App Layer)
├── AZ-a (10.0.20.0/24) → Lambda(FastAPI), Lambda(알림 전송), EC2(Grafana)
└── AZ-c (10.0.120.0/24) → Lambda(Postmortem 자동화)

Private Subnet 2 (DB Layer)
├── AZ-a (10.0.30.0/24) → RDS (Primary)
└── AZ-c (10.0.130.0/24) → RDS (Standby)


세 개의 독립된 Lambda 함수로 구성되어 있습니다.

| Lambda | 트리거 | 역할 |
|---|---|---|
| `yp-lambda-fastapi` | API Gateway | 웹 대시보드용 REST API (FastAPI + Mangum) |
| `yp-lambda-alarm` | SQS (SNS 경유) | CloudWatch 알람을 심각도별 슬랙 메시지 전송 + RDS 장애 자동 등록 |
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

### 2) Terraform Remote Backend 사전 준비

Terraform state를 S3에 저장합니다. 최초 1회만 수행합니다.

```bash
aws s3api create-bucket --bucket yp-terraform-state-{계정ID} --region ap-northeast-2 --create-bucket-configuration LocationConstraint=ap-northeast-2
aws s3api put-bucket-versioning --bucket yp-terraform-state-{계정ID} --versioning-configuration Status=Enabled
aws dynamodb create-table --table-name yp-terraform-lock --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --billing-mode PAY_PER_REQUEST --region ap-northeast-2
```

`terraform/backend.tf`에 버킷 이름을 입력합니다.

```hcl
terraform {
  backend "s3" {
    bucket         = "yp-terraform-state-{계정ID}"
    key            = "ai-postmortem-platform/terraform.tfstate"
    region         = "ap-northeast-2"
    dynamodb_table = "yp-terraform-lock"
    encrypt        = true
  }
}
```

### 3) 인프라 배포 (Terraform)

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

VPC, RDS(MySQL), Lambda 3종, API Gateway, SNS/SQS, CloudWatch 알람, EC2(Grafana)가 생성됩니다.
실행 전 `terraform.tfvars`에 필요한 값을 채워야 합니다 (아래 [환경변수 설정](#6-환경변수-설정) 참고).

### 4) config.json 업데이트 및 프론트엔드 배포

```bash
# API Gateway URL을 config.json에 자동 반영 후 S3 업로드
.\scripts\update-config.ps1
```

또는 GitHub Actions에서 Deploy Frontend → Run workflow 버튼을 클릭하면 자동으로 처리됩니다.

### 5) 백엔드 설정

```bash
cd backend
pip install -r requirements.txt
```

`.env` 파일을 생성한 뒤(아래 환경변수 참고), DB 마이그레이션을 적용합니다.

```bash
alembic upgrade head
```

### 6) Slack 앱 연동

1. Slack API 사이트에서 앱을 생성하고 Bot Token(`xoxb-...`)을 발급받습니다.
2. Event Subscriptions Request URL: `{API Gateway 주소}/slack/events`
3. Slash Command `/resolve` 등록, Request URL: `{API Gateway 주소}/slack/commands`
4. Bot Token Scopes에 `channels:history`, `channels:read`, `chat:write`, `commands`, `users:read` 추가
5. 발급받은 토큰/채널 ID를 `terraform.tfvars`에 입력 후 재배포합니다.

### 7) CI/CD 설정 (GitHub Actions)

GitHub 저장소 Settings → Secrets and variables → Actions에서 다음 시크릿을 등록합니다.

| Secret | 설명 |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS IAM 사용자 액세스 키 |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM 사용자 시크릿 키 |

등록 후 코드를 push하면 자동으로 배포됩니다.
- `backend/app/**` 또는 `lambda/postmortem/**` 변경 시 → Lambda 자동 배포
- `frontend/**` 변경 시 → 프론트엔드 자동 빌드 + S3 배포 + CloudFront 캐시 무효화

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

### `frontend/.env.production`

```env
REACT_APP_API_URL=https://{API_GATEWAY_ID}.execute-api.ap-northeast-2.amazonaws.com/dev
```

> 참고: 프론트엔드는 런타임에 `/config.json`에서 API URL을 동적으로 읽어옵니다. `scripts/update-config.ps1` 실행 또는 GitHub Actions Deploy Frontend 워크플로우를 통해 자동 업데이트됩니다.

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

---

## 7. 시연 시나리오

1. 서버 CPU 90% 초과 장애 발생
   └── 테스트: CloudWatch Alarm 강제 트리거

2. CloudWatch 자동 감지
   └── 설정된 임계치 초과 시 SNS 발행

3. 슬랙으로 🔴 Critical 알림 수신 + RDS 자동 장애 등록
   └── SQS → Lambda → 슬랙 채널 알림 전송 + incidents 테이블 자동 등록

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
| 수동 배포 | GitHub Actions CI/CD 자동 배포 |

---

## 9. 폴더 구조
ai-postmortem-platform/
├── docs/ # 설계 문서
│ ├── 01_기획서.md
│ ├── 02_요구사항정의서.md
│ ├── 03_ERD.md
│ ├── 04_API명세서.md
│ ├── 05_기술스택.md
│ └── 06_시스템아키텍처.md
├── backend/ # FastAPI 백엔드 (Lambda 배포)
│ ├── app/
│ │ ├── api/ # 라우터 (auth, incidents, postmortems, similar, statistics, slack)
│ │ ├── models/ # SQLAlchemy 모델
│ │ ├── schemas/ # Pydantic 스키마
│ │ └── core/ # 설정, 보안(JWT/bcrypt)
│ └── alembic/ # DB 마이그레이션
├── lambda/ # 알림/Postmortem 자동화 Lambda
│ ├── alarm/ # CloudWatch 알람 → 슬랙 알림 + RDS 자동 장애 등록
│ └── postmortem/ # 슬랙 대화 수집 → Claude API → RDS 저장
├── frontend/ # React 대시보드
│ └── src/
│ ├── pages/ # Dashboard, IncidentList, PostmortemDetail, Statistics 등
│ ├── components/ # Layout, SeverityBadge, StatusBadge 등 공통 컴포넌트
│ └── api/ # axios 클라이언트 (동적 API URL 로드)
├── scripts/ # 유틸리티 스크립트
│ └── update-config.ps1 # terraform output → config.json 자동 업데이트 및 S3 업로드
├── .github/
│ └── workflows/
│ ├── deploy-lambda.yml # Lambda CI/CD
│ └── deploy-frontend.yml # 프론트엔드 CI/CD
└── terraform/ # 인프라 코드 (VPC, RDS, Lambda, API Gateway, CloudWatch, EC2 등)


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
VSCode에서 README.md 열어서 전체 교체하고 저장해봐.



이 채팅은 이미지 100개 제한에 도달했습니다(PDF 페이지 포함). 더 추가하려면 새 채팅을 시작하세요.




Claude는 AI이며 실수할 수 있습니다. 응답을 다시 한번 확인해 주세요.
붙여넣은 내용
11.45 KB •332줄
원본과 형식이 일치하지 않을 수 있습니다
#  AI 기반 장애 Postmortem 자동화 플랫폼 ![GitHub stars](https://img.shields.io/github/stars/yangjunpyo1/ai-postmortem-platform)![GitHub issues](https://img.shields.io/github/issues/yangjunpyo1/ai-postmortem-platform)![GitHub last commit](https://img.shields.io/github/last-commit/yangjunpyo1/ai-postmortem-platform) > 슬랙 대화를 AI가 분석하여 Postmortem 문서를 자동으로 생성하는 경량 자동화 플랫폼 --- ## 1. 프로젝트 소개 슬랙 대화를 Claude AI가 분석하여Postmortem 문서를 자동으로 생성하고웹 대시보드에서 장애 히스토리를체계적으로 관리할 수 있는경량 자동화 플랫폼입니다. ### 목표- AWS CloudWatch로 장애 자동 감지- 심각도별 슬랙 알림으로 불필요한 온콜 호출 최소화- 장애 종료 시 슬랙 대화 자동 수집- Claude AI가 Postmortem 문서 자동 생성- 유사 장애 자동 검색으로 반복 장애 예방- Grafana로 장애 메트릭 시각화- 웹 대시보드에서 장애 히스토리 조회/관리- Terraform IaC로 누구든 동일한 환경 즉시 구축 ### 프로젝트 선택 이유 인프라 구축 및 실습 과정에서 트러블슈팅이 발생할 때마다원인과 해결 과정을 수동으로 정리해야 하는 불편함을 직접 경험했습니다.기업 엔지니어들도 서비스 장애 시 동일한 과정을 반복해야 한다는 점에서AI를 활용한 자동화의 필요성을 느껴 이 프로젝트를 시작했습니다. --- ## 2. 주요 기능 | 기능 | 설명 ||---|---||  장애 자동 감지 | CloudWatch가 CPU, 메모리, 에러율 임계치 초과 시 자동 감지 ||  심각도별 슬랙 알림 | Critical / Warning / Info 단계별 알림 자동 전송 ||  슬랙 대화 자동 수집 | 장애 종료 명령어 입력 시 대화 자동 수집 ||  AI Postmortem 생성 | Claude AI가 슬랙 대화 분석 후 문서 자동 생성 ||  유사 장애 검색 | 카테고리/심각도 기반으로 과거 유사 장애 자동 매칭 ||  Grafana 시각화 | 장애 메트릭 실시간 대시보드 ||  웹 대시보드 | 장애 목록, 문서 조회, 통계 한눈에 확인 | --- ## 3. 시스템 아키텍처 ![시스템 아키텍처](https://github.com/user-attachments/assets/d98c981e-d890-43e3-822b-15c129d1e4a3) ### 처리 흐름 ```[장애 발생] 서버 CPU/메모리/에러율 임계치 초과↓[AWS CloudWatch] 장애 자동 감지↓[SNS + SQS] 메시지 유실 없이 전달↓[AWS Lambda] 슬랙 알림 전송 + 대화 수집↓[Claude API] 슬랙 대화 분석 → Postmortem 문서 자동 생성↓[AWS RDS] 문서 저장↓[웹 대시보드] 장애 목록 / 문서 조회 / 통계``` ### 네트워크 구성 (VPC) ```VPC (10.0.0.0/16) Public Subnet
Claude에 연결할 수 없습니다. 네트워크 연결을 확인하고 다시 시도해 주세요.
