"""응답 DTO — 출력의 모양을 코드로 확정. 의존성 0 (표준 라이브러리만).

어댑터는 이 DTO를 만들고 `.to_dict()`로 반환한다(HTTP·저장·prior/history 회송은 JSON 여정).
모양의 진실은 이 클래스 — 신규 필드는 항상 끝에 붙인다(위치인자 하위호환).
기준 = heysenlyt v1.2.0: 대화는 SSE(token+tool)를 한 턴으로 접은 형태, 레시피는 도메인 페이로드.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RecipeReply:
    """generate 출력. to_dict() 통째가 다음 요청의 prior.

    stamp  : 도장 세트 {model, mode, released_at, kernel_version} — kernel_version 은
             `{model}+{mode}+{released_at}` 단일 문자열(v1.2.0 stampVersion 동일 형식).
    recipe : 도메인 레시피 페이로드.
             조향 = {buckets, weights, items, moves}(rule 엔진 산출)
             식향 = ExpoRecipePayload(drinkTitle·reason·families·sweetMl·sourMl·items·baseMl…)
    """

    domain: str  # "fragrance" | "flavor"
    version: str  # "1.0.0"
    stamp: dict[str, str]  # model·mode·released_at·kernel_version
    recipe: dict[str, Any]  # 도메인 레시피 페이로드
    is_valid: bool = True
    warnings: list[str] = field(default_factory=list)
    result_type: str = ""  # "module:Class" — refine prior 복원 힌트
    state: dict[str, Any] = field(default_factory=dict)  # refine 전제 상태(호출자 보관)

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


@dataclass(frozen=True)
class ConverseReply:
    """converse 출력 — v1.2.0 SSE(token·tool·done)를 한 턴 결과로 접은 형태.

    reply    : AI 발화 전체(v1.2.0 token 델타 누적분).
    keywords : suggestKeywords 칩(객관식 보기, ≤4). 빈 리스트=칩 없음.
    done     : readiness 툴이 호출됨(취향 축 제출 완료). v1.2.0 finishReason="tool" 계열.
               ⛔ done=True 여도 대화는 계속될 수 있다(더 깊어지면 갱신 재제출) — 종료가 아니라
               "지금 만들 수 있음" 신호. 실제 확정(제조/조향)은 별도 레시피 호출.
    result   : done일 때 취향 축 페이로드.
               식향 = {scene,mood,taste,drinkTitle,reason,(recipeId),(ko*)}
               향장향 = {emotion,memory,place,fragranceName,story,(ko*)}
    history  : 이번 턴 반영한 갱신 기록 — 통째가 다음 요청의 history.
    """

    reply: str
    done: bool = False
    result: dict[str, Any] | None = None
    keywords: list[str] = field(default_factory=list)
    history: list[tuple[str, str]] = field(default_factory=list)
    # 대화도 4개 독립 능력 중 하나 — 자기 버전 도장을 싣는다(어댑터가 3값 합쳐 kernel_version 제공).
    stamp: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)
