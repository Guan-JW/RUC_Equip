$(document).ready(function(){
  $('#equip-detail').css('display','none');
  $('#equip-update').css('display','none');
  $('.input-edit').attr("readonly","readonly");
  var breakdown = document.getElementsByClassName('btn-breakdown');
  for(var i = 0;i < breakdown.length; i++){
    if(breakdown[i].getAttribute('status') == '故障'){
      breakdown[i].style.display='none';
    }
  }
});

// 已修复
$(".btn-repair").off().on('click',function(){
  var r = confirm("是否确定仪器已修复？")
  if(r){
    _equip_id = $(this).attr("equip_id")
    $.ajax({
      type:"GET",
      contentType:"application/json;charset=UTF-8",
      url:"/equip/repair/",
      data:{equip_id:_equip_id},
      success:function(result){
        console.log("success!")
        console.log(result)
        alert("仪器已修复！")
        setTimeout(function() {
          location.reload();
        }, 1 * 2000);
        window.location.reload();
      },
      error:function(e){
        console.log(e.status);
        console.log(e.responseText);
      }
    })
  }
  /*_equip_id = $(this).attr("equip_id")
  $.ajax({
    type:"GET",
    contentType:"application/json;charset=UTF-8",
    url:"/equip/repair",
    data:{equip_id:_equip_id},
    success:function(result){
      console.log("success!")
      console.log(result)
      alert("仪器已修复！")
      setTimeout(function() {
        location.reload();
      }, 1 * 2000);
      window.location.reload();
    },
    error:function(e){
      console.log(e.status);
      console.log(e.responseText);
    }
  })*/
});

// 报废
$(".btn-scrap").off().on('click',function(){
  var r = confirm("是否确定仪器已报废？")
  if(r){
    _equip_id = $(this).attr("equip_id")
    alert(_equip_id)
    $.ajax({
      type:"GET",
      contentType:"application/json;charset=UTF-8",
      url:"/equip/scrap/",
      data:{equip_id:_equip_id},
      success:function(result){
        console.log("success!")
        console.log(result)
        alert("仪器报废！仪器信息已删除！")
        setTimeout(function() {
          location.reload();
        }, 1 * 2000);
        window.location.reload();
      },
      error:function(e){
        console.log(e.status);
        console.log(e.responseText);
        alert("仪器信息删除失败！")
      }
    })
  }
});

// 故障
$(".btn-breakdown").off().on('click',function(){
  var r = confirm("是否确定仪器故障？")
  if(r){
    _equip_id = $(this).attr("equip_id")
    $.ajax({
      type:"GET",
      contentType:"application/json;charset=UTF-8",
      url:"/equip/breakdown/",
      data:{equip_id:_equip_id},
      success:function(result){
        console.log("success!")
        console.log(result)
        setTimeout(function() {
          location.reload();
        }, 1 * 2000);
        alert("仪器故障！")
        window.location.reload();
      },
      error:function(e){
        console.log(e.status);
        console.log(e.responseText);
        alert("仪器状态修改失败！")
      }
    })
  }
});

// 显示仪器详情
$(".show-detail").off().on('click',function(){
  $('#equip-detail').css('display','inline');
  _equip_id = $(this).attr("equip_id")
  $.ajax({
    type:"GET",
    contentType:"application/json;charset=UTF-8",
    url:"/equip/detail/",
    data:{equip_id:_equip_id},
    success:function(result){
      console.log("success!")
      console.log(result)
      //alert("显示仪器详情！")
      show_equip_detail(result)
    },
    error:function(e){
      console.log(e.status);
      console.log(e.responseText)
      alert("仪器详情获取失败！")
    }
  })
});

