const ENV_CONFIG = {
    disableContextMenu: import.meta.env.VITE_DISABLE_CONTEXT_MENU === "true",
    gameBackend: import.meta.env.VITE_GAME_BACKEND,
    userBackend: import.meta.env.VITE_USER_BACKEND,
};
<<<<<<< HEAD
console.log(import.meta.env.VITE_DISABLE_CONTEXT_MENU);
console.log(import.meta.env.VITE_GAME_BACKEND);
export default ENV_CONFIG;

=======

export default ENV_CONFIG;
>>>>>>> acf985c70c1da2c5bfb50053298cc3cf2ae95fb2
