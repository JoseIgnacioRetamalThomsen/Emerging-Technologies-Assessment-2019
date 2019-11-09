//get canvas from DOM
var canvas = document.getElementById("inputCanvas");

//size of the canvas
var canvasSize = {
    width: 260,
    height: 260,

}

//position of canvas for calulate offset
var canvasPosition = {
    x: canvas.offsetLeft,
    y: canvas.offsetTop
}

//radius of the circvle for drawing
var radius = 15;
//colour for drawing
var colour = '#000000';

//change size of canvas.
canvas.width = canvasSize.width;
canvas.height = canvasSize.height;



// Get a 2D context for the canvas.
var ctx = canvas.getContext("2d");

//keep track last circle drawed position.
var x, y, lastX, lastY;

//min space between circles.
// if space is larger a line will be draw.
canvas.space = radius / 2;

//Draw circle on the position x,y with radio r and color.
ctx.drawCircle = function (x, y, r, color) {

    this.fillStyle = color;
    this.beginPath();
    this.moveTo(x, y);
    this.arc(x, y, r, 0, Math.PI * 2, false);
    this.fill();

};

//start drawing
//is mouse is down we start drawing
$(document).on('mousedown touchstart', function (e) {

 

    canvas.isDrawing = true;

    //get mouase position relative to canvas
    lastX = e.pageX - canvasPosition.x;
    lastY = e.pageY - canvasPosition.y;

    //Draw first circle
    ctx.drawCircle(lastX, lastY, radius, colour);

});

//draw
$(document).on('mousemove touchmove', function (e) {


    canvasPosition.x = canvas.offsetLeft ;
    
        canvasPosition.y= canvas.offsetTop;

    //only draw after mouse is down
    if (!canvas.isDrawing) {
        return;
    }

    //get actual x and y position of mouse or touch
    x = e.pageX - canvasPosition.x;
    y = e.pageY - canvasPosition.y;

    //   var fillColor = colour;
    ctx.drawCircle(x, y, radius, colour);

    //distance beetwen this and last draw
    var distance = Math.sqrt(Math.pow((lastX - x), 2) + Math.pow(lastY - y, 2));

    // if the distance is bigger than the radius we will draw circles between the 2 points.
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
$(document).on('mouseup touchend', function (e) {
    canvas.isDrawing = false;
});

//Clear canvas when button is tabed.
$(document).ready(function () {
    $("#clearButton").click(function () {
        console.log("Clear");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    });
});

$(document).ready(function () {
    $("#processButton").click(function () {
        /// console.log("Processing");
        var img = [];
        for (var n = 0, cc = 0; n < canvas.width; n += 10, cc++) {
            img[cc] = [];
            for (var m = 0; m < canvas.height; m += 10) {
                var iData = ctx.getImageData(m, n, 10, 10);
                var c = 0;

                for (i = 0; i < iData.data.length; i += 4) {
                    if (iData.data[i + 3] > 0) c++;
                }
                // console.log(c);
                img[cc].push(parseInt((255 * (c / 100))));
            }
        }
        //console.log(img[0].length);
        //for (var i = 0; i < 28; i++) {
        //  console.log(img[i]);
        //}
        //  console.log(img);
        /*
                        $.ajax({
                            type: 'POST',
                            url: "http://127.0.0.1:5000/",
                            contentType: 'application/json;charset=UTF-8',
                            data: { 'data': img }
                        });
        */
        img = processImage();
        console.log(img);
        $.ajax({
            url: 'http://127.0.0.1:5000/reco',
            data: JSON.stringify(img),
            contentType: 'application/json;charset=UTF-8',
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
});

function processImage(a){
    
    //declare array
    var img = [];
        for (var n = 0, cc = 0; n < canvas.width+20; n += 10, cc++) {
            //add a new row
            img[cc] = [];
            for (var m = 0; m < canvas.height+20; m += 10) {

                //get data of a 10x 10 portion wich will be 1 pixel
                var iData = ctx.getImageData(m -10 , n -10, 10, 10);
                var c = 0;

                //count total of black pixels
                for (i = 0; i < iData.data.length; i += 4) {
                    if (iData.data[i + 3] > 0) c++;
                }
                
                // add the pixel proportilan for 255
                // ex : if there was all black it will be 255
                // if was no black will be 0
                //we also add the withe margin
                if(n==0||n==0 ||m==0||m==0){
                    img[cc].push(0);
                }else{
                img[cc].push(parseInt((255 * (c / 100))));
                }
            }
        }
    return img;
}
