const ENV_CONFIG = {
    disableContextMenu: import.meta.env.VITE_DISABLE_CONTEXT_MENU === "true",
    gameBackend: import.meta.env.VITE_GAME_BACKEND,
    userBackend: import.meta.env.VITE_USER_BACKEND,
};

export default ENV_CONFIG;
