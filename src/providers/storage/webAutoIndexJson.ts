import axios from "axios";
import { IAsset, AssetType, StorageType} from "../../models/applicationState";
import { IAssetProvider } from "./assetProviderFactory";
import { AssetService } from "../../services/assetService";
import Guard from "../../common/guard";
import { createQueryString } from "../../common/utils";
import * as path from 'path';


/**
 * Options for Web AutoIndex JSON
 * @member removeUrl - remote url
 */
export interface IWebAutoIndexJsonOptions {
    remoteUrl: string;
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

    constructor(private options: IWebAutoIndexJsonOptions) {
        Guard.null(options);
    }

    /**
     * Reads text from specified blob
     * @param blobName - Name of blob in container
     */
    public async readText(blobName: string): Promise<string> {
      const response = await axios.get(path.join(this.options.remoteUrl, blobName))
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
      await axios.post(path.join(this.options.remoteUrl, blobName), content)
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
        throw new Error("Method not implemented.");
    }

    /**
     * Lists files in container
     * @param path - NOT USED IN CURRENT IMPLEMENTATION. Only uses container
     * as specified in Azure Cloud Storage Options. Included to satisfy
     * Storage Provider interface
     * @param ext - Extension of files to filter on when retrieving files
     * from container
     */
    public async listFiles(path: string, ext?: string): Promise<string[]> {
        throw new Error("Method not implemented.");
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
        throw new Error("Method not implemented.");
    }

    /**
     * Deletes container
     * @param containerName -
     */
    public async deleteContainer(containerName: string): Promise<void> {
        throw new Error("Method not implemented.");
    }


    /**
     * Retrieves assets from Web AutoIndex JSON based on options provided
     */
    public async getAssets(): Promise<IAsset[]> {
        const response = await axios.get(this.options.remoteUrl);

      const items = response.data
      .filter(f => f.tupe === 'file')
      .map(f => path.join(this.options.remoteUrl, f.name));

      console.log(items);

        return items
            .map((filePath) => AssetService.createAssetFromFilePath(filePath))
            .filter((asset) => asset.type !== AssetType.Unknown);
    }

}
