// function Banner() {
//     //　相当于python中的__init__方法
//     console.log('banner');
//     this.persion = 'haoge';
// }
//
// //　原型链　－　添加方法
// Banner.prototype.greet = function (word) {
//     console.log('hello',word);
// };
//
// var banner = new Banner();
// console.log(banner.persion);

function Banner() {
    this.bannerGroup = $('#banner-group');//获取标签对象
    this.index = 0;//初始化轮播图编号
    this.leftArrow = $('.left-arrow');//轮播图左箭头
    this.rightArrow = $('.right-arrow');//轮播图右箭头
    this.bannerUL = $('#banner-ul');//获取标签
    this.liList = this.bannerUL.children('li');//获取li标签对象
    this.bannerCount = this.liList.length;//获取li标签个数
    this.listenBannerHover();//监听轮播图鼠标事件

}

Banner.prototype.animate = function () {
    //封装通用函数 - 轮播图
    var self = this;
    self.bannerUL.animate({'left':-798*self.index},500);
};

Banner.prototype.toggleArrow = function (isShow) {
    //控制轮播图左右箭头的显示
    var self = this;
    if (isShow){
        // $('.left-arrow').toggle();
        // $('.right-arrow').toggle();
        // $('.left-arrow').show();
        // $('.right-arrow').show();
        self.leftArrow.show();
        self.rightArrow.show();
    }else{
        // $('.left-arrow').hide();
        // $('.right-arrow').hide();
        self.leftArrow.hide();
        self.rightArrow.hide();
    }
};

Banner.prototype.listenBannerHover = function () {
    //监听鼠标移动到轮播图事件
    var self = this;
    this.bannerGroup.hover(function () {
        console.log('鼠标移动,暂停播放...');
        //第一个函数是把鼠标移动到banner上会执行的函数
        // clearInterval(this.timer); 函数内的this对象指的是函数　不是Ｂanner对象
        clearInterval(self.timer);//关闭定时器
        self.toggleArrow(true);//显示轮播图左右箭头

    },function () {
        //第二个函数是把鼠标从banner移走会执行的函数
        console.log('鼠标移走,开始播放...');
        self.loop();
        self.toggleArrow(false);//隐藏轮播图左右箭头
    });
};

Banner.prototype.loop = function () {
    var self = this;
    // var bannerUL = $('#banner-ul');

    // bannerUL.css({'left':-798});
    // bannerUL.animate({'left':-798},500);//修改css提供过度效果
     this.timer = setInterval(function () {
        //定时器功能
        if (self.index >= 3){
            self.index = 0;
        }else{
            self.index++;
        }
       // bannerUL.animate({'left':-798*self.index},500);
         self.animate();
        },2000);//轮播
};

Banner.prototype.listenArrowClick = function () {
    //监听轮播图左右箭头事件
    var self = this;
    self.leftArrow.click(function () {
        if(self.index === 0) {
            self.index = self.bannerCount - 1;
        }else{
             self.index--;
        }
        self.animate();
    });
    self.rightArrow.click(function () {
       if(self.index === self.bannerCount -1){
           self.index = 0;
       }else{
           self.index++;
       }
       self.animate();
    });
};

Banner.prototype.run = function () {
    console.log('runing...........');
    this.loop();
    this.listenArrowClick();
};

$(function () {
    var banner = new Banner();
    banner.run();//主启动函数
});