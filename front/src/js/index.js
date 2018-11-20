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
    this.bannerWitdh = 798;
    this.bannerGroup = $('#banner-group');//获取标签对象
    this.index = 1;//初始化轮播图编号
    this.leftArrow = $('.left-arrow');//轮播图左箭头
    this.rightArrow = $('.right-arrow');//轮播图右箭头
    this.bannerUL = $('#banner-ul');//获取标签
    this.liList = this.bannerUL.children('li');//获取li标签对象
    this.bannerCount = this.liList.length;//获取li标签个数
    this.pageControl = $('.page-control');
}

Banner.prototype.initBanner = function () {
    var self = this;

    var firstBanner = self.liList.eq(0).clone();
    var lastBanner = self.liList.eq(self.bannerCount-1).clone();
    self.bannerUL.append(firstBanner);// 添加到最后一个
    self.bannerUL.prepend(lastBanner);// 添加到第一个
    self.bannerUL.css({'width':self.bannerWitdh*(self.bannerCount+2),
    'left':-self.bannerWitdh});// 动态更改小圆点标签宽度
};

Banner.prototype.initPageControl = function () {
    var self = this;// 动态修改小圆点个数＝＝轮播图个数
    //var pageControl = $('.page-control');
    for(var i = 0; i < self.bannerCount; i++){
        var circle = $('<li></li>');
        self.pageControl.append(circle);
        if(i === 0){
            circle.addClass('active');
        }
    }
    self.pageControl.css({'width':self.bannerCount*12+8*2+16*(self.bannerCount-1)})
};// 动态修改小圆点外部div总宽度

Banner.prototype.animate = function () {
    //封装通用函数 - 轮播图
    var self = this;
    self.bannerUL.stop().animate({'left':-798*self.index},500);　//　轮播
    var index = self.index;
    if(index === 0){
        index = self.bannerCount-1;
    }else if(index === self.bannerCount+1){
        index = 0;
    }else{
        index = self.index-1;
    }
    self.pageControl.children('li').eq(index).addClass('active').siblings().removeClass('active');// 动态找到所有的兄弟节点并移除class
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

Banner.prototype.loop = function () {
    var self = this;
    // var bannerUL = $('#banner-ul');

    // bannerUL.css({'left':-798});
    // bannerUL.animate({'left':-798},500);//修改css提供过度效果
     this.timer = setInterval(function () {
        //定时器功能
        if (self.index >= self.bannerCount+1){
            self.bannerUL.css({'left':-self.bannerWitdh});
            self.index = 2;
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
            self.bannerUL.css({'left':-self.bannerCount*self.bannerWitdh});
            self.index = self.bannerCount - 1;
        }else{
             self.index--;
        }
        self.animate();
    });
    self.rightArrow.click(function () {
       if(self.index === self.bannerCount + 1){
           self.bannerUL.css({'left':-self.bannerWitdh});
           self.index = 2;
       }else{
           self.index++;
       }
       self.animate();
    });
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

Banner.prototype.listenPageControl = function () {
    // 监听li标签
    var self = this;
    self.pageControl.children('li').each(function (index,obj) {
        // console.log(index);　标签下标值
        // console.log(obj);　li标签
        $(obj).click(function () {
            self.index = index;
            self.animate();
            // $(obj).addClass('active').siblings().removeClass('active');// 找到所有的兄弟节点并移除class
        });
    });
};

Banner.prototype.run = function () {
    console.log('runing...........');
    this.initBanner();
    this.initPageControl();
    this.loop();
    this.listenArrowClick();
    this.listenBannerHover();//监听轮播图鼠标事件
    this.listenPageControl();
};

$(function () {
    var banner = new Banner();
    banner.run();//主启动函数
});