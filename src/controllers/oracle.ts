import winston from 'winston';
import { EndPointReader } from './endPointReader';
import { CityInfo } from '../models/interface';
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
        for(const cityConfig of this._oracleConfig) {
            await this.processCity(cityConfig.city, cityConfig.endPoints);
        }
        this._taskRunnerTimeout = setTimeout(()=> { this.runTask();}, this._oracleInterval * 1000);
    }

    private async processCity(city, endPoints) {
        this._logger.info(`Started processing city : ${city}`);
        try {
            let temperatureSum = 0;
            let humiditySum = 0;
            let pressureSum = 0;
            const allEndPointsResponse = await Promise.all(endPoints.map((endPointConfig) => {
                return this.processEndpoint(endPointConfig);
            }));
            (allEndPointsResponse as CityInfo[]).forEach((info: CityInfo) => {
                temperatureSum += info.temperature;
                humiditySum += info.humidity;
                pressureSum += info.pressure;
            });
            
            const temperatureAvg = Math.floor(temperatureSum / allEndPointsResponse.length);
            const pressureAvg = Math.floor(pressureSum / allEndPointsResponse.length);
            const humidityAvg = Math.floor(humiditySum / allEndPointsResponse.length);

            await this._contractHandler.writeToOracleContract(city, {
                temperature : temperatureAvg,
                pressure: pressureAvg,
                humidity: humidityAvg
            });
            this._logger.info(`Finished processing city : ${city}`);            
        } catch(error) {
            this._logger.error(`Can not process the city : ${city} : ${error}`);
        }
    }

    private async processEndpoint(endPointConfig): Promise<CityInfo> {
        const response = await this._endPointReader.fetchDataPoint(endPointConfig.link);
        let temperature = this.parseResponse(endPointConfig.temperaturePosition, response);
        const pressure = this.parseResponse(endPointConfig.pressurePosition, response);
        const humidity = this.parseResponse(endPointConfig.humidityPosition, response);
        const tempUnit = endPointConfig.tempUnit;

        if (!temperature || !pressure || !humidity) {
            throw Error(`failed to get data for endPoint : ${endPointConfig.link}`);
        }

        if (tempUnit === 'K') {
            temperature -= 273.15;
        } else if (tempUnit ==='F') {
            temperature = (((temperature-32)*5)/9);
        }

        const cityInfo = {
            temperature: temperature,
            pressure : pressure,
            humidity : humidity
        };

        return cityInfo;
    }
    
    private parseResponse(path, response) {
        return path.split('.').reduce(function(prev, curr) {
            return prev ? prev[curr] : null;
        }, response || self);
    }
}