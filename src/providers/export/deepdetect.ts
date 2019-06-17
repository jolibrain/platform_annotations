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

        // FIXME: hack to fetch modelType
        // it should be available by calling directly modelTayp attribute on providerOptions
        const providerOptions = JSON.parse(JSON.stringify(this.project.targetConnection.providerOptions))

        switch(providerOptions.modelType) {
          case 'classification':
            this.exportClassification(providerOptions.containerName, this.options);
            break;
          case 'detection':
            this.exportDetection(providerOptions.containerName, this.options);
            break;
          default:
            break;
        }
    }

    private async exportClassification(containerName, options): Promise<void> {
      if(
        !options ||
        !options.asset ||
        !options.asset.name ||
        !options.regions ||
        !options.regions[0] ||
        !options.regions[0].tags ||
        !options.regions[0].tags[0]
      )
        return null;

      await axios.post(
        'tasks/classification',
        {
          targetDir: containerName,
          item:
            {
              filename: options.asset.name,
              classname: options.regions[0].tags[0]
            }
        }
      );
    }

    private async exportDetection(containerName, options): Promise<void> {
      if(
        !options ||
        !options.asset ||
        !options.asset.name ||
        !options.regions ||
        options.regions.length === 0
      )
        return null;

      await axios.post(
        'tasks/detection',
        {
          targetDir: containerName,
          item:
            {
              filename: options.asset.name,
              regions: options.regions.map(r => {
                return {
                  classname: r.tags[0],
                  xmin: parseInt(r.points[0].x),
                  ymin: parseInt(r.points[0].y),
                  xmax: parseInt(r.points[3].x),
                  ymax: parseInt(r.points[3].y)
                }
              })
            }
        }
      );
    }

}
