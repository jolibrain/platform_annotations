import axios from "axios";
import { IAsset, AssetType, StorageType} from "../../models/applicationState";
import { IAssetProvider } from "./assetProviderFactory";
import { AssetService } from "../../services/assetService";
import Guard from "../../common/guard";
import { createQueryString } from "../../common/utils";
import * as path from 'path';

/**
 * Options for Web AutoIndex JSON
 * @member containerName - remote url
 */
export interface IWebAutoIndexJsonOptions {
    containerName: string;
}

/**
 * Asset Provider for Web AutoIndex JSON
 */
export class WebAutoIndexJson implements IAssetProvider {

    /**
     * Storage type
     * @returns - StorageType.Cloud
     */
    public storageType: StorageType = StorageType.Cloud;

  private readPath: string = "/data";
  private writePath: string = "/filebrowser/api/resource";

    constructor(private options: IWebAutoIndexJsonOptions) {
        Guard.null(options);
    }

    /**
     * Reads text from specified blob
     * @param blobName - Name of blob in container
     */
    public async readText(blobName: string): Promise<string> {
      const response = await axios.get(path.join(this.readPath, this.options.containerName, blobName))
      return response.data;
    }

    /**
     * Reads Buffer from specified blob
     * @param blobName - Name of blob in container
     */
    public async readBinary(blobName: string) {
        const text = await this.readText(blobName);
        return Buffer.from(text);
    }

    /**
     * Writes text to blob in container
     * @param blobName - Name of blob in container
     * @param content - Content to write to blob (string or Buffer)
     */
    public async writeText(blobName: string, content: string | Buffer) {
      await axios.post(path.join(this.writePath, this.options.containerName, blobName), content)
    }

    /**
     * Writes buffer to blob in container
     * @param blobName - Name of blob in container
     * @param content - Buffer to write to blob
     */
    public writeBinary(blobName: string, content: Buffer) {
        return this.writeText(blobName, content);
    }

    /**
     * Deletes file from container
     * @param blobName - Name of blob in container
     */
    public async deleteFile(blobName: string): Promise<void> {
        throw new Error("Method deleteFile not implemented.");
    }

    /**
     * Lists files in container
     * @param path - Container path
     * @param ext - Extension of files to filter on when retrieving files
     * from container
     */
    public async listFiles(containerPath: string, ext?: string): Promise<string[]> {

      if(!containerPath)
        return null;

      const response = await axios.get(path.join(this.readPath, containerPath));

      let items = response.data;

      if(ext && ext.length > 0) {
        items = items.filter(f => f.indexOf(ext) > -1);
      }

      items = items.map(f => path.join(this.readPath, containerPath, f.name));

      return items
    }

    /**
     * Lists the containers
     * @param path
     */
    public async listContainers(path: string) {
        const result: string[] = [];
        return result;
    }

    /**
     * Creates container
     * @param containerName -
     */
    public async createContainer(containerName: string): Promise<void> {
        throw new Error("Method createContainer not implemented.");
    }

    /**
     * Deletes container
     * @param containerName -
     */
    public async deleteContainer(containerName: string): Promise<void> {
        throw new Error("Method deleteContainer not implemented.");
    }


    /**
     * Retrieves assets from Web AutoIndex JSON based on options provided
     */
    public async getAssets(): Promise<IAsset[]> {
      const response = await axios.get(path.join(this.readPath, this.options.containerName));

      const items = response.data
      .filter(f => f.type === 'file')
      .map(f => {
        return {
          filename: f.name,
          path: path.join(window.location.origin, this.readPath, this.options.containerName, f.name)
        }
      });

      return items
      .map(f => AssetService.createAssetFromFilePath(f.path, f.filename))
      .filter((asset) => asset.type !== AssetType.Unknown);
    }

}
