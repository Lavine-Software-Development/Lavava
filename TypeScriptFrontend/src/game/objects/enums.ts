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

enum GameStateEnum {
    LOBBY = 1,
    BUILDING_GAME,
    START_SELECTION,
    PLAY,
    END_GAME,
    GAME_OVER
}

export { ClickType, PlayerStateEnum, GameStateEnum };
