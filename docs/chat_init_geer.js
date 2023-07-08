
var yw_div = document.createElement('div');
var yw_chat_window = null;
var yw_mask = null;
var yw_isDown = false;
document.body.appendChild(yw_div);
var w_inner_w = window.innerWidth;
var w_inner_h = window.innerHeight;
var entrancePositionArray = ['', 'left:' + entrancePositionConfigVO_transverse + 'px; top:' + entrancePositionConfigVO_longitudinal + 'px;', 'right:' + entrancePositionConfigVO_transverse + 'px; top:' + entrancePositionConfigVO_longitudinal + 'px;', 'left:' + entrancePositionConfigVO_transverse + 'px; top:' + (w_inner_h / 2 + entrancePositionConfigVO_longitudinal) + 'px;', 'right:' + entrancePositionConfigVO_transverse + 'px; top:' + (w_inner_h / 2 + entrancePositionConfigVO_longitudinal) + 'px;', 'left:' + entrancePositionConfigVO_transverse + 'px; bottom:' + entrancePositionConfigVO_longitudinal + 'px;', 'right:' + entrancePositionConfigVO_transverse + 'px; bottom:' + entrancePositionConfigVO_longitudinal + 'px;'];
var textLength = entranceStyleConfigVO_buttonText.length * 20;
var entranceStyleTypeArray = ['', {
    outerStyle: 'width:35px;background:' + entranceStyleConfigVO_buttonColor + ';',
    imgStyle: 'width:35px;',
    textStyle: 'width: 13px;padding: 10px;word-break: break-all;text-align: center;display: inline-block;font-size: 14px;color:' + entranceStyleConfigVO_textColor + ';'
},
    {
        outerStyle: 'height: 35px;line-height: 35px;background:' + entranceStyleConfigVO_buttonColor + ';',
        imgStyle: 'height: 30px;vertical-align: middle;',
        textStyle: 'padding-right:5px;color:' + entranceStyleConfigVO_textColor + ';'
    },
    {
        outerStyle: 'width:' + textLength + 'px;height:' + textLength + 'px;line-height:' + textLength + 'px;text-align:center;border-radius:50%;background:' + entranceStyleConfigVO_buttonColor + ';',
        imgStyle: 'display:none;',
        textStyle: 'color:' + entranceStyleConfigVO_textColor + ';'
    },
    {
        outerStyle: '',
        imgStyle: 'display:none;',
        textStyle: 'color:' + entranceStyleConfigVO_textColor + ';'
    }];
var yw_html = '';
if (entranceStyleConfigVO_type == 1) {
    yw_html = "<div style='position:fixed; width:75px; height:75px; z-index:99999;" + entrancePositionArray[entrancePositionConfigVO_position] + "visibility:visible; border: 0px;' class='iyunwen_js_class'>" + "<a id='yw_link' href='javascript:;' target='blank'><img id='yw_icon' style='border:none;' width='100%'/></a></div>";
} else {
    yw_html = "<div style='position:fixed; z-index:99999;" + entranceStyleTypeArray[entranceStyleConfigVO_style].outerStyle + entrancePositionArray[entrancePositionConfigVO_position] + "' class='iyunwen_js_class'>" + "<a id='yw_link' href='javascript:;' style='text-decoration: none;' target='blank'><img id='yw_icon' style='" + entranceStyleTypeArray[entranceStyleConfigVO_style].imgStyle + "'/><span id='yw_text' style='" + entranceStyleTypeArray[entranceStyleConfigVO_style].textStyle + "'></span></a></div>";
}
yw_div.outerHTML = yw_html;

var yw_icon = document.getElementById('yw_icon');
changeImg();
var changeImgTimer;
if(changeImgTimer){
    clearInterval(changeImgTimer);
}
changeImgTimer = setInterval(function(){
    changeImg();
},10000);

