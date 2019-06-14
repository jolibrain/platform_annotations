import _ from "lodash";
import axios from "axios";
import { ExportProvider } from "./exportProvider";
import { IProject, IExportProviderOptions } from "../../models/applicationState";
import Guard from "../../common/guard";
import { constants } from "../../common/constants";
import HtmlFileReader from "../../common/htmlFileReader";

/**
 * Deepdetect Export Provider options
 */
export interface IDeepdetectExportProviderOptions extends IExportProviderOptions {
    /** Filebrowser path */
    filebrowserPath: string;
    /** Whether or not to include binary assets in target connection */
  includeImages: boolean;
  asset: any;
  regions: any[];
}

/**
 * @name - DeepDetect Export Provider
 * @description - Exports a project into a DeepDetect server
 */
export class DeepdetectExportProvider extends ExportProvider<IDeepdetectExportProviderOptions> {
    constructor(project: IProject, options: IDeepdetectExportProviderOptions) {
        super(project, options);
        Guard.null(options);
    }

    /**
     * Export project to VoTT JSON format
     */
    public async export(): Promise<void> {
        const results = await this.getAssetsForExport();
        const providerOptions = JSON.parse(JSON.stringify(this.project.targetConnection.providerOptions))

        const exportUrl = `annotation_tasks/${providerOptions.modeltype}_task`;
        const projectItems = [
          {
            filename: this.options.asset.name,
            classname: this.options.regions[0].tags[0]
          }
        ];

        const response = await axios.post(
          exportUrl,
          {
            targetDir: providerOptions.containerName,
            items: projectItems
          }
        );
    }

}
