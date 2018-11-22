function News() {

}

News.prototype.run = function () {
    var self = this;
    self.listenUploadFilelEvent();
    self.initUEditor();
    self.listenSubmitEvent();
};

// 上传文件
News.prototype.listenUploadFilelEvent = function () {
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file',file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if(result['code'] === 200){
                    var url = result['data']['url'];
                    var thumbnailInput = $("#thumbnail-form");
                    thumbnailInput.val(url);
                    console.log(result);
                }
            }
        });
    });
};

// 富文本编辑器
News.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor',{
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });
};

// 添加新闻
News.prototype.listenSubmitEvent = function () {
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();

        var title = $('input[name="title"]').val();
        var category = $('select[name="category"]').val();
        var desc = $('input[name="desc"]').val();
        var thumbnail = $('input[name="thumbnail"]').val();
        var content = window.ue.getContent();
        console.log(content);

        xfzajax.post({
           'url':'/cms/write_news/',
           'data':{
               'title':title,
               'category':category,
               'desc':desc,
               'thumbnail':thumbnail,
               'content':content
           },
            'success':function (result) {
                if(result['code'] === 200){
                    xfzalert.alertSuccess('恭喜！新闻发表成功！',function () {
                        window.location.reload();
                    });
                }
            }
        });
    });
};

$(function () {
    var news = new News();
    news.run();
});