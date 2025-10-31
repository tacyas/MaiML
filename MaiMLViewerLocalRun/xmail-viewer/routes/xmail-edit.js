'use strict';

/**
 * express module
 * @const
 */
const express = require('express');
const util = require('util');
const xmail = require('../models/xmail-edit.js');
const router = express.Router();
var logger = require('../common/log-utils.js');

/**
 * ルートサービス  PNarc作成可否チェック
 * @name post/pnarc-check
 * @function
 * @memberof module:routes/xmail-pnarc-check
 * @inner
 * @param {number} src_nid - Source node id
 * @param {number} dst_nid - Destination node id
 * @param {callback} middleware - Express middleware.
 */
router.post('/pnarc-check', async (req, res, next) => {
	logger.app.debug('[router-pnarc-check]');
	xmail
		.pnarc_check(req.body.src_nid, req.body.dst_nid)
		.then(result => {
			logger.app.debug('[router-pnarc-check]' + util.inspect(result));

			res.setHeader('Content-Type', 'application/json');
			res.status(200);
			res.send(result);
		})
		.catch(error => {
			res.status(500);
			logger.app.error('[router-pnarc-check]' + error.message);
			res.send(error.message);
		});

	return next;
});

/**
 * ルートサービス  PNarc作成
 * @name post/pnarc-create
 * @function
 * @memberof module:routes/xmail-pnarc-create
 * @inner
 * @param {number} src_nid - Source node id
 * @param {number} dst_nid - Destination node id
 * @param {callback} middleware - Express middleware.
 */
router.post('/pnarc-create', async (req, res, next) => {
	logger.app.debug('[router-pnarc-create]');
	xmail
		.pnarc_create(req.body.src_nid, req.body.dst_nid)
		.then(result => {
			logger.app.debug('[router-pnarc-create]' + util.inspect(result));

			res.setHeader('Content-Type', 'application/json');
			res.status(200);
			res.send(result);
		})
		.catch(error => {
			res.status(500);
			logger.app.error('[router-pnarc-create]' + error.message);
			res.send(error.message);
		});

	return next;
});

/**
 * ルートサービス  PNarc削除
 * @name post/pnarc-delete
 * @function
 * @memberof module:routes/xmail-pnarc-delete
 * @inner
 * @param {number} src_nid - Source node id
 * @param {number} dst_nid - Destination node id
 * @param {callback} middleware - Express middleware.
 */
router.post('/pnarc-delete', async (req, res, next) => {
	logger.app.debug('[router-pnarc-delete]');
	xmail
		.pnarc_delete(req.body.src_nid, req.body.dst_nid)
		.then(result => {
			logger.app.debug('[router-pnarc-delete]' + util.inspect(result));

			res.setHeader('Content-Type', 'application/json');
			res.status(200);
			res.send(result);
		})
		.catch(error => {
			res.status(500);
			logger.app.error('[router-pnarc-delete]' + error.message);
			res.send(error.message);
		});

	return next;
});

/**
 * ルートサービス  ノード作成
 * @name post/node-creation
 * @function
 * @memberof module:routes/xmail-node-creation
 * @inner
 * @param {number} nid - Node id
 * @param {number} id - Place or transition id
 * @param {string} type - Type.
 */
router.post('/node-creation', async (req, res, next) => {
	logger.app.debug('[router-node-creation]');
	xmail
		.node_creation(req.body.nid, req.body.id, req.body.kind)
		.then(result => {
			logger.app.debug('[router-node-creation]' + util.inspect(result));

			res.setHeader('Content-Type', 'application/json');
			res.status(200);
			res.send(result);
		})
		.catch(error => {
			res.status(500);
			logger.app.error('[router-node-creation]' + error.message);
			res.send(error.message);
		});

	return next;
});

/**
 * ルートサービス  XMAIエクスポート 
 * @name post/export
 * @function
 * @memberof module:routes/xmail-export
 * @inner
 * @param {string} nid - Node id
 * @param {string} infile - existing original XMAIL
 * @param {string} outfile - exported XMAIL.
 */
router.post('/export', async (req, res, next) => {
	logger.app.debug('[router-export]');
	xmail
		.export(req.body.nid, req.body.infile, req.body.outfile)
		.then(result => {
			logger.app.debug('[router-export]' + util.inspect(result));

			res.setHeader('Content-Type', 'application/json');
			res.status(200);
			res.send(result);
		})
		.catch(error => {
			res.status(500);
			logger.app.error('[router-export]' + error.message);
			res.send(error.message);
		});

	return next;
});

module.exports = router;
