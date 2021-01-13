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
  //$('.btn-success').attr('style','background-color: #AE0B2A;color: #FFFFFF"');
  //$('.btn-info').attr('style','background-color: #AE0B2A;color: #FFFFFF"');
  //$('.btn-warning').attr('style','background-color: #AE0B2A;color: #FFFFFF"');
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
});

// 报废
$(".btn-scrap").off().on('click',function(){
  var r = confirm("是否确定仪器已报废？")
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
      //alert(JSON.stringify(result.student))
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
  document.getElementById("current_check_qualification").innerHTML=data.check_qualification;
  document.getElementById("current_buy_date").innerHTML=data.buy_date;

  //alert(data.student.length)
  //var student = document.getElementsByClassName('student');
  //for(var i = 0;i < data.student.length; i++){
  //  student[i].innerHTML = data.student[i].userid
  //}

  $('#equip_name_update').attr("value",data.equip_name);
  $('#equip_id_update').attr("value",data.equip_id);
  $('#type_update').attr("value",data.type);
  $('#address_update').attr("value",data.address);
  document.getElementById("description_update").innerHTML=data.description;
  $('#qualification_update').attr("value",data.qualification);
  $('#buy_date_update').attr("value",data.buy_date);

  if(data.check_qualification == '是'){
    $("#yes_update").prop("checked",true);
    $("#no_update").prop("checked",false);
    //$('#no_update').removeAttr("checked");
    //$('#yes_update').attr("checked","checked");
    $("#show_qualification").attr('style','display:block;');
    $("#current_check_qualification").attr("style","color: blue");
    $("#current_check_qualification").attr("onclick","see_qualification()");
    $("#current_check_qualification").attr("title","点击查看具备仪器使用资格的学生");
  }
  else{
    $("#no_update").prop("checked",true);
    $("#yes_update").prop("checked",false);
    $("#show_qualification").css('display','none');
    $("#check_qualification").css('display','none');
    $("#current_check_qualification").attr("style","color: default");
    $("#current_check_qualification").attr("onclick","none");
    $("#current_check_qualification").removeAttr("title");
    $("#current_check_qualification").removeAttr("style");
    $("#current_check_qualification").removeAttr("onclick");
  }

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

// 导入学生使用资格
// $("#btn-check-in").click(function(){
//   $("#check_qualification").attr('style','display:block;');
// });

function see_qualification(){
  var height = 500;
	var width = 600;
	var top=Math.round((window.screen.height-height)/2);
	var left=Math.round((window.screen.width-width)/2);
  $.ajax({
    type:"GET",
    contentType:"application/json;charset=UTF-8",
    url:"/equip/qualification/",
    data:{equip_id:_equip_id},
    success:function(result){
      console.log("success!")
      console.log(result)
      /*setTimeout(function() {
        location.reload();
      }, 1 * 2000);*/
      window.open('/equip/qualification', _equip_id,"height=" + height + ", width=" + width + ", top=" + top + ", left= " + left + ", toolbar=no, menubar=no, scrollbars=auto, resizable=no, location=yes, status=no");
    },
    error:function(e){
      console.log(e.status);
      console.log(e.responseText);
      alert("学生使用资格查询失败！")
    }
  })
};

// 查看具备使用资格的学生
// $("#btn-see").off().on('click',function(){
//   var height = 500;
// 	var width = 600;
// 	var top=Math.round((window.screen.height-height)/2);
// 	var left=Math.round((window.screen.width-width)/2);
//   $.ajax({
//     type:"GET",
//     contentType:"application/json;charset=UTF-8",
//     url:"/equip/qualification/",
//     data:{equip_id:_equip_id},
//     success:function(result){
//       console.log("success!")
//       console.log(result)
//       /*setTimeout(function() {
//         location.reload();
//       }, 1 * 2000);*/
//       window.open('/equip/qualification', _equip_id,"height=" + height + ", width=" + width + ", top=" + top + ", left= " + left + ", toolbar=no, menubar=no, scrollbars=auto, resizable=no, location=yes, status=no");
//     },
//     error:function(e){
//       console.log(e.status);
//       console.log(e.responseText);
//       alert("学生使用资格查询失败！")
//     }
//   })
//   //window.open('/equip/index', 'newwindow', 'height=500, width=800, top=0, left=0, toolbar=no, menubar=no, scrollbars=no, resizable=no,location=no, status=no');
// });

// 撤销学生使用资格
$(".btn-withdraw").off().on('click',function(){
  _equip_id = $(this).attr("equip_id")
  _sno = $(this).attr("sno")
  var r = confirm("是否确定撤销学生 "+_sno+" 对仪器 "+_equip_id+" 的使用资格？")
  if(r){
    $.ajax({
      type:"GET",
      contentType:"application/json;charset=UTF-8",
      url:"/equip/withdraw/",
      data:{sno:_sno,
            equip_id:_equip_id},
      success:function(result){
        console.log("success!")
        console.log(result)
        alert("成功收回学生 "+_sno+" 对仪器 "+_equip_id+" 的使用资格！")
        setTimeout(function() {
          location.reload();
        }, 1 * 2000);
        window.location.reload();
      },
      error:function(e){
        console.log(e.status);
        console.log(e.responseText);
        alert("学生使用资格收回失败！")
      }
    })
  }
});

// 确认导入学生使用资格
$("#btn-check").off().on('click',function(){
  _sno = $("#sno").val();
  _equip_id = $(this).attr("equip_id");
  var r = confirm("是否确定学生 "+_sno+" 具备仪器 "+_equip_id+" 的使用资格？")
  if(r){
    $.ajax({
      type:"GET",
      contentType:"application/json;charset=UTF-8",
      url:"/equip/check/",
      data:{sno:_sno,
            equip_id:_equip_id},
      success:function(result){
        console.log("success!")
        console.log(result)
        alert("成功导入具备使用资格的学生学号！")
        setTimeout(function() {
          location.reload();
        }, 1 * 2000);
        window.location.reload();
      },
      error:function(e){
        console.log(e.status);
        console.log(e.responseText);
        alert("学生使用资格导入失败！学号输入错误 或 该学号可能已被导入！")
        window.location.reload();
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
            check_qualification: context.check_qualification,
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
            check_qualification: context.check_qualification,
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