function show_equip_detail(data){
  //$('#equip-detail').css('display','inline');
  //var data = eval('('+jsonData+')');
  //var data = jsonData
  //alert(data.equip_id)
  document.getElementById("current_equip_id").innerHTML=data.equip_id;
  document.getElementById("current_equip_name").innerHTML=data.equip_name;
  document.getElementById("current_type").innerHTML=data.type;
  document.getElementById("current_address").innerHTML=data.address;
  document.getElementById("current_status").innerHTML=data.status;
  document.getElementById("current_description").innerHTML=data.description;
  document.getElementById("current_qualification").innerHTML=data.qualification;
  document.getElementById("current_buy_date").innerHTML=data.buy_date;

  $('#equip_name_update').attr("value",data.equip_name);
  $('#equip_id_update').attr("value",data.equip_id);
  $('#type_update').attr("value",data.type);
  $('#address_update').attr("value",data.address);
  document.getElementById("description_update").innerHTML=data.description;
  $('#qualification_update').attr("value",data.qualification);
  $('#buy_date_update').attr("value",data.buy_date);

  $('#btn-edit').attr("equip_id",data.equip_id);
  $('#btn-delete').attr("equip_id",data.equip_id);
  $('#btn-submit-update').attr("target_id",data.equip_id);
  $('#btn-reset-update').attr("target_id",data.equip_id);
  $('#btn-submit-update').attr("target_status",data.status);
  $('#btn-reset-update').attr("target_status",data.status);
};

// 编辑
$("#btn-edit").click(function(){
  $('#btn-submit-edit').css('display','inline');
  $('#btn-reset-edit').css('display','inline');
  $('#equip-update').css('display','inline');
  $('#date-edit').css('display','inline');
  $('.input-edit').removeAttr("readonly");
});

// 删除
$("#btn-delete").off().on('click',function(){
  var r = confirm("是否确定删除仪器信息？")
  if(r){
    _equip_id = $(this).attr("equip_id")
    $.ajax({
      type:"GET",
      contentType:"application/json;charset=UTF-8",
      url:"/equip/scrap/",
      data:{equip_id:_equip_id},
      success:function(result){
        console.log("success!")
        console.log(result)
        alert("仪器信息已删除！")
        setTimeout(function() {
          location.reload();
        }, 1 * 2000);
        window.location.reload();
      },
      error:function(e){
        console.log(e.status);
        console.log(e.responseText);
        alert("仪器信息删除失败！")
      }
    })
  }
});

function update(context){
  var r = confirm("是否确定更新的仪器信息无误？")
  if(r){
    $.ajax({
      type:"GET",
      contentType:"application/json;charset=UTF-8",
      url:"/equip/update/",
      data: {equip_id: context.equip_id,
            equip_name: context.equip_name,
            type: context.type,
            address: context.address,
            description: context.description,
            qualification: context.qualification,
            buy_date: context.buy_date,
            status: context.status,
            target: context.target},
      async: false,
      success:function(result){
        console.log("success!")
        console.log(result)
        alert("仪器信息已更新！")
        setTimeout(function() {
          location.reload();
        }, 1 * 2000);
        window.location.reload();
      },
      error:function(e){
        //alert(context['equip_id'])
        console.log(e.status);
        console.log(e.responseText);
        alert("仪器信息更新失败！")
      }
    })
  }
};

function insert(context){
  var r = confirm("是否确定插入的仪器信息无误？")
  if(r){
    $.ajax({
      type:"GET",
      contentType:"application/json;charset=UTF-8",
      url:"/equip/insert/",
      data: {equip_id: context.equip_id,
            equip_name: context.equip_name,
            type: context.type,
            address: context.address,
            description: context.description,
            qualification: context.qualification,
            buy_date: context.buy_date},
      async: false,
      success:function(result){
        console.log("success!")
        console.log(result)
        if(result.status == 1)
          alert("仪器信息插入成功！")
        else{
          alert("无资格插入仪器信息！")
          location.href = "/login/";
        }
        setTimeout(function() {
          location.reload();
        }, 1 * 2000);
        window.location.reload();
      },
      error:function(e){
        console.log(e.status);
        console.log(e.responseText);
        alert("仪器信息插入失败！")
        window.location.reload();
      }
    })
  }
};