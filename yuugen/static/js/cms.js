//setting csrf cookie for ajax operations

$(document).ready(function () {
  function getCookie(name){
      var cookieValue = null;
      if (document.cookie && document.cookie != ''){
          var cookies = document.cookie.split(';');
          for (var i = 0; i< cookies.length; i++){
              var cookie = cookies[i].trim();

              if (cookie.substring(0, name.length +1) === (name + "=")){
                  cookieValue = decodeURIComponent(cookie.substring(name.length +1));
                  break;
              }
          }
      }
      return cookieValue;
  };

  var csrftoken = getCookie('csrftoken')

  function csrfSafeMethod(method){
      return ['GET', 'OPTIONS', 'HEAD', 'TRACE'].includes(method);
  };

  $.ajaxSetup({
      beforeSend: function(xhr, setting){
          if (!csrfSafeMethod(setting.type) && !this.crossDomain)
          xhr.setRequestHeader("X-CSRFToken", csrftoken)
      }
    });
  });


//comportement function
$(document).ready(function(){
  var n_row = $('#Attributes_table tbody tr').length;
  if(n_row === 2){
    $('#del_row').prop('disabled',true)
  };
  $('#btn_refresh').hide();
  $('#id_content-input').wysiwyg({
  });
  $('#id_description-input').wysiwyg({
  });
});

$(document).on('click', '#btn_refresh',function(){
  location.reload(true);
});

$(document).on('click', '#add_row', function(e){
  $('#del_row').prop('disabled',false)
  // console.log('add clicked')
  var index = $('.duplicable').length
  var newId = 'duplicable'+index;
  var row = `
    <tr id="${newId}" class="duplicable">
    <td>
        <ul class="list-inline">
            <li>
                <button class="btn btn-outline-danger btn-sm rounded-0" type="button" data-toggle="tooltip" data-placement="top" title="Delete Row" id="del_row"><i class="fa-solid fa-minus"></i></button>
            </li>
            <li>
                <button  class="btn btn-outline-success btn-sm rounded-0" type="button" data-toggle="tooltip" data-placement="top" title="Add Row" id="add_row"><i class="fa-solid fa-plus"></i></button>
            </li>
        </ul>
    </td>
    <td>
        <div class="input-group mb-3">
            <input class="form-control finition" type="text" id="finition_input" placeholder="Add a Finition" aria-label="Add a Finition" aria-describedby="finition_submit"  >
        </div>
    </td>
    <td>
        <div class="input-group mb-3">
            <input class="form-control size" type="text" id="size_input" placeholder="Add a Size" aria-label="Add a size" aria-describedby="size_submit">
        </div>
    </td>
    <td class="input_attr_price">
        <div class="input-group mb-3">
            <div class="input-group-prepend">
                <span class="input-group-text">$</span>
                <span class="input-group-text">0.00</span>
            </div>
            <input id="price_attr_input" type="text" class="form-control price" aria-label="Dollar amount (with dot and two decimal places)">
        </div>
    </td>
    <td class="input_attr_img">
        <div class="input-group mb-3">
            <div class="input-group-prepend">
                <span class="input-group-text" id="inputGroupFileAddon01">Upload</span>
            </div>
            <div class="custom-file">
                <input type="file" class="custom-file-input img" id="img_attr_input" aria-describedby="inputGroupFileAddon01">
                <label class="custom-file-label" for="img_attr_input">Choose file</label>
            </div>
        </div>
    </td>
  </tr>
    `
  $('#Attributes_table tbody').append(row);
});


$(document).on("click",'#del_row',function(){
  // console.log('del clicked')
  $(this).closest('tr').remove(); 
});

$(document).on('click', '#reset-search', function(){
  // console.log('reset hitted')
  $('div').remove('#append-result');
})


//Ajax Call 

$(document).on('click', '#ttag_submit', function(e){
  $.ajax({
    type: 'POST',
    url :  window.location.pathname,
    data : {
      'ajax_post': 'create_ttag',
      'sent_ttag': $('#id_input_ttag').val(),
    },
    success : function(){
      location.reload(true)
    },
    error: function(xhr, errmsg, err){
      alert(xhr.status + ":" + xhr.responseText)
    }

  })
});



