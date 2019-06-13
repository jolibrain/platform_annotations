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

        if (this.options.includeImages) {
            await results.forEachAsync(async (assetMetadata) => {
                const arrayBuffer = await HtmlFileReader.getAssetArray(assetMetadata.asset);
                await axios.post(
                  this.options.filebrowserPath + assetMetadata.asset.name,
                  Buffer.from(arrayBuffer)
                );
            });
        }

        const exportObject = { ...this.project };
        exportObject.assets = _.keyBy(results, (assetMetadata) => assetMetadata.asset.id) as any;

        // We don't need these fields in the export JSON
        delete exportObject.sourceConnection;
        delete exportObject.targetConnection;
        delete exportObject.exportFormat;

        const fileName = `${this.project.name.replace(/\s/g, "-")}${constants.exportFileExtension}`;
        const resultPostJson = await axios.post(
          this.options.filebrowserPath + fileName,
          JSON.stringify(exportObject, null, 4)
        );
    }

    public async exportClassification(): Promise<void> {
        const results = await this.getAssetsForExport();

        const exportObject = { ...this.project };
        exportObject.assets = _.keyBy(results, (assetMetadata) => assetMetadata.asset.id) as any;

        // We don't need these fields in the export JSON
        delete exportObject.sourceConnection;
        delete exportObject.targetConnection;
        delete exportObject.exportFormat;

        const fileName = `${this.project.name.replace(/\s/g, "-")}${constants.exportFileExtension}`;
        const resultPostJson = await axios.post(
          this.options.filebrowserPath + fileName,
          JSON.stringify(exportObject, null, 4)
        );
        const projectItems = [];
        const response = await axios.post(
          `/annotation_tasks/classification_task`,
          {
            targetDir: this.options.containerName,
            items: projectItems
          }
        );
    }
}
