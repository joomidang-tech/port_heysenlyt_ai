"""VersionPort — 버전을 알려주는 약속. 의존성 0 (표준 라이브러리만).

이 값이 없으면 프로덕트팀이 주문에 "무엇으로 만들었는지"를 남길 수 없다
(없는 값을 지어낼 수 없음 — 규약서 04).

계보: v1.2.0 워크오더 "커널 버전 코드 소유·도장 자동 연동"(2026-07-20)의 일반화.
  - 주문 데이터에 찍는 도장 세트 = model(버전) · mode(생성 방식) · released_at
  - 버전의 진실은 문서(MODEL_VERSIONS.md류)가 아니라 **코드가 들고 다닌다**
    — 코드가 반영되는 순간 도장이 자동으로 따라와, "문서만 갱신되고 도장은
    옛값" 어긋남 창(window)이 구조적으로 사라진다.
  - ⛔ 구조 제약(고정): 이 값은 **무거운 커널 본체를 import하지 않고** 읽혀야
    한다 — 백필 등 standalone 스크립트가 도장 세트만 싸게 가져가는 경로.
    (구현체는 manifest/registry 같은 가벼운 메타만 읽을 것)

도장 3필드 매핑: model = VersionInfo.model_id · released_at = VersionInfo.released_at ·
mode(생성 방식)는 호출별 값이라 RecipePort.generate 반환의 result.mode가 정본.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from heysenlyt_ai_port.dto.params import VersionInfo


class VersionPort(ABC):
    """버전을 알려주는 방법 — 연구소가 상속해 구현한다."""

    @abstractmethod
    def get_version(self) -> VersionInfo:
        ...