$(document).on('click', '#ctag_submit', function(e){
  $.ajax({
    type: 'POST',
    url :  window.location.pathname,
    data : {
      'ajax_post': 'create_ctag',
      'sent_ctag': $('#id_input_ctag').val(),
    },
    success : function(){
      location.reload(true)
    },
    error: function(xhr, errmsg, err){
      alert(xhr.status + ":" + xhr.responseText)
    }

  })
});

$(document).on('click', '#otag_submit', function(e){
  $.ajax({
    type: 'POST',
    url :  window.location.pathname,
    data : {
      'ajax_post': 'create_otag',
      'sent_otag': $('#id_input_otag').val(),
    },
    success : function(){
      location.reload(true)
    },
    error: function(xhr, errmsg, err){
      alert(xhr.status + ":" + xhr.responseText)
    }

  })
});

$(document).on('click', '#attribute_submit', function(e){
  var attrs;
   $('#row_source').map(function(){
  attrs = $('select, input', 'td').map(function(){
      return $(this).val();
    }).get();
  }).get();
  console.log(attrs)
  $.ajax({
    type: 'POST',
    url :  window.location.pathname,
    data : {
      'ajax_post': 'create_finition',
      'finition_sent': $('#finition_input').val(),
      'size_sent': $('#size_input').val(),
      'price_sent': $('#price_input').val(),
      'img_sent': $('#img_input').val(),
    },
    success : function(){
      console.log('finition-sent')
    },
    error: function(xhr, errmsg, err){
      alert(xhr.status + ":" + xhr.responseText)
    }

  })
});




$(document).on('click', '#product-submit', function(e){
  var attrs = [];
  $('.duplicable').each(function(index, item){ 
    var id = $(this).attr('id');
    var finition = $(this).find('.finition').val();
    var size = $(this).find('.size').val();
    var price = $(this).find('.price').val();
    var image = $(this).find('.img').val();
    attrs.push({
      'id': id,
      'finition' : finition,
      'size' : size,
      'price' : price,
      'img': image,
    });
  });
  $.ajax({
    type: 'POST',
    url :  window.location.pathname,
    data : {
      'ajax_post' : 'create_product',
      'designation': $('#id_designation_input').val(),
      'description': $('.editor-content').text(),
      'selected_ttag': $('#id_product_select_ttag').val(),
      'selected_ctag': $('#id_product_select_ctag').val(),
      'selected_otag': $('#id_product_select_otag').val(),
      'attr': JSON.stringify(attrs)
        
      },
    success : function(response){
      var error = response.submit_failure
      if(response.submit_failure){
        console.log(error)
        $('#message').append(`<div class="alert alert-danger" role="alert">`+error+`</div>`)
      }
      else{
      $('#btn_refresh').show();
      }
    },
    error: function(xhr, errmsg, err){
      console.log(xhr.status + ":"+ errmsg+ err)
    }

  });
});

$(document).on('click', '#page-submit', function(e){
  $.ajax({
    type: 'POST',
    url :  window.location.pathname,
    data : {
      "action": 'create_page',
      "title": $('#id_title-input').val(),
      "content": $('#id_content-input').val(),
      },
    success : function(){
      location.reload(true)
      },
    error: function(xhr, errmsg, err){
      alert(xhr.status + ":" + xhr.responseText)
     }

  })
});



