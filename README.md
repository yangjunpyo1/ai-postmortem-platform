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

| 기능 | 설명 |
|---|---|
|  장애 자동 감지 | CloudWatch가 CPU, 메모리, 에러율 임계치 초과 시 자동 감지 |
|  장애 자동 등록 | CloudWatch 알람 발생 시 RDS에 장애 자동 등록 |
|  심각도별 슬랙 알림 | Critical / Warning / Info 단계별 알림 자동 전송 |
|  슬랙 대화 자동 수집 | 장애 종료 명령어 입력 시 대화 자동 수집 |
|  AI Postmortem 생성 | Claude AI가 슬랙 대화 분석 후 문서 자동 생성 |
|  유사 장애 검색 | 카테고리/심각도 기반으로 과거 유사 장애 자동 매칭 |
|  Grafana 시각화 | 장애 메트릭 실시간 대시보드 |
|  웹 대시보드 | 장애 목록, 문서 조회, 통계 한눈에 확인 |
|  CI/CD 자동화 | GitHub Actions로 Lambda/프론트엔드 자동 배포 |

---

## 3. 시스템 아키텍처

![시스템 아키텍처](https://github.com/user-attachments/assets/d98c981e-d890-43e3-822b-15c129d1e4a3)

### 처리 흐름
