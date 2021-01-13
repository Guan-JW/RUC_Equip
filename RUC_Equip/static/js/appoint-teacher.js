$(document).ready(function(){
  var status_ed = document.getElementsByClassName('status_ed');
  for(var i = 0;i < status_ed.length; i++){
    if(status_ed[i].innerHTML == '通过'){
      status_ed[i].style="color: green;"
    }
    else if(status_ed[i].innerHTML =='已撤回'){
        status_ed[i].style="color: orange"
    }
    else{
      status_ed[i].style="color: red;"
    }
  }
});

// 同意
$(".btn-agree").off().on('click',function(){
  var r = confirm("是否确定同意预约？")
  if(r){
    _index_id = $(this).attr("index_id")
    $.ajax({
      type:"GET",
      contentType:"application/json;charset=UTF-8",
      url:"/teacher/Agree/",
      data:{index_id:_index_id},
      success:function(result){
        console.log("success!")
        console.log(result)
        if(result.status == 1)
          alert("同意预约！")
        else
          alert("无资格操作！")
        setTimeout(function() {
          location.reload();
        }, 1 * 2000);
        window.location.reload();
      },
      error:function(e){
        console.log(e.status);
        console.log(e.responseText);
        alert("审批操作失败！")
      }
    })
  }
});

// 驳回
$(".btn-reject").off().on('click',function(){
  var r = confirm("是否确定驳回预约？")
  if(r){
    _index_id = $(this).attr("index_id")
    $.ajax({
      type:"GET",
      contentType:"application/json;charset=UTF-8",
      url:"/teacher/Reject/",
      data:{index_id:_index_id},
      success:function(result){
        console.log("success!")
        console.log(result)
        if(result.status == 1)
          alert("驳回预约！")
        else
          alert("无资格操作！")
        setTimeout(function() {
          location.reload();
        }, 1 * 2000);
        window.location.reload();
      },
      error:function(e){
        console.log(e.status);
        console.log(e.responseText);
        alert("审批操作失败！")
      }
    })
  }
});