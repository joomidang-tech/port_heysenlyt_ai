"""입력·버전 DTO — 계약이 주고받는 값 봉투. 의존성 0 (표준 라이브러리만).

기준 = heysenlyt v1.2.0 AI 코드의 실제 I/O:
  - 레시피: 조향(문장→노트선정→rule 포지셔닝) / 식향(대화축→expo 생성형).
  - 대화: `POST /api/chat`의 ChatRequestBody (mode·lang·demographics·history·userMessage·kickoff).
응답 DTO(RecipeReply·ConverseReply)는 dto/replies.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Demographics:
    """손님 인구통계 — v1.2.0 대화가 톤·추천에 반영하던 값 (선택)."""

    gender: str = ""  # "male" | "female" | "" (미지정)
    age: int = 0  # 0 = 미지정


@dataclass(frozen=True)
class RecipeParam:
    """한 번의 레시피 요청. 불변(frozen) — 요청 객체 재사용이 안전하다.

    prompt : 자연어 요청(백지 생성). 손님 피드백은 여기가 아니라 RegenerateParam.feedback.
             조향=한 문장(예 "제주 서귀포 해수욕장의 향"), 식향=취향 축 요약(scene/mood/taste).
    mode   : 도메인 내 방식. 조향 "rule"(v1.2.0 기본) / 식향 "generative"(expo, v1.2.0 기본).
             None이면 도메인 기본값.
    lang   : 결과 텍스트 언어 ("ko"|"en"|"ja"|"vi"). 비-ko는 ko 병기(직원 주문 읽기 P0).
    params : 방식 파라미터 오버라이드. 조향 {complexity, ratio} / 식향 {} / 공통 {temperature}.
             어댑터 허용목록 밖 키는 거부된다(비용·통제 이탈 차단).

    ⛔ prior 필드는 없다 — 재조향은 이 DTO 가 아니라 **RegenerateParam** 이다(계약상 별개 동작).
       nullable prior 로 두 동작을 한 타입에 얹으면 "무엇이 지배하나"가 타입에서 사라진다.
    """

    prompt: str
    mode: str | None = None
    lang: str = "ko"
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RegenerateParam:
    """재조향 한 번 — 손님이 결과를 맡아보고 "이렇게 바꿔줘"를 넣은 상황.

    generate 와 **별개 동작**이라 별개 DTO 로 둔다. 두 동작의 차이는 prior 유무가 아니라
    **무엇이 결과를 지배하느냐**다:

      generate    : prompt 가 지배. 백지에서 만든다.
      regenerate  : feedback 이 지배. prior 는 "직전엔 이랬다"는 **참고 맥락일 뿐 픽스가 아니다**
                    — 결과가 prior 와 크게 달라지는 것이 정상이고, 그래야 맞다.

    이 구분이 기획 결정(2026-08-14 D1 "B 방식")이다. 미세조정(A′ — prior 를 base 로 깔고
    비율만 만지는 쪽)은 **기각됐다.** 어댑터가 그 둘을 헷갈리지 않도록 계약 표면에서 갈라 둔다.

    feedback : 손님이 적은 수정 방향. 예 "덜 우디하게" / "잔향을 더 진하게" (≤300자, 화면 규칙)
    prior    : 직전 generate/regenerate 가 돌려준 dict 그대로. 참고 맥락.
               ⛔ 상태는 어댑터가 아니라 호출자(서버)가 보관한다 — 재진입 안전의 전제.
    mode/lang/params : RecipeParam 과 같은 의미.
    """

    feedback: str
    prior: dict[str, Any]
    mode: str | None = None
    lang: str = "ko"
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ConversationParam:
    """대화 한 턴 — v1.2.0 `POST /api/chat` ChatRequestBody 대응.

    message=None + kickoff=True 이면 대화 시작(AI 선 발화·첫 질문).
    상태(대화 기록)는 호출자(서버)가 history로 보관·회송한다 — RecipePort.prior와 같은 왕복 규약.
    """

    domain: str  # "fragrance"(향장향) | "flavor"(식향)
    message: str | None = None  # 손님 발화(userMessage). None+kickoff=첫 발화 요청
    history: tuple[tuple[str, str], ...] = ()  # ((role, content), ...) role: "user"|"assistant"
    lang: str = "ko"  # "ko"|"en"|"ja"|"vi"
    demographics: Demographics | None = None
    kickoff: bool = False  # 첫 턴 AI 선 발화
    # 식향 전용(v1.2.0 §E) — 클라가 지난 턴 자기 제출 축을 회송(통합코드는 판정 않고 에코).
    last_known_axes: dict[str, str] | None = None
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VersionInfo:
    """AI 세대 버전 — 주문 도장(kernelVersion)의 출처. 도장 3필드 = model·mode·released_at.

    계보: v1.2.0 워크오더 "커널 버전 코드 소유"(2026-07-20) — 버전의 진실은 문서가 아니라
    코드가 들고 다닌다. lib/expo/stamp.ts(EXPO_STAMP·FRAGRANCE_STAMP)의 일반화.
    """

    model_id: str  # 예 "fragrance-rule" — 도장의 model 축 근원
    domain: str  # "fragrance" | "flavor"
    version: str  # "1.0.0"
    spec: str = ""  # 대상 기기 스펙 (예 "senlyt-shop"/"expo") — 비면 미지정
    notes: str = ""  # 체인지로그 한 줄
    # ⚠️ 신규 필드는 항상 끝에 추가 — 위치인자 소비자가 있어도 계약이 안 깨지게
    released_at: str = ""  # 그 세대가 나온 날 (도장의 released_at)
    model_type: str = ""  # "llm-pipeline"
