var baseUrl = 'http://127.0.0.1:5000/'
var radius = 5;
var colour = '#000000';
var background = 'white'
var canvasSize = {
    width: 800,
    height: 200,
}
var canvasId = 'canvas';
var chart = "";
var isFirst = 0;
var num = "";
var parent;
var charts = []

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

var queue = [];

ctx = canvas.getContext("2d");

//keep track last circle drawed position.
var x, y, lastX, lastY;

canvas.space = radius / 2;
//position of canvas for calulate offset
var canvasPosition = {
    x: canvas.offsetLeft,
    y: canvas.offsetTop
}

/**
 *  Draw circle on the position x,y with radio r and color.
 */
ctx.drawCircle = function (x, y, r, color) {

    this.fillStyle = color;
    this.beginPath();
    this.moveTo(x, y);
    this.arc(x, y, r, 0, Math.PI * 2, false);
    this.fill();
};

/**
 * Add image on cavas to queue
 */
function addToQueue() {
    queue.push(canvas.toDataURL('image/png'))
}

/**
 * Clear queue and canvas.
 */
function clear() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    queue = [];
}

/**
 * On Mouse down, start drawing.
 */
$("#canvas").mousedown(function (e) {
    canvas.isDrawing = true;
    //get mouase position relative to canvas
    lastX = e.pageX - canvasPosition.x;
    lastY = e.pageY - canvasPosition.y;
    //Draw first circle
    ctx.drawCircle(lastX, lastY, radius, colour);
});

/**
 * On touch start, startdrawing.
 */
canvas.addEventListener("touchstart", function (e) {
    // prvent other action like scrolling 
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

/**
 * Mousemove, circles are draw in every call then line is draw beetwen them.
 */
$(canvas).on('mousemove ', function (e) {
    //only draw after mouse is down
    if (canvas.isDrawing) {
        canvasPosition.x = canvas.offsetLeft;
        canvasPosition.y = canvas.offsetTop;

        //get actual x and y position of mouse or touch
        x = e.pageX - canvasPosition.x;
        y = e.pageY - canvasPosition.y;

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

/**
 * Touchmove event, draw circle every call and lines beetwen actual and last.
 */
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


/**
 * OnMouseup, stop drawind and add image on canvas to queue.
 */
$(canvas).on('mouseup ', function (e) {
    canvas.isDrawing = false;
    addToQueue();
});

/**
 * touchend event, stop drawind and add image on canvas to queue.
 */
canvas.addEventListener("touchend", function (e) {
    if (e.target == canvas) {
        e.preventDefault();
    }
    canvas.isDrawing = false;
    var img = canvas.toDataURL('image/png');
    queue.push(img)

}, false);

/**
 * OnMouseleave, stop drawing.
 */
$(canvas).on('mouseleave ', function (e) {
    canvas.isDrawing = false;
});

/**
 * touch leave event, stop drawing.
 */
canvas.addEventListener("touchleave", function (e) {
    if (e.target == canvas) {
        e.preventDefault();
    }
    canvas.isDrawing = false;
}, false);

/**
 * Clear button, crear canvas and queue.
 */
$("#clearButton").click(function () {
    clear();
});

/**
 * Process button, send img of queue, clear queue and clear canvas.
 */
$("#processButton").click(function () {
    var url = baseUrl + 'imgs';
    $('#spi').removeClass('invisible');
    var imgs = JSON.stringify(queue);
    $.ajax({
        url: url,
        data: imgs,
        contentType: 'application/json; charset=utf-8',
        type: 'POST',
        success: function (response) {
            r = JSON.parse(response)
            $('#spi').addClass('invisible');
            $('#prediction').removeClass('invisible');
            // show prediction
            $('#prediction').html(r[0]);
            diplay(r)
        },
        error: function (error) {
            console.log("error")
            console.log(error);
        }
    });
});

/**
 * Change brush radius.
 */
$('#formControlRange').on('input change', function (e) {
    radius = parseInt($(this).val());
});

//code modified from https://bensonruan.com/handwritten-digit-recognition-with-tensorflow-js/
function createChart(label, prediction) {
    var numberStr = prediction[0];
    parent = $("#result_box").children();
    for (var i = 1; i < prediction.length; i++) {
        num = numberStr[i - 1];
        parent[i - 1].width = 100;
        parent[i - 1].height = 100;
        var ctx = parent[i - 1].getContext('2d');
        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: label,
                datasets: [{
                    label: num,
                    backgroundColor: 'blue',
                    borderColor: 'black',
                    data: prediction[i][0],
                }]
            },

            // Configuration options go here
            options: {}
        });
        charts.push(chart);
    }
}


function diplay(data) {
    label = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
    if (isFirst == 0) {
        createChart(label, data);
        isFirst = 1;
    } else {
        for (var i = 0; i < charts.length; i++) {
            charts[i].destroy()
        }
        createChart(label, data);
    }
    for (var i = 0; i < parent.length; i++) {
        parent[i].style.display = "block";
    }
}

