'use strict';

var log4js = require('log4js');
var logger = exports = module.exports = {};

log4js.configure({
	appenders: { 
		app: { type: 'file', filename: './logs/app.log' },
		access: { type: 'file', filename: './logs/access.log' } 
	},
	categories: { 
		default: { appenders: ['app'], level: 'debug' } ,
		access: { appenders: ['access'], level: 'debug' }
	}
});

logger.app = log4js.getLogger('app');
logger.access = log4js.getLogger('access');
logger.connect = log4js.connectLogger(logger.access);
