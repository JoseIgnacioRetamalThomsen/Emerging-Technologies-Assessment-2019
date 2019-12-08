var baseUrl = 'http://192.168.43.57:5000/'
var radius = 5;
var colour = '#000000';
var background = 'white'
var canvasSize = {
    width: 800,
    height: 200,
}
var canvasId = 'canvas';

var canvasBox = document.getElementById('canvas_container');
var canvas = document.createElement("canvas");

canvas.width = canvasSize.width;
canvas.height = canvasSize.height;
canvas.id = canvasId;
canvas.style.backgroundColor = background;
canvasBox.appendChild(canvas);
if (typeof G_vmlCanvasManager != 'undefined') {
    canvas = G_vmlCanvasManager.initElement(canvas);
}

ctx = canvas.getContext("2d");

//keep track last circle drawed position.
var x, y, lastX, lastY;

canvas.space = radius / 2;
//position of canvas for calulate offset
var canvasPosition = {
    x: canvas.offsetLeft,
    y: canvas.offsetTop
}

//Draw circle on the position x,y with radio r and color.
ctx.drawCircle = function (x, y, r, color) {

    this.fillStyle = color;
    this.beginPath();
    this.moveTo(x, y);
    this.arc(x, y, r, 0, Math.PI * 2, false);
    this.fill();
};

function sendImage(){
    // we send image after each up or touch end
    var img = canvas.toDataURL('image/png');
    var url = baseUrl + 'imgs';
    $.ajax({
        url: url,
        data: img,
        contentType: 'data:image/png;base64',
        type: 'POST',
        success: function (response) {
            console.log("no error")
            console.log(response);
        },
        error: function (error) {
            console.log("error")
            console.log(error);
        }
    });
}

function requestClear(){

    var url = baseUrl + 'clear'
    $.ajax({
        url: url,
        type: 'POST',
        success: function (response) {
            console.log("no error")
            console.log(response);
        },
        error: function (error) {
            console.log("error")
            console.log(error);
        }
    });
}

$("#canvas").mousedown(function (e) {
    canvas.isDrawing = true;
    //get mouase position relative to canvas
    lastX = e.pageX - canvasPosition.x;
    lastY = e.pageY - canvasPosition.y;
    //Draw first circle
    ctx.drawCircle(lastX, lastY, radius, colour);
});

canvas.addEventListener("touchstart", function (e) {
    if (e.target == canvas) {
        e.preventDefault();
    }
    canvas.isDrawing = true;
    var touch = e.touches[0];
    lastX = touch.clientX - canvasPosition.x;
    lastY = touch.clientY - canvasPosition.y;

    //Draw first circle
    ctx.drawCircle(lastX, lastY, radius, colour);
}, false);

$(canvas).on('mousemove ', function (e) {
    //only draw after mouse is down
    if (canvas.isDrawing) {

        canvasPosition.x = canvas.offsetLeft;
        canvasPosition.y = canvas.offsetTop;

        //get actual x and y position of mouse or touch
        x = e.pageX - canvasPosition.x;
        y = e.pageY - canvasPosition.y;

        //   var fillColor = colour;
        ctx.drawCircle(x, y, radius, colour);

        //distance beetwen this and last draw
        var distance = Math.sqrt(Math.pow((lastX - x), 2) + Math.pow(lastY - y, 2));

        // if the distance is bigger than the radius we will draw a line between the 2 points.
        if (distance > canvas.space) {
            ctx.beginPath();
            ctx.moveTo(lastX, lastY);
            ctx.lineWidth = radius * 2;
            ctx.lineTo(x, y);

            ctx.stroke();
        }
        // save position for next iteration      
        lastX = x;
        lastY = y;
    }
});

canvas.addEventListener("touchmove", function (e) {
    if (e.target == canvas) {
        e.preventDefault();
    }
    if (canvas.isDrawing) {
        canvasPosition.x = canvas.offsetLeft;
        canvasPosition.y = canvas.offsetTop;

        var touch = e.touches[0];

        x = touch.clientX - canvasPosition.x;
        y = touch.clientY - canvasPosition.y;
        //   var fillColor = colour;
        ctx.drawCircle(x, y, radius, colour);

        //distance beetwen this and last draw
        var distance = Math.sqrt(Math.pow((lastX - x), 2) + Math.pow(lastY - y, 2));

        // if the distance is bigger than the radius we will draw a line between the 2 points.
        if (distance > canvas.space) {
            ctx.beginPath();
            ctx.moveTo(lastX, lastY);
            ctx.lineWidth = radius * 2;
            ctx.lineTo(x, y);

            ctx.stroke();
        }
        // save position for next iteration      
        lastX = x;
        lastY = y;
    }
}, false);

//end drawing
$(canvas).on('mouseup ', function (e) {
    canvas.isDrawing = false;
    sendImage();

});

canvas.addEventListener("touchend", function (e) {
    if (e.target == canvas) {
        e.preventDefault();
    }
    canvas.isDrawing = false;
    sendImage();
}, false);

$(canvas).on('mouseleave ', function (e){
    canvas.isDrawing = false;
    //sendImage();
});

canvas.addEventListener("touchleave", function (e) {
    if (e.target == canvas) {
        e.preventDefault();
    }
    canvas.isDrawing = false;
    //sendImage();
}, false);

$("#clearButton").click(function () {

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    requestClear();
});

$("#processButton").click(function () {
    var url = baseUrl + 'imgs';
    $('#spi').removeClass('invisible');
    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
            // make spiner not visible and result visible
            $('#spi').addClass('invisible');
            $('#prediction').removeClass('invisible');
            // show prediction
            $('#prediction').html(response);
        },
        error: function (error) {
            console.log(error);
        }
    });
});

$('#formControlRange').on('input change', function (e) {
    console.log($(this).val());
    radius = parseInt($(this).val());
});

