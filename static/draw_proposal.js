const { PDFDocument, StandardFonts, rgb } = PDFLib




// Clear the canvas context using the canvas width and height
function clearCanvas() {
  var canvas = document.getElementById("annexure_canvas");
  var context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height);
}

var lineHeight;
async function getAndPutAnnexure() {
    var canvas = document.getElementById("annexure_canvas");
    var context = canvas.getContext("2d");
    context.font = "14px Arial";
    lines = (data.length * 20) + 100
    lineHeight = lines
    $(canvas).attr('height', lines.toString() +'px')

    x = 20;
    y = 20;
    for (const stage of data) {
      context.fillText(stage[0], x, y);
      x = 500;
      context.fillText(stage[1].toString()+'%', x, y);
      x = 600
      const amount = (parseFloat(stage[1]) / 100) * wo_value
      context.fillText('₹ '+amount.toString(), x, y);
      y += 20;
      x = 20;
    }

}

$('.preview-proposal').on('click', async function(){
    const prosposalFile = $(this).attr('data-file')
    console.log(prosposalFile)
    var canvas = document.getElementById("annexure_canvas");
    var context = canvas.getContext("2d");
    context.font = "30px Arial";
    lines = ($('.floor-element').length * 40) + 100
    lineHeight = lines
    $(canvas).attr('height', lines.toString() +'px')

    x = -90;
    y = 40;


    context.font = "20px Times New Roman";
    x = 170;

    context.fillText('Slab area', x, y);
    x += 145;


    context.fillText('Cost per sqft', x, y);
    x += 145;

    context.fillText('Cost for floor', x, y);
    y += 46;
    x = -90;

    let y1
    context.strokeStyle = '#b9b9b9';
    context.lineWidth = 0.5;

    for(y1=1; y1< 100*3;y1 = y1+50 ) {
      context.beginPath();
      context.moveTo(0, y1);
      context.lineTo(600, y1);

      // Draw the Path
      context.stroke();

    }

    for(let x=1; x< 160*4;x = x+150 ) {
      context.beginPath();
      context.moveTo(x, 0);
      context.lineTo(x, 50 *( $('.floor-element').length + 1));

      // Draw the Path
      context.stroke();

    }


    context.strokeStyle = '#000';

    
    
    $('.slab-area-in-sqft').removeClass('border-danger');
    $('#shr_and_oht').removeClass('border-danger');

    for (const element of $('.floor-element')) {
      if($(element).find('.slab-area-in-sqft').val().trim() == '') {
        $(element).find('.slab-area-in-sqft').addClass('border-danger');
        return;
      }
      context.font = "18px Times New Roman";
      context.fillText($(element).find('.item-desc').text().replace('Enter ','').replace(' slab area',''), x, y);
      x = 170;

      context.fillText($(element).find('.slab-area-in-sqft').val(), x, y);
      x += 145;


      context.fillText($('.cost_per_sqft_for_plan').text(), x, y);
      x += 145;

      context.fillText($(element).find('.total-cost-for-floor').val(), x, y);
      y += 46;
      x = -90;

    }

    if($('#shr_and_oht').val().trim() == '') {
      $('#shr_and_oht').addClass('border-danger');
      return
    }

    let pngImageBytes = canvas.toDataURL("image/png");


  const url = 'https://office.buildahome.in/files/'+ prosposalFile
  const arrayBuffer = await fetch(url).then(res => res.arrayBuffer())
  const pdfDoc = await PDFDocument.load(arrayBuffer)

  const helveticaFont = await pdfDoc.embedFont(StandardFonts.Helvetica)

  const pngImage = await pdfDoc.embedPng(pngImageBytes)

  let pngImageBytes1 = canvas.toDataURL("image/png");

  const pngImage1 = await pdfDoc.embedPng(pngImageBytes1)

  const pages = pdfDoc.getPages()

  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

var node = document.getElementById('toImage');

const img = await htmlToImage.toPng(node)
  
const pngImage2 = await pdfDoc.embedPng(img)
const imgDom = document.createElement('IMG')
imgDom.src = img;
console.log(parseInt(node.scrollWidth), parseInt(node.scrollHeight))

  pages[0].setFont(helveticaFont)
  pages[0].setFontSize(14)
  pages[0].setFontColor(rgb(0/255, 84/255, 125/255))

  pages[0].drawText($('#client_name').text().toUpperCase(), {
    x: 780,
    y: 347,
  })

  pages[0].drawText(`${new Date().getDate()} ${monthNames[new Date().getMonth()]} ${new Date().getFullYear()}`, {
    x: 640,
    y: 58,
  })

  console.log(pages[14].getSize(), pages[14].getX(), pages[14].getY(), canvas.width, canvas.height)

  pages[14].drawImage(pngImage2, {
    x: 20,
    y: 130,
    width: parseInt(node.scrollWidth),
    height:  parseInt(node.scrollHeight),
  })

  pages[14].setFontSize(14)
  
  pages[14].drawText($('#project_value').val() + '/-', {
    x: 96,
    y: 92,
  })

  pages[14].drawText(parseFloat($('#project_value').val()) * 0.01 + '/-', {
    x: 170,
    y: 72,
  })


  const pdfBytes = await pdfDoc.save()


  const blob = new Blob([pdfBytes], { type: 'application/pdf' })

  proposal_pdf = new File([blob], `Proposal for ${$('#client_name').text()}.pdf`);

  console.log(proposal_pdf)


  var url1 = window.URL.createObjectURL(blob);



    // Create a link element
    var link = document.createElement('a');

    // Set the link's href to the Blob URL and download attribute to the desired file name
    link.href = url1;
    link.download = 'test.pdf';

    // Simulate a click event on the link to trigger the download
    // link.click();

    // // Clean up by revoking the URL object
    // window.URL.revokeObjectURL(url1);

    $('.proposal-iframe').removeClass('d-none')
    $('.proposal-iframe').get(0).src = url1

    $('.submit-for-approval').attr('disabled', false)

})



