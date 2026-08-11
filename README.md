# interface_heysenlyt_ports

heysenlyt(프로덕트팀) ↔ SENSORIUM(연구소) 사이의 **약속만** 담는 계약 라이브러리.

- Python 패키지명: `sensorium_ports` (import 경로 불변)
- ⛔ 의존성 0 — 표준 라이브러리 외 import 금지 (AST 테스트로 강제)
- 스튜어드: 프로덕트팀 (규약서 §03 — "저희가 초안을 드립니다. 바꾸실 일 생기면 말씀만")
- 소비자: SENSORIUM(엔진이 구현) · product_heysenlyt_fastapi(서버가 호출)
