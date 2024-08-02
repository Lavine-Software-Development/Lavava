const ENV_CONFIG = {
    disableContextMenu: import.meta.env.VITE_DISABLE_CONTEXT_MENU === "false",
    gameBackend: import.meta.env.VITE_GAME_BACKEND,
    userBackend: import.meta.env.VITE_USER_BACKEND,
};
console.log(ENV_CONFIG.userBackend);
console.log(ENV_CONFIG.gameBackend);
export default ENV_CONFIG;

