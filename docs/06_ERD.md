# 📋 ERD (Entity Relationship Diagram)

## 1. 테이블 목록

- users (사용자)
- incidents (장애)
- postmortems (포스트모템 문서)
- slack_messages (슬랙 대화 원본)

---

## 2. 테이블 상세

### 2-1. users (사용자)

| 컬럼명 | 타입 | 설명 |
|---|---|---|
| id | INT (PK) | 사용자 고유 ID |
| email | VARCHAR(255) | 이메일 (로그인 ID) |
| password | VARCHAR(255) | 비밀번호 (암호화) |
| name | VARCHAR(100) | 이름 |
| created_at | DATETIME | 가입일 |
| updated_at | DATETIME | 수정일 |

---

### 2-2. incidents (장애)

| 컬럼명 | 타입 | 설명 |
|---|---|---|
| id | INT (PK) | 장애 고유 ID |
| user_id | INT (FK) | 담당자 (users.id 참조) |
| title | VARCHAR(255) | 장애 제목 |
| severity | ENUM | 심각도 (critical/warning/info) |
| category | ENUM | 카테고리 (db/network/server/application/etc) |
| status | ENUM | 상태 (ongoing/resolved) |
| started_at | DATETIME | 장애 발생 시각 |
| resolved_at | DATETIME | 장애 종료 시각 |
| downtime | INT | 총 다운타임 (분) |
| affected_scope | TEXT | 영향 범위 |
| slack_channel_id | VARCHAR(255) | 슬랙 채널 ID |
| created_at | DATETIME | 생성일 |
| updated_at | DATETIME | 수정일 |

---

### 2-3. postmortems (포스트모템 문서)

| 컬럼명 | 타입 | 설명 |
|---|---|---|
| id | INT (PK) | 문서 고유 ID |
| incident_id | INT (FK) | 장애 ID (incidents.id 참조) |
| summary | TEXT | 장애 요약 |
| timeline | TEXT | 타임라인 |
| root_cause | TEXT | 근본 원인 분석 |
| resolution | TEXT | 해결 방법 |
| prevention | TEXT | 재발 방지 대책 |
| similar_incidents | TEXT | 유사 장애 히스토리 참고 |
| is_ai_generated | BOOLEAN | AI 자동 생성 여부 |
| created_at | DATETIME | 생성일 |
| updated_at | DATETIME | 수정일 |

---

### 2-4. slack_messages (슬랙 대화 원본)

| 컬럼명 | 타입 | 설명 |
|---|---|---|
| id | INT (PK) | 메시지 고유 ID |
| incident_id | INT (FK) | 장애 ID (incidents.id 참조) |
| user_name | VARCHAR(255) | 슬랙 사용자 이름 |
| message | TEXT | 메시지 내용 |
| sent_at | DATETIME | 메시지 전송 시각 |
| created_at | DATETIME | 저장일 |

---

## 3. 테이블 관계

users
└── 1 : N → incidents (한 사용자가 여러 장애 담당)

incidents
├── 1 : 1 → postmortems (장애 하나에 문서 하나)
└── 1 : N → slack_messages (장애 하나에 슬랙 메시지 여러 개)

---

## 4. ERD 다이어그램

users
│
│ 1:N
▼
incidents ──── 1:1 ────▶ postmortems
│
│ 1:N
▼
slack_messages
