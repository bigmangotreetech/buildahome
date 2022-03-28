const { PDFDocument, StandardFonts, rgb } = PDFLib

$(document).ready(function () {
  if ($('#canvas').length)
    initialize();
});

// works out the X, Y position of the click inside the canvas from the X, Y position on the page

function getPosition(mouseEvent, sigCanvas) {
  var rect = sigCanvas.getBoundingClientRect();
  return {
    X: mouseEvent.clientX - rect.left,
    Y: mouseEvent.clientY - rect.top
  };
}

/*function getPosition(mouseEvent, sigCanvas) {
  var x, y;
  if (mouseEvent.pageX != undefined && mouseEvent.pageY != undefined) {
    x = mouseEvent.pageX;
    y = mouseEvent.pageY;

  } else {
    x = mouseEvent.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
    y = mouseEvent.clientY + document.body.scrollTop + document.documentElement.scrollTop;
  }

  return {
    X: x - sigCanvas.offsetLeft,
    Y: y - sigCanvas.offsetTop
  };
}*/

function initialize() {
  // get references to the canvas element as well as the 2D drawing context
  var sigCanvas = document.getElementById("canvas");
  var context = sigCanvas.getContext("2d");
  context.strokeStyle = "#000000";
  context.lineJoin = "round";
  context.lineWidth = 3;

  // This will be defined on a TOUCH device such as iPad or Android, etc.
  var is_touch_device = 'ontouchstart' in document.documentElement;

  if (is_touch_device) {
    // create a drawer which tracks touch movements
    var drawer = {
      isDrawing: false,
      touchstart: function (coors) {
        context.beginPath();
        context.moveTo(coors.x, coors.y);
        this.isDrawing = true;
      },
      touchmove: function (coors) {
        if (this.isDrawing) {
          context.lineTo(coors.x, coors.y);
          context.stroke();
        }
      },
      touchend: function (coors) {
        if (this.isDrawing) {
          this.touchmove(coors);
          this.isDrawing = false;
        }
      }
    };

    // create a function to pass touch events and coordinates to drawer
    function draw(event) {

      // get the touch coordinates.  Using the first touch in case of multi-touch
      var coors = {
        x: event.targetTouches[0].pageX,
        y: event.targetTouches[0].pageY
      };

      // Now we need to get the offset of the canvas location
      var obj = sigCanvas;

      if (obj.offsetParent) {
        // Every time we find a new object, we add its offsetLeft and offsetTop to curleft and curtop.
        do {
          coors.x -= obj.offsetLeft;
          coors.y -= obj.offsetTop;
        }
        // The while loop can be "while (obj = obj.offsetParent)" only, which does return null
        // when null is passed back, but that creates a warning in some editors (i.e. VS2010).
        while ((obj = obj.offsetParent) != null);
      }

      // pass the coordinates to the appropriate handler
      drawer[event.type](coors);
    }

    // attach the touchstart, touchmove, touchend event listeners.
    sigCanvas.addEventListener('touchstart', draw, false);
    sigCanvas.addEventListener('touchmove', draw, false);
    sigCanvas.addEventListener('touchend', draw, false);

    // prevent elastic scrolling
    sigCanvas.addEventListener('touchmove', function (event) {
      event.preventDefault();
    }, false);
  } else {

    // start drawing when the mousedown event fires, and attach handlers to
    // draw a line to wherever the mouse moves to
    $("#canvas").mousedown(function (mouseEvent) {
      var position = getPosition(mouseEvent, sigCanvas);
      context.moveTo(position.X, position.Y);
      context.beginPath();

      // attach event handlers
      $(this).mousemove(function (mouseEvent) {
        drawLine(mouseEvent, sigCanvas, context);
      }).mouseup(function (mouseEvent) {
        finishDrawing(mouseEvent, sigCanvas, context);
      }).mouseout(function (mouseEvent) {
        finishDrawing(mouseEvent, sigCanvas, context);
      });
    });

  }
}

// draws a line to the x and y coordinates of the mouse event inside
// the specified element using the specified context
function drawLine(mouseEvent, sigCanvas, context) {

  var position = getPosition(mouseEvent, sigCanvas);

  context.lineTo(position.X, position.Y);
  context.stroke();
}

// draws a line from the last coordiantes in the path to the finishing
// coordinates and unbind any event handlers which need to be preceded
// by the mouse down event
function finishDrawing(mouseEvent, sigCanvas, context) {
  // draw the line to the finishing coordinates
  drawLine(mouseEvent, sigCanvas, context);

  context.closePath();

  // unbind any events which could draw
  $(sigCanvas).unbind("mousemove")
    .unbind("mouseup")
    .unbind("mouseout");
}

