import { ToolbarItem } from "./toolbarItem";
import { toast } from "react-toastify";

/**
 * @name - Save Project inside deepdetect platform
 * @description - Toolbar item to save current project
 */
export class SaveDeepDetect extends ToolbarItem {
    protected onItemClick = async () => {
        const infoId = toast.info(`Started export for ${this.props.project.name}...`, { autoClose: false });
        const results = await this.props.actions.saveDeepDetect(this.props.project);

        toast.dismiss(infoId);

        if (!results || (results && results.errors.length === 0)) {
            toast.success(`Export completed successfully!`);
        } else if (results && results.errors.length > 0) {
            toast.warn(`Successfully exported ${results.completed.length}/${results.count} assets`);
        }
    }
}
