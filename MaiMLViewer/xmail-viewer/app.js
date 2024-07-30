'use strict';

const express = require('express');
const hbs = require('hbs');
const path = require('path');
const favicon = require('serve-favicon');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
var logger = require('./common/log-utils.js');

const xmail_list = require('./routes/xmail-list');
const xmail_petrinet = require('./routes/xmail-petrinet');
const xmail_node = require('./routes/xmail-node');
const xmail_edit = require('./routes/xmail-edit');

const app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));   // テンプレートレンダリングのディレクトリ
app.set('view engine', 'hbs');                     // .hbsの拡張子は省略可能
hbs.registerPartials(path.join(__dirname, 'views/partials'));   // html header,navigatorを定義（header.hbs）

app.use(favicon(path.join(__dirname, 'views/img/favicon.ico')));
app.use(logger.connect);

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ limit: '10mb', extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(
	'/assets/vendor/bootstrap/js',
	express.static(
		path.join(__dirname, 'node_modules', 'bootstrap', 'dist', 'js')
	)
);
app.use(
	'/assets/vendor/bootstrap/css',
	express.static(path.join(__dirname, 'minty'))
);
app.use(
	'/assets/vendor/jquery',
	express.static(path.join(__dirname, 'node_modules', 'jquery'))
);
app.use(
	'/assets/vendor/popper.js',
	express.static(path.join(__dirname, 'node_modules', 'popper.js', 'dist'))
);
app.use(
	'/assets/vendor/feather-icons',
	express.static(
		path.join(__dirname, 'node_modules', 'feather-icons', 'dist')
	)
);
app.use(
	'/assets/vendor/bootstrap/css',
	express.static(path.join(__dirname, 'minty'))
);

// views components setup
app.use('/views/css', express.static(path.join(__dirname, 'views', 'css')));
app.use('/views/js', express.static(path.join(__dirname, 'views', 'js')));
app.use('/views/img', express.static(path.join(__dirname, 'views', 'img')));

// router setup
app.use('/', xmail_list);
app.use('/petrinet', xmail_petrinet);
app.use('/node', xmail_node);
app.use('/node-edit', xmail_edit);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
	var err = new Error('Not Found');
	err.status = 404;
	logger.app.error('express:' + err.message);
	next(err);
});

// error handler
app.use(function(err, req, res, next) {
	// set locals, only providing error in development
	res.locals.message = err.message;
	logger.app.error('express:' + err.message);

	res.locals.error = req.app.get('env') === 'development' ? err : {};

	// render the error page
	res.status(err.status || 500);
	res.render('error');

	return next;
});

module.exports = app;
