from typing import Literal, TypedDict, Optional, List, Tuple, Dict, Union

__all__ = ["CellType", "CellState", "Board", "CountInfo", "ComponentTemplate", "ComponentConfig", "CellConfig", "BoardMetadata", "U_Hint", "ClickResponse"]

class CellType(TypedDict):
    boardname: str
    x: int
    y: int

class CellState(TypedDict):
    type: CellType
    isRevealed: bool
    isLoading: bool
    hint1: bool
    hint2: bool
    error: bool
    errormine: bool

class Board(TypedDict):
    name: Optional[str]
    position: Tuple[int, int]
    showLabel: Optional[bool]
    showName: Optional[bool]
    dye: Optional[List[List[bool]]]
    mask: Optional[List[List[bool]]]
    size: Tuple[int, int]

class CountInfo(TypedDict):
    total: int
    known: Optional[int]
    unknown: int
    remains: Optional[int]

class ComponentTemplate(TypedDict):
    name: str
    value: object

class ComponentConfig(TypedDict):
    type: Literal["container", "text", "assets", "template"]
    value: Union[List['ComponentConfig'], str, ComponentTemplate]
    style: Optional[str]
    class_: Optional[str]

class CellConfig(TypedDict):
    overlayText: str
    position: CellType
    component: ComponentConfig
    highlight: Optional[Dict[str, List[CellType]]]

class BoardMetadata(TypedDict):
    rules: List[str]
    boards: Dict[str, Board]
    cells: List[CellConfig]
    count: Optional[CountInfo]
    seed: Optional[str]
    noFail: Optional[bool]
    noHint: Optional[bool]
    mode: Literal["NORMAL", "EXPERT", "ULTIMATE"]
    u_mode: Optional[List[str]]

class U_Hint(TypedDict):
    emptycount: int
    flagcount: int
    markcount: Optional[int]

class ClickResponse(TypedDict):
    success: bool
    gameover: bool
    reason: str
    cells: List[CellConfig]
    count: Optional[CountInfo]
    noFail: Optional[bool]
    noHint: Optional[bool]
    mines: Optional[List[CellType]]
    win: Optional[bool]
    u_hint: Optional[U_Hint]

class GenerateBoardResult(TypedDict):
    reason: str
    success: bool

class CreateGameParams(TypedDict):
    size: str
    rules: str
    mode: str
    total: str
    u_mode: Optional[str]
    dye: Optional[str]
    mask: Optional[str]
    seed: Optional[str]

type ResponseType[T] = T | tuple[T, int]