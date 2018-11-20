//点击登录按钮，弹出模态对话框

$(function () {
    $('#btn').click(function () {
        $('.mask-wrapper').show();
    });
    
    $('.close-btn').click(function () {
        $('.mask-wrapper').hide()
    })
});

// 登录注册页面　点击切换
$(function () {
   $('.switch').click(function () {
      var srcollWrapper = $('.scroll-wrapper');
      var currentLeft = srcollWrapper.css('left');
      currentLeft = parseInt(currentLeft);//解析为整型
       if(currentLeft<0){
           srcollWrapper.animate({'left':'0'});
       }else {
           srcollWrapper.animate({'left':'-400px'});
       }
   });
});