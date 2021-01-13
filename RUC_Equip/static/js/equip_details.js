$(document).ready(function(){
  $('#equip-detail').css('display','none');
  $(document).on("click","#show-detail.btn", function() {
//$("#show-detail.btn").click(function(){
//  $(".show-detail").off().on('click',function(){
  $('#equip-detail').css('display','inline');
  _equip_id = $(this).attr("equip_id")
  $.ajax({
    type:"GET",
    contentType:"application/json;charset=UTF-8",
    url:"/teacher/EquipDetails/",
    data:{equip_id:_equip_id},
    success:function(result){
      console.log("success!")
      console.log(result)
      //var jsonData = JSON.stringify(result);// 转成string格式
      show_equip_detail(result)
    },
    error:function(e){
      console.log(e.status);
      console.log(e.responseText)
      alert("仪器详情获取失败！")
    }
  })
});

function show_equip_detail(data){
  $('#equip-detail').css('display','inline');
  //var data = eval('('+jsonData+')');
  //alert("请在页面底部查看详情")
  document.getElementById("current_equip_id").innerHTML=data.equip_id;
  document.getElementById("current_equip_name").innerHTML=data.equip_name;
  document.getElementById("current_type").innerHTML= data.type
  document.getElementById("current_email").innerHTML=data.email;
  document.getElementById("current_buy_date").innerHTML=data.buy_date;
  document.getElementById("current_description").innerHTML=data.description;
  document.getElementById("current_address").innerHTML=data.address;
  document.getElementById("current_manager_id").innerHTML=data.manager_id;
  document.getElementById("current_status").innerHTML=data.status;
  document.getElementById("current_qualification").innerHTML=data.qualification;
  document.getElementById("current_check_qualification").innerHTML=data.check_qualification;
};

});