var proposal_pdf;

async function saveSign() {
  $('.create-wo-btn').attr('disabled','true')
  $('.create-wo-btn').text('Submitting..')
  if($('.verification_code').text().length) {
    entered_code = $('#entered_code').val()
    if (entered_code.trim() != $('.verification_code').text().trim()) {
      alert('Invalid verification code')
      $('.create-wo-btn').removeAttr('disabled')
      $('.create-wo-btn').text('Submit')
      return false;
    }
  }
  getAndPutAnnexure()
  var canvas = document.getElementById("canvas");
  var ctx = canvas.getContext("2d");
  let pngImageBytes = canvas.toDataURL("image/png");


  const url = 'https://office.buildahome.in/static/Standard_WO.pdf'
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
    x: 448,
    y: 698,
    size: 11,
  })

  const wo_number = $('.wo_number').text().trim()
  pages[0].drawText(wo_number, {
    x: 448,
    y: 676,
    size: 10,
    lineHeight: 13,
  })

  const contractor_name = $('.contractor_name').text().trim()
  pages[0].drawText(contractor_name, {
    x: 448,
    y: 655,
    size: 11,
  })

  const contractor_address = $('.contractor_address').text().trim()
  pages[0].drawText(contractor_address, {
    x: 448,
    y: 609,
    size: 10,
    lineHeight: 13,
    maxWidth: 150,
  })

  const contractor_pan = $('.contractor_pan').text().trim()
  pages[0].drawText(contractor_pan, {
    x: 448,
    y: 553,
    size: 11,
  })

  const cheque_number = $('.cheque_number').text().trim()
  pages[0].drawText(cheque_number, {
    x: 448,
    y: 534,
    size: 11,
  })

  const contractor_code = $('.contractor_code').text().trim()
  pages[0].drawText(contractor_code, {
    x: 448,
    y: 514,
    size: 11,
  })

  const description = $('.trade').text().trim() + ' work order for ' + $('.project_name').text().trim()
  pages[0].drawText(description, {
    x: 100,
    y: 410,
    size: 11,
  })

  if($(".total_bua").text().trim().length && $(".cost_per_sqft").text().trim().length) {
    const total_bua = $(".total_bua").text().trim() 
    const cost_per_sqft = $(".cost_per_sqft").text().trim() 
    pages[0].drawText('Total BUA :'+total_bua.toString()+', Cost/sqft : '+cost_per_sqft.toString(), {
      x: 100,
      y: 395,
      size: 11,
    })
  }

  const value = $('.value').text().trim()
  pages[0].drawText(value, {
    x: 448,
    y: 410,
    size: 11,
  })

  const notes = $(".contractor_notes").text().trim()
  const notesList = notes.split('\n')
  var yCord = pages[3].getSize().height - 120;
  for(const note of notesList) {
    pages[3].drawText(note.trim(), {
      x: 100,
      y: yCord,
      size: 10,
      lineHeight: 12,
      maxWidth: pages[3].getSize().width - 150,
    })
    noOfLines = parseInt(note.trim().length / 100)
    yCord = yCord - (14 * noOfLines)
    yCord = yCord - 20;
  } 
  

  pages[4].drawImage(pngImage, {
    x: 330,
    y: 140,
    width: 100,
    height: 50,
  })

  const sealUrl = 'https://office.buildahome.in/static/seal.png'
  const sealImgBytes = await fetch(sealUrl).then((res) => res.arrayBuffer())

  const sealImg = await pdfDoc.embedPng(sealImgBytes)

  pages[4].drawImage(sealImg, {
    x: 40,
    y: 90,
    width: 70,
    height: 100,
  })
  
  pages[4].drawImage(pngImage1, {
    x: 40,
    y: pages[4].getSize().height - 110  - parseInt(lineHeight * 0.8),
    width: parseInt(550 * 0.8),
    height: parseInt(lineHeight * 0.8),
  })




  const pdfBytes = await pdfDoc.save()


  const blob = new Blob([pdfBytes])
  proposal_pdf = new File([blob], `Proposal for ${$('#client_name').text()}.pdf`);

  console.log(proposal_pdf)

  
  
  
}

$('.submit-for-approval').on('click', function(){
  $('.submit-for-approval').attr('disabled', true)
  var formData = new FormData();

  console.log(proposal_pdf)

  formData.append("proposal_pdf", proposal_pdf, `Proposal for ${$('#client_name').text()}.pdf`);

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/upload_proposal_and_submit_for_approval', true);

  xhr.onload = function () {
      if (xhr.status === 200) {
          console.log('Done')
          window.location.href='/create_proposal'
      } else {
        console.log('failed')
      }
  };

  xhr.send(formData);
})


