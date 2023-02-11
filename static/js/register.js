function bindCaptchaBtnClick(){
    // 自动寻找id= captcha-btn的元素
    $('#captcha-btn').on("click",function (event){
        var $this =$(this);
        // 获取输入框的值
         var email = $("input[name='email']").val();
         if(!email){
             alert("请先输入邮箱！")  //弹出提示框
             return;
         }
         //通过js发送网络请求：ajax ASync JavaScript Json
        $.ajax({
            url:"/user/captcha",
            method:"POST",
            data: {
                "email":email
            },
            success: function (res){
                var code = res['code'];
                if (code == 200){
                    // 取消点击事件
                    $this.off("click")
                    // 取消倒计时
                    var countDown =60;
                    var timer = setInterval(function (){
                        countDown -= 1;
                        if(countDown > 0){
                            $this.text(countDown+'秒后重新发送');
                        }
                        else {
                            $this.text("获取验证码");
                            bindCaptchaBtnClick();
                            // 清楚倒计时
                            clearInterval(timer);
                        }
                    },1000);
                    alert("验证码发送成功");
                }else {
                    alert(res['message']);
                }
            }
        })
    })
}

// $(fcun)会等待网页全部加载完再执行
$(function (){
    bindCaptchaBtnClick();
    }
);