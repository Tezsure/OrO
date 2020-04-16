import winston from 'winston';
import { EndPointReader } from './endPointReader';
import { ContractHandler } from './contractHandler';

export class Oracle {
    private _taskRunnerTimeout;
    
    constructor(private _oracleConfig,
                private _oracleInterval,
                private _logger: winston.Logger,
                private _endPointReader: EndPointReader,
                private _contractHandler: ContractHandler) {
    }

    run() {
        this._logger.info('Oracle has started');
        this.runTask();
    }

    stop() {
        this._logger.info('Stopping Oracle node');
        clearTimeout(this._taskRunnerTimeout);
    }

    private async runTask() {
        this._logger.info('----- running Oracle task -----');
        for(const config of this._oracleConfig) {
            await this.processConfig(config);
        }
        this._taskRunnerTimeout = setTimeout(()=> { this.runTask();}, this._oracleInterval * 1000);
    }

    private async processConfig(config) {
        this._logger.info(`Started processing config : ${config.entryPointMichelson}`);
        try {
            let dataMichelson = await this.processEndpoint(config);
            dataMichelson = dataMichelson.replace(/'/g, '"');
            await this._contractHandler.writeToOracleContract(config.contractAddress, dataMichelson);
            this._logger.info(`Finished processing config : ${config.entryPointMichelson}`);            
        } catch(error) {
            this._logger.error(`Can not process the config : ${config.entryPointMichelson} : ${error}`);
        }
    }

    private async processEndpoint(config): Promise<string> {
        const response = await this._endPointReader.fetchDataPoint(config.endPoint);
        let entryPointMichelson = config.entryPointMichelson;

        config.fields.forEach((field) => {
            switch(field.type) {
                case 'fixed':
					entryPointMichelson = this.formatMichelson(entryPointMichelson, field.nameInEntryPoint, field.data);
                    break;
                
                case 'custom':
                    let dataToBeAdded = this.parseResponse(field.path, response);
                    if (dataToBeAdded === null || dataToBeAdded === undefined) {
                        throw Error(`failed to get data for endPoint : ${config.endPoint}`);
                    }
                    if(field.isString) {
						dataToBeAdded = (field.prefix || '') + dataToBeAdded + (field.suffix || '');
						entryPointMichelson = this.formatMichelson(entryPointMichelson, field.nameInEntryPoint, dataToBeAdded);
					} else {
						dataToBeAdded *= (field.multiplier || 1);
						if(field.doFloor) {
							dataToBeAdded = Math.floor(dataToBeAdded);
						}
						if(field.doCeil) {
							dataToBeAdded = Math.ceil(dataToBeAdded);
						}
						entryPointMichelson = this.formatMichelson(entryPointMichelson, field.nameInEntryPoint, dataToBeAdded);
					}
                    break;
            }
        });

        return entryPointMichelson;
    }
    
    private parseResponse(path, response) {
        return path.split('.').reduce(function(prev, curr) {
            return prev ? prev[curr] : null;
        }, response || self);
    }

    private formatMichelson(entryPointMichelson, nameInEntryPoint, dataToBeAdded): string{
        const parts = entryPointMichelson.split(nameInEntryPoint);
        return parts[0] + dataToBeAdded + parts[1];
    }
}