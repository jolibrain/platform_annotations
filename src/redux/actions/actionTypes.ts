/**
 * Redux Action types
 */
export enum ActionTypes {
    // App
    TOGGLE_DEV_TOOLS_SUCCESS = "TOGGLE_DEV_TOOLS_SUCCESS",
    OPEN_LOCAL_FOLDER_SUCCESS = "OPEN_LOCAL_FOLDER_SUCCESS",
    REFRESH_APP_SUCCESS = "REFRESH_APP_SUCCESS",
    SAVE_APP_SETTINGS_SUCCESS = "SAVE_APP_SETTINGS_SUCCESS",
    ENSURE_SECURITY_TOKEN_SUCCESS = "ENSURE_SECURITY_TOKEN_SUCCESS",

    // Projects
    LOAD_PROJECT_SUCCESS = "LOAD_PROJECT_SUCCESS",
    SAVE_PROJECT_SUCCESS = "SAVE_PROJECT_SUCCESS",
    SAVE_DEEPDETECT_SUCCESS = "SAVE_DEEPDETECT_SUCCESS",
    DELETE_PROJECT_SUCCESS = "DELETE_PROJECT_SUCCESS",
    CLOSE_PROJECT_SUCCESS = "CLOSE_PROJECT_SUCCESS",
    LOAD_PROJECT_ASSETS_SUCCESS = "LOAD_PROJECT_ASSETS_SUCCESS",
    EXPORT_PROJECT_SUCCESS = "EXPORT_PROJECT_SUCCESS",
    UPDATE_PROJECT_TAG_SUCCESS = "UPDATE_PROJECT_TAG_SUCCESS",
    DELETE_PROJECT_TAG_SUCCESS = "DELETE_PROJECT_TAG_SUCCESS",

    // Connections
    LOAD_CONNECTION_SUCCESS = "LOAD_CONNECTION_SUCCESS",
    SAVE_CONNECTION_SUCCESS = "SAVE_CONNECTION_SUCCESS",
    DELETE_CONNECTION_SUCCESS = "DELETE_CONNECTION_SUCCESS",

    // Assets
    SAVE_ASSET_METADATA_SUCCESS = "SAVE_ASSET_METADATA_SUCCESS",
    LOAD_ASSET_METADATA_SUCCESS = "LOAD_ASSET_METADATA_SUCCESS",

    ANY_OTHER_ACTION = "ANY_OTHER_ACTION_SUCCESS",

    SHOW_ERROR= "SHOW_ERROR",
    CLEAR_ERROR = "CLEAR_ERROR",
}
