import winston from 'winston';
import * as request from 'request-promise';

export class EndPointReader {
    constructor(private _logger: winston.Logger) {}

    async fetchDataPoint(endPoint) {
        const options = {
            method: 'GET',
            uri: endPoint,
            json: true
        };
    
        try {
            const response = await request(options);
            this._logger.info(`Data received from endPoint ${endPoint}`);
            this._logger.info(response);
            return response;
        } catch(error) {
            this._logger.error(`Error occured while fetching endpoint ${endPoint}: ${error}`);
        }
    }
}