enum ClickType {
    BLANK,
    EDGE,
    NODE,
    ABILITY,
}

enum PlayerStateEnum {
    ABILITY_SELECTION,
    ABILITY_WAITING,
    START_SELECTION,
    START_WAITING,
    PLAY,
    ELIMINATED,
    VICTORY,
    LOSER
}

export { ClickType, PlayerStateEnum };