// Clear the canvas context using the canvas width and height
function clearCanvas() {
  var canvas = document.getElementById("canvas");
  var context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height);
}

async function getAndPutAnnexure() {
  var formData = new FormData();
  formData.append("work_order_id", $('#wo_id').val())

  $.ajax({
    type: "POST",
    url: "/erp/get_milsetones",
    async: true,
    data: formData,
    cache: false,
    contentType: false,
    processData: false,
    timeout: 60000,
    success: function (data) {
      console.log(data)
      
      var canvas = document.getElementById("annexure_canvas");
      var context = canvas.getContext("2d");
      context.font = "14px Arial";
      lines = (data.length * 20) + 100
      $(canvas).attr('height', lines.toString() +'px')

      x = 20;
      y = 20;
      for (const stage of data) {
        context.fillText(stage[0], x, y);
        x = 500;
        context.fillText(stage[1].toString()+'%', x, y);
        y += 20;
        x = 20;
      }
    },
    error: function (error) {
      console.log(error)
    },
  });

}

async function saveSign() {
  var canvas = document.getElementById("canvas");
  var ctx = canvas.getContext("2d");
  let pngImageBytes = canvas.toDataURL("image/png");


  const url = 'https://erpbuildahome.s3.ap-south-1.amazonaws.com/Standard+WO.pdf'
  const arrayBuffer = await fetch(url).then(res => res.arrayBuffer())
  const pdfDoc = await PDFDocument.load(arrayBuffer)

  const pngImage = await pdfDoc.embedPng(pngImageBytes)
  const pngDims = pngImage.scale(0.5)

  var annexure_canvas = document.getElementById("annexure_canvas");
  var ctx1 = annexure_canvas.getContext("2d");
  let pngImageBytes1 = annexure_canvas.toDataURL("image/png");

  const pngImage1 = await pdfDoc.embedPng(pngImageBytes1)
  const pngDims1 = pngImage.scale(0.5)

  const pages = pdfDoc.getPages()

  const date = new Date()
  pages[0].drawText(date.getDate() + '/' + (parseInt(date.getMonth()) + 1).toString() + '/' + date.getFullYear(), {
    x: 418,
    y: 678,
    size: 11,
  })

  const wo_number = $('.wo_number').text().trim()
  pages[0].drawText(wo_number, {
    x: 418,
    y: 656,
    size: 11,
  })

  const contractor_name = $('.contractor_name').text().trim()
  pages[0].drawText(contractor_name, {
    x: 418,
    y: 635,
    size: 11,
  })

  const contractor_address = $('.contractor_address').text().trim()
  pages[0].drawText(contractor_address, {
    x: 418,
    y: 609,
    size: 10,
    lineHeight: 13,
    maxWidth: 150,
  })

  const contractor_pan = $('.contractor_pan').text().trim()
  pages[0].drawText(contractor_pan, {
    x: 418,
    y: 553,
    size: 11,
  })

  const cheque_number = $('.cheque_number').text().trim()
  pages[0].drawText(cheque_number, {
    x: 418,
    y: 534,
    size: 11,
  })

  const contractor_code = $('.contractor_code').text().trim()
  pages[0].drawText(contractor_code, {
    x: 418,
    y: 514,
    size: 11,
  })

  const description = $('.trade').text().trim() + ' work order for ' + $('.project_name').text().trim()
  pages[0].drawText(description, {
    x: 100,
    y: 430,
    size: 11,
  })

  const value = $('.value').text().trim()
  pages[0].drawText(value, {
    x: 418,
    y: 430,
    size: 11,
  })

  pages[4].drawImage(pngImage, {
    x: 700,
    y: 700,
    width: 100,
    height: 50,
  })

  pages[4].drawImage(pngImage, {
    x: 100,
    y: 100,
    width: 100,
    height: 50,
  })




  const pdfBytes = await pdfDoc.save()


  const blob = new Blob([pdfBytes])
  var file = new File([blob], 'test.pdf');

  var formData = new FormData();
  formData.append("wo_id", $('#wo_id').val())
  formData.append("file", file, 'test.pdf');

  $.ajax({
    type: "POST",
    url: "/erp/upload_signed_wo",
    success: function (data) {
      window.location.href = '/erp/view_unsigned_work_order'
    },
    error: function (error) {
      console.log(error)
      // handle error
    },
    async: true,
    data: formData,
    cache: false,
    contentType: false,
    processData: false,
    timeout: 60000
  });

  // Trigger the browser to download the PDF document
  // download(pdfBytes, "signed_wo.pdf", "application/pdf");



}