$(document).on('click', '#submit-search', function(e){
  e.preventDefault();
  $('div').remove('#append-result');
  $.ajax({
    type: 'POST',
    url :  window.location.pathname,
    data : {
      "action": 'submit_search',
      "query": $('#search-bar').val(),
    },
    success : function(response){
      // console.log('query sent');
      var er = response.not_found;
      if(er){
        console.log(er);
        $("#results-error").append('<div id="append-result"><h4>'+er+'</h4></div>')
      }
      if(response.products){
        var products = JSON.parse(response.products);
        console.log(products);
        $.each(products, function(index, item){
          $("#results-products").append(
            `
            <div id="append-result" class="col mb-4">
              <div class="card" style="width:18rem">
                <div class="card-body" id="product-card">
                  <h5 class="card-title"><a href="{% url 'cms:product-editor' %}" value="${item['fields']['designation']}">${item['fields']['designation']}</a></h5>
                  <h6 class="card-subtitle mb-2 text-muted">Product</h6>
                </div>
            </div>
            `
          );
        });
      }
      if(response.details){
      var details = JSON.parse(response.details);
      $.each(details, function(index, item){
        console.log(item.pk)
        $("#results-details").append(
          `
          <div id="append-result" class="col mb-4">
            <div class="card" style="width:18rem">
              <div class⁼card-body" id="details-card">
                <h5 class="card-title"><a href="{% url 'cms:details-editor' %}" value="${item.pk || ''}">${item.pk || ''}</a></h5>
                <h6 class="card-subtitle mb-2 text-muted">Detail</h6>
              </div>
            </div>
          </div>
          `
        );
      })
      }
    if(response.pages){
      var pages = JSON.parse(response.pages);
      console.log(pages.pk)
      $.each(pages, function(index, item){
        $("#resultes-pages").append(
          `
            <div id="append-result" class="card">
              <div class="card-body">
              <h5 class="card-title"><a href="{% url 'cms:page-editor' %}" value="${item.pk}">${item.fields.title}</a></h5>
              <H6 class="card-subtitle mb-2 text-muted">Page</H6>
              </div>
            </div>
          `
        );
      });
    }
    if(response.staff_products){
      var products = JSON.parse(response.staff_products);
      $.each(products, function(index, item){
        $("#results-products").append(
          `
          <div id="append-result" class="col mb-4"
            <div class="card" style="width:18rem">
              <div class⁼card-body" id="product-card">
                <h5 class="card-title"><a href="{% url 'cms:product-editor' %}" value="${item.pk}">${item['fields']['designation']}</a></h5>
                <h6 class="card-subtitle mb-2 text-muted">Product</h6>
              </div>
          </div>
          `
        );
      })
    }
    if(response.staff_details){
      var details = JSON.parse(response.staff_details);
      $.each(details, function(index, item){
        $("#results-details").append(
          `
          <div id="append-result" class="col mb-4">
            <div class="card" style="width:18rem">
              <div class⁼card-body" id="details-card">
                <h5 class="card-title"><a href="{% url 'cms:details-editor' %}" value="${item.pk || ''}">${item.pk || ''}</a></h5>
                <h6 class="card-subtitle mb-2 text-muted">Detail</h6>
              </div>
            </div>
          </div>
          `
        );
      })
      }
      if(response.staff_pages){
      var pages = JSON.parse(response.staff_pages);
      $.each(pages, function(index, item){
        console.log(item.fields.title)
        $("#resultes-pages").append(
          `
            <div id="append-result" class="card">
              <div class="card-body">
              <h5 class="card-title"><a href="{% url 'cms:page-editor' %}" value="${item.pk}">${item['fields']['title']}</a></h5>
              <H6 class="card-subtitle mb-2 text-muted">Page</H6>
              </div>
            </div>
          `
        )
      })
    }
    },
    error: function(xhr){
      console.log(xhr.status + ":" + xhr.responseText)
    }

  })
});

$(document).ready(function(){
  $('#product-list').DataTable({
    paging: false,
    bInfo: false,
    columnDefs:[
      {
        "targets": 11,
        "orderable": false,
      }
    ],
    dom: 'Blfrt',
    buttons:[
      {
        extend: 'copy',
        text: '<i class="fas fa-clone"></i>',
        className:'btn btn-secondary',
        titleAttr:'Copy',
        exportOptions:{
          columns:[0,1,2,3,4,5,6,7,8,9,10]
        },
      },
      {
        extend:'csv',
        text:'<i class="fas fa-file-csv"></i>',
        className:'btn btn-secondary',
        titleAttr:'CSV',
        exportOptions:{
          columns:[0,1,2,3,4,5,6,7,8,9,10]
        },
      },
      {
        extend:'pdf',
        text:'<i class="fas fa-file-pdf"></i>',
        className:'btn btn-secondary',
        titleAttr:'PDF',
        exportOptions:{
          columns:[0,1,2,3,4,5,6,7,8,9,10]
          },
        title: 'Product list',
        orientation:"landscape",
        tableHeader:{
          alignment:'center'
        },
        customize: function(doc){
          doc.styles.tableHeader.alignment = 'center';
          doc.styles.tableHeader.fontSize= 10;
          doc.defaultStyle.fontSize= 8;
        }
      },
    ],
  });

});