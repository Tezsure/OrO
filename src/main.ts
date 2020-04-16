import { createLogger, transports } from 'winston';
import { Oracle } from './controllers/oracle';
import { EndPointReader } from './controllers/endPointReader';
import { ContractHandler } from './controllers/contractHandler';
import * as config from '../oro-config.json';

const logger = createLogger({
  transports: [
    new transports.Console(),
    new transports.File ({ filename: 'oracle.log' })
  ]
});

const endPointReader = new EndPointReader(logger);
const contractHandler = new ContractHandler(logger, config.tezosConfig);
const oracle = new Oracle(config.oracleConfig, config.oracleInterval, logger, endPointReader, contractHandler);
oracle.run();


let exitHandler = function(options, exitCode){
  oracle.stop();
  if (exitCode || exitCode === 0) logger.info(exitCode);
  if (options.exit) process.exit();
};
exitHandler = exitHandler.bind(this);

//do something when app is closing
process.on('exit', exitHandler.bind(this,{cleanup:true}));

//catches ctrl+c event
process.on('SIGINT', exitHandler.bind(this, {exit:true}));

// catches "kill pid" (for example: nodemon restart)
process.on('SIGUSR1', exitHandler.bind(this, {exit:true}));
process.on('SIGUSR2', exitHandler.bind(this, {exit:true}));

//catches uncaught exceptions
process.on('uncaughtException', exitHandler.bind(this, {exit:true}));