var yw_text = document.getElementById('yw_text');
if (yw_text) {
    yw_text.innerText = entranceStyleConfigVO_buttonText;
}
var yw_link = document.getElementById('yw_link');
function createChatwindowCommon (width, height) {
    yw_chat_window = document.getElementById('yw_chat_window');
    if (yw_chat_window) {
        if (yw_mask.style.display === 'block') {
            yw_mask.style.display = 'none';
        } else {
            yw_mask.style.display = 'block';
        }
    } else {
        yw_mask = document.createElement('div');
        document.body.appendChild(yw_mask);
        yw_mask.outerHTML = '<div id="yw_chat_mask" style="position: fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.3);z-index:1000;"></div>';
        yw_mask = document.getElementById('yw_chat_mask');
        yw_chat_window = document.createElement('div');
        var windowHtml = "<div id='yw_chat_window' style='overflow: hidden;display:block;position:absolute;width:" + width + "px;height:" + height + "px;z-index:1001;top:0;left:0;right:0;bottom:0;margin:auto;box-shadow:0 0 10px #aaa;'></div>";
        var banner = document.createElement('div');
        var bannerHtml = '<div id="yw_chat_banner" style="z-index: 100;position:absolute;top:0;left:0;height:20px;width:100%;background: #cacaca;">' + '<span id="yw_chat_close" style="position:absolute;top:0;right:0;height:20px;line-height:20px;width:25px;font-size:12px;color:#000;text-align: center;cursor: pointer;background:#eee;">x<span>' + '<div>';
        var iframe = document.createElement('iframe');
        var iframeHtml = "<iframe style='width:100%;height:680px;position:absolute;bottom:0;left:0;border:none;' src='" + chat_window_url + "'></iframe>";
        yw_mask.appendChild(yw_chat_window);
        yw_chat_window.outerHTML = windowHtml;
        yw_chat_window = document.getElementById('yw_chat_window');
        yw_chat_window.appendChild(banner);
        banner.outerHTML = bannerHtml;
        yw_chat_window.appendChild(iframe);
        iframe.outerHTML = iframeHtml;
        var yw_chat_close = document.getElementById('yw_chat_close');
        yw_chat_close.addEventListener('click',
            function () {
                yw_mask.style.display = 'none';
            });
    }
};
function changeImg(){
    if(yw_icon.src && yw_icon.src.indexOf("ing.png") != -1){
        clearInterval(changeImgTimer);
    }

    var domain = chat_window_url.split("/")[0]+"//"+chat_window_url.split("/")[2];
    var url = domain+"/admin/geer/getNewsImg";

    if(adNum && employeeID){
        url = url+"?adNum="+adNum+"&employeeID="+employeeID;
    }else if(adNum && !employeeID){
        url = url+"?adNum="+adNum;
    }else if(!adNum && employeeID){
        url = url+"?employeeID="+employeeID;
    }

    var xhr = new XMLHttpRequest();
    xhr.open("GET",url,true);
    xhr.onload=function(e){
        if(xhr.readyState === 4){
            if(xhr.status === 200){
                console.log(xhr.responseText);
                var rest = JSON.parse(xhr.responseText);
                if(rest.code == 1){
                    yw_icon.src=rest.data.img;
                }
            }else{
                console.error(xhr.statusText);
                yw_icon.src = entranceStyleConfigVO_picUrl;
            }
        }
    };
    xhr.onerror = function(e){
        console.error(xhr.statusText);
        yw_icon.src=entranceStyleConfigVO_picUrl;
    };
    xhr.send(null);
};
function createChatwindow3 (width, height) {
    yw_chat_window = document.getElementById('yw_chat_window');
    var dec = '';
    var dis = 0;
    if (entrancePositionConfigVO_position === 1 || entrancePositionConfigVO_position === 3 || entrancePositionConfigVO_position === 5) {
        dec = 'left';
        dis = entrancePositionConfigVO_transverse + 75;
    } else {
        dec = 'right';
        dis = entrancePositionConfigVO_transverse + 75;
    }
    if (yw_chat_window) {
        if (yw_chat_window.style.width === (width + 'px')) {
            yw_chat_window.style.width = '0';
        } else {
            yw_chat_window.style.width = width + 'px';
        }

    } else {
        yw_chat_window = document.createElement('div');
        var windowHtml = "<div id='yw_chat_window' style='overflow:hidden;" + dec + ':' + dis + "px;transition:width 0.3s;display:block;position:fixed;width:0;height:" + height + "px;top:" + ((w_inner_h - height) / 2) + "px;z-index:1000;box-shadow:0 0 10px #aaa;border-radius: 8px;'></div>";
        var banner = document.createElement('div');
        var bannerHtml = '<div id="yw_chat_banner" style="position:absolute;top:0;left:0;height:20px;width:100%;background: #45B035;cursor: move;">' + '<span id="yw_chat_close" style="position:absolute;top:0px;right:0px;height:20px;z-index:99;line-height:20px;width:25px;font-size:24px;color:#fff;text-align: center;cursor: pointer;background:#45B035;">x<span>' + '<div>';
        var iframe = document.createElement('iframe');
        var iframeHtml = "<iframe style='width:100%;height:" + (height - 20) + "px;position:absolute;bottom:0;left:0;border:none;' src='" + chat_window_url + "'></iframe>";
        var iframeCover = document.createElement('div');
        var iframeCoverHtml = '<div id="yw_iframe_cover" style="display:none;position: absolute;top: 20px;left: 0;width: 100%;height: calc(100% - 20px);"><div>';
        document.body.appendChild(yw_chat_window);
        yw_chat_window.outerHTML = windowHtml;
        yw_chat_window = document.getElementById('yw_chat_window');
        yw_chat_window.appendChild(banner);
        banner.outerHTML = bannerHtml;
        yw_chat_window.appendChild(iframe);
        iframe.outerHTML = iframeHtml;
        yw_chat_window.appendChild(iframeCover);
        iframeCover.outerHTML = iframeCoverHtml;
        var yw_chat_close = document.getElementById('yw_chat_close');
        yw_chat_close.addEventListener('click',
            function () {
                document.onmousemove = null;
                document.onmouseup = null;
                yw_chat_window.style.width = '0';
            });
        setTimeout(function () {
                yw_chat_window.style.width = width + 'px';
            },
            20);
        addMoveEvent();
    }
};
function addMoveEvent () {
    var box = document.getElementById('yw_chat_banner');
    var windowa = document.getElementById('yw_chat_window');
    var iframCover = document.getElementById('yw_iframe_cover');

    box.onmousedown = function (ev) {
        var clearSlct = "getSelection" in window ? function(){
            window.getSelection().removeAllRanges();
        }:function(){
            document.selection.empty();
        };
        clearSlct();

        iframCover.style.display = "block";

        let e = ev || event;
        let x = e.clientX - windowa.offsetLeft;
        let y = e.clientY - windowa.offsetTop;
        let bodyScreenX = "";
        let bodyClientWidth = document.documentElement.clientWidth;
        let bodyClientHeight = document.documentElement.clientHeight;

        document.onmousemove = function (ev) {
            let e = ev || event;
            windowa.style.left = ev.clientX - x + 'px';
            windowa.style.top = ev.clientY - y + 'px';

            bodyScreenX = ev.screenX;
        };

        document.onmouseup = function (ev) {
            iframCover.style.display = "none";
            if (ev.clientY - y<0) {
                windowa.style.top = 0;
            } else if (ev.clientY - y + 20 > bodyClientHeight) {
                windowa.style.top = (bodyClientHeight - 20) + 'px';
            } else if (ev.clientX - x < 0) {
                windowa.style.left = 0;
            }
            document.onmousemove = null;
            document.onmouseup = null;
        };
    };
};
switch (windowStyleConfigVO_type) {
    case 1:
    case 2:
        yw_link.href = chat_window_url;
        break;
    case 3:
        var clickFlag = true;
        var boxHeight = window.screen.height > 768 ? 680 : 620;
        yw_link.addEventListener('click',
            function (e) {
                e.preventDefault();
                if(!clickFlag){
                    return false;
                }
                createChatwindow3( 800, boxHeight);
            });

        var yw_icon = document.getElementById('yw_icon');
        var iyunwen_js_class = document.getElementsByClassName('iyunwen_js_class')[0];
        yw_icon.onmousedown = function (ev) {
            ev.preventDefault();
            clickFlag=false;
            var clearSlct = "getSelection" in window ? function(){
                window.getSelection().removeAllRanges();
            }:function(){
                document.selection.empty();
            };
            clearSlct();
            let e = ev || event;
            let x1 = e.clientX;
            let y1 = e.clientY;
            let y = e.clientY - iyunwen_js_class.offsetTop;
            let bodyScreenX = "";
            let bodyClientHeight = "";

            document.onmousemove = function (ev) {
                let e = ev || event;
                iyunwen_js_class.style.top = ev.clientY - y + 'px';

                bodyScreenX = ev.screenX;
                bodyClientHeight = document.documentElement.clientHeight;
            };
            document.onmouseup = function (ev) {
                let x2 = ev.clientX;
                let y2 = ev.clientY;
                if(Math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))<5){
                    clickFlag = true;
                }

                if(!clickFlag){
                    if(ev.clientY - y < 0){
                        iyunwen_js_class.style.top = 0;
                    }else if(ev.clientY - y + 75 > bodyClientHeight){
                        iyunwen_js_class.style.top = (bodyClientHeight-75)+"px";
                    }
                }

                document.onmousemove = null;
                document.onmouseup = null;
            };
        };
        break;
    case 4:
        yw_link.addEventListener('click',
            function (e) {
                e.preventDefault();
                createChatwindowCommon(850, 700);
            });
        break;
    default:
        break;
}
window.closeYWChatWindow = function () {
    if (windowStyleConfigVO_type === 5) {
        yw_chat_window.style.right = '-400px';
        setTimeout(function () {
                document.body.removeChild(document.getElementById('yw_chat_window'));
            },
            300);
    } else {
        document.body.removeChild(document.getElementById('yw_chat_window'));
    }
}