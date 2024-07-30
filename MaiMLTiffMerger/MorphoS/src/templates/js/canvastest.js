



// testdata::{'xxxyyyP':[['XXXYYYP'],['XXXYYYP']]}
//  {a:[b,c],[d]}  ===  b+c->a->d
const testdata1 = {
    '001001':{p:'M',b:[''],a:['002001T']},
    '001002':{p:'C',b:[''],a:['002001T']},
    '002001':{p:'T',b:['001001M','001002C'],a:['003001R']},
    '003001':{p:'R',b:['002001I'],a:['']},
}

/**//**//**//**//**//**//**//**//**//*
 keyを数値で持てばソート可能になる
 Array型だと検索に時間がかかる
*//**//**//**//**//**//**//**//**//**/
/*
const testdata1 = {
    '001001M':[[''],['002001I']],
    '001002C':[[''],['002001I']],
    '002001I':[['001001M','001002C'],['003001R']],
    '003001R':[['002001I'],['']],
}
*/

const testdata2= {
    '001001M':[[''],['002001T']],
    '001002C':[[''],['002001T']],
    '002001T':[['001001M','001002C'],['003001R']],
    '003001R':[['002001T'],['004001T']],
    '003002C':[[''],['004001T']],
    '004001T':[['003001R','003002C'],['005001R','005002R']],
    '005001R':[['004001T'],['']],
    '005002R':[['004001T'],['']],
}

const testdata3= {
    '001001M':[[''],['002001T']],
    '001002C':[[''],['002001T']],
    '002001T':[['001001M','001002C'],['003001R']],
    '003001R':[['002001T'],['004001T']],
    '001003M':[[''],['002003T']],
    '001004C':[[''],['002003T']],
    '002003T':[['001003M','001004C'],['003003R']],
    '003003R':[['002003T'],['004001T']],
    '004001T':[['003001R','003003R'],['005001R']],
    '005001R':[['004001T'],['']],
}


// グローバル変数
// 図形のポジション
const positionList = []
// マス目の基準値
const n = 40
const m = 40
// 図形の半径の基準値
const r = 10

/* 線を引く */
function drawline(thiscanvas,x,y){
    var line_ctx = thiscanvas.getContext("2d");
    line_ctx.beginPath();
    // 開始位置に移動する
    //line_ctx.moveTo(20, 20);
    var lx = n*x
    var ly = n*y
    line_ctx.moveTo(lx, ly);
    // 線を引く
    const xend = lx + 80
    const yend = ly + 80
    line_ctx.lineTo(xend, yend);
    line_ctx.closePath();
    line_ctx.stroke();
    //return 
}
/* 正方形を描く */
function drawsquare(thiscanvas,x,y){
    var sq_ctx = thiscanvas.getContext("2d");
    sq_ctx.beginPath();   // 現在のパスをリセットする
    // 四角を描く（四角の左上座標を指定）
    const sx = n*x
    const sy = n*y
    sq_ctx.strokeRect(sx-r, sy-r, r*2, r*2);
    return [sx, sy]
}

/* 長方形を描く */
function drawrectangle(thiscanvas,x,y){
    var rec_ctx = thiscanvas.getContext("2d");
    rec_ctx.beginPath();   // 現在のパスをリセットする
    // 四角を描く（四角の左上座標を指定）
    const rx = n*x - r/3
    const ry = n*y + n/2 
    rec_ctx.strokeRect(rx, ry-r, r/3, r*2);
    return [rx, ry]
}

/* 五角形を描く */
function drawpentagon(thiscanvas,x,y){
    return drawcircle(thiscanvas,x,y)
}

/* 円を書く */
function drawcircle(thiscanvas,x,y){
    var cir_ctx = thiscanvas.getContext("2d");
    // 塗りつぶす色を指定する
    cir_ctx.fillStyle = 'rgb(0, 255, 0)';
    cir_ctx.beginPath();   // 現在のパスをリセットする
    // 円を描く位置を決める(円の中心を指定)
    const cx = n*x
    const cy = n*y
    cir_ctx.arc(cx, cy, r, 0, Math.PI * 2, false);
    // 実際に円を書く
    cir_ctx.fill();
    return [cx, cy]
}


window.onload = function drawpetrinetd() {

    // canvasを取得
    var ptri_canvas = document.getElementById("petri-id")
    /* 線を引く */
    //drawline(ptri_canvas)
    /* 四角を描く */
    //drawrect(ptri_canvas)
    /* 円を書く */
    //drawcircle(ptri_canvas)
    /* 五角形を書く */
    //drawpentagon(ptri_canvas)

    const drawdata = testdata1
    const keylist = Object.keys(drawdata)
    //console.log(keylist)
    for(let key in drawdata){
        const onedata = drawdata[key]
        console.log(onedata)
        var x = key.substring(0,3);
        var y = key.substring(3,6);
        console.log(x,y)
        var rp =[]
        //positionList.push({[key] :[x,y]})
        console.log(positionList)
        if(onedata.p == 'M'){
            rp = drawcircle(ptri_canvas,x,y)
        }else if(onedata.p == 'C'){
            rp = drawpentagon(ptri_canvas,x,y)
        }else if(onedata.p == 'R'){
            rp = drawsquare(ptri_canvas,x,y)
        }else if(onedata.p == 'T'){
            // transitionの図形を描く
            rp = drawrectangle(ptri_canvas,x,y)
        }
        positionList.push({[key]:{p:[onedata.p],position:[rp]}})
    }
    // arcのlineを描く
    console.log(positionList)
    //p＝Tのデータを取得
    for(let key in drawdata){
        const onedata2 = drawdata[key]

        if(onedata2.p == 'T'){
            const mae = onedata2.a
            const usiro = onedata2.b
            for(let i in mae){
                const maedata = positionList[i]
                
            }
            for(let l in usiro){
                const usirodata = positionList[l]
            }
        }
    }

 }
