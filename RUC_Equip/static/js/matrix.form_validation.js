
$(document).ready(function(){
	
	$('input[type=checkbox],input[type=radio],input[type=file]').uniform();
	
	$('select').select2();
	
	// Form Validation
	$("#basic_validate_update").validate({
		rules:{
			equip_name:{
				required:true,
			},
			equip_id:{
				required:true
			},
			type:{
				required:true,
			},
			description:{
				required:true,
			},
			qualification:{
				required:true,
			},
			date:{
				required:true,
				date: true
			},
			address:{
				required:true,
			}
		},
		errorClass: "help-inline",
		errorElement: "span",
		highlight:function(element, errorClass, validClass) {
			$(element).parents('.control-group').addClass('error');
		},
		unhighlight: function(element, errorClass, validClass) {
			$(element).parents('.control-group').removeClass('error');
			$(element).parents('.control-group').addClass('success');
		}
	});

	$("#basic_validate_insert").validate({
		rules:{
			equip_name:{
				required:true
			},
			equip_id:{
				required:true
			},
			type:{
				required:true
			},
			description:{
				required:true
			},
			qualification:{
				required:true
			},
			buy_date:{
				required:true,
				date: true
			},
			address:{
				required:true
			}
			/*required:{
				required:true
			}
			email:{
				required:true,
				email: true
			},
			date:{
				required:true,
				date: true
			},
			url:{
				required:true,
				url: true
			}*/
		},
		errorClass: "help-inline",
		errorElement: "span",
		highlight:function(element, errorClass, validClass) {
			$(element).parents('.control-group').addClass('error');
		},
		unhighlight: function(element, errorClass, validClass) {
			$(element).parents('.control-group').removeClass('error');
			$(element).parents('.control-group').addClass('success');
		}
	});
});
