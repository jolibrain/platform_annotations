import { ToolbarItem } from "./toolbarItem";
import { toast } from "react-toastify";

/**
 * @name - Save Project inside deepdetect platform
 * @description - Toolbar item to save current project
 */
export class SaveDeepDetect extends ToolbarItem {
    protected onItemClick = async () => {
        try {
            await this.props.actions.saveDeepDetect(this.props.project);
            toast.success(`${this.props.project.name} saved successfully on DeepDetect platform!`);
        } catch (e) {
            toast.error(`Error saving ${this.props.project.name}`);
        }
    }
}
