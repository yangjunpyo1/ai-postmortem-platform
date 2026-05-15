# 📋 API 명세서

## 공통 사항

- Base URL: `https://api.ai-postmortem.com`
- 인증 방식: JWT Token (Bearer)
- 응답 형식: JSON

---

## 1. 인증 (Auth)

### 1-1. 회원가입
| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | /api/auth/register |
| 인증 필요 | X |

요청
{
  "email": "kim@gmail.com",
  "password": "1234",
  "name": "김철수"
}

응답
{
  "message": "회원가입 성공",
  "user_id": 1
}

---

### 1-2. 로그인
| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | /api/auth/login |
| 인증 필요 | X |

요청
{
  "email": "kim@gmail.com",
  "password": "1234"
}

응답
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "name": "김철수"
}

---

### 1-3. 로그아웃
| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | /api/auth/logout |
| 인증 필요 | O |

응답
{
  "message": "로그아웃 성공"
}

---

## 2. 장애 (Incidents)

### 2-1. 장애 목록 조회
| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | /api/incidents |
| 인증 필요 | O |

쿼리 파라미터
?severity=critical     심각도 필터
?category=db           카테고리 필터
?status=resolved       상태 필터
?page=1                페이지 번호

응답
{
  "total": 10,
  "incidents": [
    {
      "id": 1,
      "title": "DB 커넥션 풀 고갈",
      "severity": "critical",
      "category": "db",
      "status": "resolved",
      "started_at": "2025-05-15 23:00:00",
      "resolved_at": "2025-05-16 00:10:00",
      "downtime": 70,
      "user_name": "김철수"
    }
  ]
}

---

### 2-2. 장애 상세 조회
| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | /api/incidents/{id} |
| 인증 필요 | O |

응답
{
  "id": 1,
  "title": "DB 커넥션 풀 고갈",
  "severity": "critical",
  "category": "db",
  "status": "resolved",
  "started_at": "2025-05-15 23:00:00",
  "resolved_at": "2025-05-16 00:10:00",
  "downtime": 70,
  "affected_scope": "API 서버 전체",
  "user_name": "김철수"
}

---

### 2-3. 장애 수동 등록
| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | /api/incidents |
| 인증 필요 | O |

요청
{
  "title": "DB 커넥션 풀 고갈",
  "severity": "critical",
  "category": "db",
  "started_at": "2025-05-15 23:00:00",
  "affected_scope": "API 서버 전체"
}

응답
{
  "message": "장애 등록 성공",
  "incident_id": 1
}

---

### 2-4. 장애 종료
| 항목 | 내용 |
|---|---|
| Method | PATCH |
| URL | /api/incidents/{id}/resolve |
| 인증 필요 | O |

응답
{
  "message": "장애 종료 처리 완료",
  "incident_id": 1,
  "downtime": 70
}

---

## 3. Postmortem 문서

### 3-1. Postmortem 조회
| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | /api/incidents/{id}/postmortem |
| 인증 필요 | O |

응답
{
  "id": 1,
  "incident_id": 1,
  "summary": "DB 커넥션 풀 고갈로 API 응답 불가",
  "timeline": "23:00 장애 발생...",
  "root_cause": "트래픽 급증으로 커넥션 풀 초과",
  "resolution": "커넥션 풀 사이즈 증가 후 재시작",
  "prevention": "자동 스케일링 정책 추가",
  "similar_incidents": "2025-03-10 유사 장애 참고",
  "is_ai_generated": true,
  "created_at": "2025-05-16 00:15:00"
}

---

### 3-2. Postmortem AI 자동 생성
| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | /api/incidents/{id}/postmortem/generate |
| 인증 필요 | O |

응답
{
  "message": "Postmortem 생성 완료",
  "postmortem_id": 1
}

---

### 3-3. Postmortem 수정
| 항목 | 내용 |
|---|---|
| Method | PUT |
| URL | /api/incidents/{id}/postmortem |
| 인증 필요 | O |

요청
{
  "summary": "수정된 요약",
  "timeline": "수정된 타임라인",
  "root_cause": "수정된 원인",
  "resolution": "수정된 해결방법",
  "prevention": "수정된 재발 방지 대책"
}

응답
{
  "message": "수정 완료",
  "postmortem_id": 1
}

---

## 4. 통계 (Statistics)

### 4-1. 장애 통계 조회
| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | /api/statistics |
| 인증 필요 | O |

응답
{
  "total_incidents": 10,
  "by_severity": {
    "critical": 3,
    "warning": 5,
    "info": 2
  },
  "by_category": {
    "db": 4,
    "network": 2,
    "server": 3,
    "application": 1
  },
  "avg_downtime": 45
}

---

## 5. 유사 장애 검색

### 5-1. 유사 장애 검색
| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | /api/incidents/{id}/similar |
| 인증 필요 | O |

응답
{
  "similar_incidents": [
    {
      "id": 3,
      "title": "DB 응답 지연",
      "category": "db",
      "started_at": "2025-03-10",
      "summary": "DB 커넥션 문제로 응답 지연"
    }
  ]
}
