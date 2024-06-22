enum ClickType {
    BLANK,
    EDGE,
    NODE,
    ABILITY,
}

enum PlayerStateEnum {
    WAITING = 1,
    START_SELECTION,
    START_WAITING,
    PLAY,
    ELIMINATED,
    VICTORY,
    LOSER
}

export { ClickType, PlayerStateEnum };
