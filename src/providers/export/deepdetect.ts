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
  fileContent?: string;
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

        const providerOptions = JSON.parse(JSON.stringify(
            this.project.targetConnection.providerOptions));

        switch (providerOptions.modelType) {
          case "classification":
            await this.exportClassification(providerOptions.containerName, this.options);
            break;
          case "detection":
            await this.exportDetection(providerOptions.containerName, this.options);
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

      let item = {
        filename: options.asset.name,
        content: null,
        classname: options.regions[0].tags[0]
      };

      if(item.filename.indexOf('#t=') !== -1) {
        const [ basename, timestamp ] = item.filename.split('#t=');
        item.filename = `${parseInt(timestamp)}_${basename}`;
      }

      if(this.options.fileContent) {
        item.content = options.fileContent;
        item.filename = item.filename.substr(0, item.filename.lastIndexOf(".")) + ".jpg";
      }

      // Append / path suffix if missing
      if(!containerName.endsWith('/')) {
        containerName += '/';
      }

      // Remove / path prefix
      // platform_annotations_backend uses python3
      // os.path.join() method will not join path starting with a /
      if(containerName.startsWith('/')) {
        containerName = containerName.substring(1);
      }

      // project name must be used in targetted dir path
      // in order to use the same image path in various projects
      let projectName = ""
      if(
        this.assetService &&
        this.assetService.project &&
        this.assetService.project.name ) {
        projectName = this.assetService.project.name;
      }

      await axios.post(
        'tasks/classification',
        {
          targetDir: containerName,
          projectName: projectName,
          item: item
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

      let item = {
        filename: options.asset.name,
        content: null,
        regions: options.regions.map(r => {

          const classname = r.tags[0];
          let class_number = null;

          if(
            this.project &&
              this.project.tags &&
              this.project.tags.length > 0
          ) {
            const tagNames = this.project.tags.map(t => t.name);

            if(tagNames.indexOf(classname) !== -1) {

              // tags do not include classname "none"
              // and so they should begin at index = 1
              class_number = tagNames.indexOf(classname) + 1;

            }
          }

          let region = {
            class_number: class_number,
            classname: classname,
            xmin: parseInt(r.points[0].x),
            ymin: parseInt(r.points[0].y),
            xmax: parseInt(r.points[2].x),
            ymax: parseInt(r.points[2].y)
          }

          return region;
        })
      };

      if(item.filename.indexOf('#t=') !== -1) {
        const [ basename, timestamp ] = item.filename.split('#t=');
        item.filename = `${parseInt(timestamp)}_${basename}`;
      }

      if(this.options.fileContent) {
        item.content = options.fileContent;
        item.filename = item.filename.substr(0, item.filename.lastIndexOf(".")) + ".jpg";
      }

      // Append / path suffix if missing
      if(!containerName.endsWith('/')) {
        containerName += '/';
      }

      // Remove / path prefix
      // platform_annotations_backend uses python3
      // os.path.join() method will not join path starting with a /
      if(containerName.startsWith('/')) {
        containerName = containerName.substring(1);
      }

      // project name must be used in targetted dir path
      // in order to use the same image path in various projects
      let projectName = ""
      if(
        this.assetService &&
        this.assetService.project &&
        this.assetService.project.name ) {
        projectName = this.assetService.project.name;
      }

      let tags = [];
      if(
        this.assetService &&
        this.assetService.project &&
        this.assetService.project.tags &&
        this.assetService.project.tags.length > 0) {
        tags = this.assetService.project.tags.map(t => t.name)
      }

      await axios.post(
        'tasks/detection',
        {
          targetDir: containerName,
          projectName: projectName,
          item: item,
          tags: tags
        }
      );
    }

}
