function setFormatter() {
    numericFormatter();
    decimalFormatter();
    alphaNumericFormatter();
    alphaNumericMarkFormatter();
    dateFormatter();
    zenkakuFormatter();
}

function numericFormatter() {
    $('.numeric').on({
        'paste': function(e) {
            e.preventDefault();
        },
        'keypress': function(e) {
            st = String.fromCharCode(e.which);
            if ("0123456789-\b\r\t".indexOf(st,0) < 0) return false;
            return true;
        }
    });
    
    $('.numeric').attr({
        autocomplete: 'off'
        
    }).css({
        'ime-mode': 'disabled',
        'text-align': 'right'
        
    });
}

function decimalFormatter() {
    $('.decimal').on({
        'paste': function(e) {
            e.preventDefault();
        },
        'keypress': function(e) {
            st = String.fromCharCode(e.which);
            if ("0123456789-.\b\r\t".indexOf(st,0) < 0) return false;
            return true;
        }
    });
    
    $('.decimal').attr({
        autocomplete: 'off'
        
    }).css({
        'ime-mode': 'disabled',
        'text-align': 'right'
    });
}

function alphaNumericMarkFormatter() {
    $('.anm').on({
        'paste': function(e) {
            e.preventDefault();
        },
        'keypress': function(e) {
            st = String.fromCharCode(e.which);
            if ("!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ ".indexOf(st,0) < 0) return false;
            return true;
        }
    });
    
    $('.anm').attr({
        autocomplete: 'off'
        
    }).css({
        'ime-mode': 'disabled',
        'text-align': 'left'
    });
}

function alphaNumericFormatter() {
    $('.an').on({
        'paste': function(e) {
            e.preventDefault();
        },
        'keypress': function(e) {
            st = String.fromCharCode(e.which);
            if ("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ".indexOf(st,0) < 0) return false;
            return true;
        }
    });
    
    $('.an').attr({
        autocomplete: 'off'
        
    }).css({
        'ime-mode': 'disabled',
        'text-align': 'left'
    });
}

function zenkakuFormatter() {
    $('.zenkaku').on({
        'paste': function(e) {
            e.preventDefault();
        }
    });
    
    $('.zenkaku').attr({
        autocomplete: 'off'
        
    }).css({
        'ime-mode': 'disabled',
        'text-align': 'left'
    });
}

function dateFormatter() {
    $('.dte').on({
        'paste': function(e) {
            e.preventDefault();
        }
    });
    
    $('.dte').attr({
        autocomplete: 'off'
        
    }).css({
        'ime-mode': 'disabled',
        'text-align': 'right'
    });
}

function comma3 ( num ) {
    if (num == null) {return '';}
    return num.toString().replace(/^(-?[0-9]+)(?=\.|$)/, function(s){ return s.replace(/([0-9]+?)(?=(?:[0-9]{3})+$)/g, '$1,');});
}

function replaceSlashOfYearMonth(){
    var valYearMonth = $('#monthpicker').val();
    var sendValue = valYearMonth.replace("/", "");
    return sendValue;
}

function getCurrentYearMonth() {
	var now = new Date();
	var yearMonth = "" + now.getFullYear() + "/" +  padZero(now.getMonth() + 1);
	return yearMonth;
}

function padZero(num) {
	var result;
	if (num < 10) {
		result = "0" + num;
	} else {
		result = "" + num;
	}
	return result;
}

function getCurrentYearMonth() {
    var now = new Date();
    var yearMonth = "" + now.getFullYear() + "/" +  padZero(now.getMonth() + 1);
    return yearMonth;
}


function getLastYearMonth() {
    var now = new Date();
    var yearMonth = "" + now.getFullYear() + "/" +  padZero(now.getMonth());
    return yearMonth;
}
