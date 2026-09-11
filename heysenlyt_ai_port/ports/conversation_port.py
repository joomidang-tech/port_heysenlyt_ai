"""ConversationPort — 대화 한 턴의 약속. 의존성 0.

기준 = heysenlyt v1.2.0 `POST /api/chat`: 매장 채팅은 ①첫 인사(kickoff) ②턴 반복
(손님 발화→AI 응답 + 칩 + readiness) 이 전부다. readiness가 서면 취향 축이 제출되고,
실제 확정(제조/조향)은 별도 레시피 호출이 맡는다(대화는 축까지, 레시피는 배합).
상태(대화 기록)는 서버가 history로 보관·회송한다 — RecipePort.prior와 같은 왕복 규약.
도메인(식향/향장향)은 어댑터 인스턴스로 나뉜다.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from heysenlyt_ai_port.dto.params import ConversationParam
from heysenlyt_ai_port.ports.recipe_port import LlmPort


class ConversationPort(ABC):
    """대화 함수의 약속 — 반환 = ConverseReply.to_dict():
    {"reply": AI 발화, "keywords": 폐기(항상 []), "done": readiness 제출됨,
     "result": done일 때 취향 축 페이로드|None, "history": 갱신된 기록}.
    history 통째가 다음 요청의 history. 재진입·llm 인자 주입 불변식은 RecipePort와 동일.
    """

    @abstractmethod
    def converse(self, request: ConversationParam, llm: LlmPort | None = None) -> dict[str, Any]:
        ...
