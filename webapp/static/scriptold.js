//get canvas from DOM
var canvas = document.getElementById("inputCanvas");

//size of the canvas
var canvasSize = {
    width: 800,
    height: 200,
}

//position of canvas for calulate offset
var canvasPosition = {
    x: canvas.offsetLeft,
    y: canvas.offsetTop
}
//radius of the circvle for drawing
var radius = 5;
//colour for drawing
var colour = '#000000';

//change size of canvas.
canvas.width = canvasSize.width;
canvas.height = canvasSize.height;

//add on mouse over
canvas.mouseIsOver = false;

if(typeof G_vmlCanvasManager != 'undefined') {
    canvas = G_vmlCanvasManager.initElement(canvas);
  }


// Get a 2D context for the canvas.
var ctx = canvas.getContext("2d");

//keep track last circle drawed position.
var x, y, lastX, lastY;

//min space between circles.
// if space is larger a line will be draw.
canvas.space = radius / 2;

var queue = []

//Draw circle on the position x,y with radio r and color.
ctx.drawCircle = function (x, y, r, color) {

    this.fillStyle = color;
    this.beginPath();
    this.moveTo(x, y);
    this.arc(x, y, r, 0, Math.PI * 2, false);
    this.fill();
};

canvas.addEventListener("touchstart", function (e) {
    if (e.target == canvas) {
        e.preventDefault();
    }
    
},false);
canvas.addEventListener("touchmove", function (e) {
    if (e.target == canvas) {
        e.preventDefault();
    }
   
    
}, false);

$(document).ready(function () {
    //start drawing
    //is mouse is down we start drawing
    $(canvas).on('mousedown', function (e) {
        canvas.isDrawing = true;
        //get mouase position relative to canvas
        lastX = e.pageX - canvasPosition.x;
        lastY = e.pageY - canvasPosition.y;
        //Draw first circle
        ctx.drawCircle(lastX, lastY, radius, colour);
    });



/*
$(canvas).on('touchstart', function (e) {
        if (e.target == canvas) {
            e.preventDefault();
        }
        alert("tart");
        canvas.isDrawing = true;
        var touch = e.touches[0];
        //get mouase position relative to canvas
        lastX = touch.clientX - canvasPosition.x;
        lastY = touch.clientY - canvasPosition.y;
        //Draw first circle
        ctx.drawCircle(lastX, lastY, radius, colour);
    });
*/
    //draw
    $(canvas).on('mousemove ', function (e) {

        
        //only draw after mouse is down
        if (!canvas.isDrawing) {
            return;
        }
        
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
    });



    //end drawing
    $(canvas).on('mouseup ', function (e) {
        canvas.isDrawing = false;


        // we send image after each up or touch end
        var img = canvas.toDataURL('image/png');
        $.ajax({
            url: 'http://127.0.0.1:5000/imgs',
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

    });

    //Clear canvas when button is tabed.
    $("#clearButton").click(function () {

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        $.ajax({
            url: 'http://127.0.0.1:5000/clear',
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
    });

    $("#processButton").click(function () {
        $('#spi').removeClass('invisible');
        $.ajax({
            url: 'http://127.0.0.1:5000/imgs',
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

});

