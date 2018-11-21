function News() {

}

News.prototype.run = function () {
    var self = this;
    self.listenUploadFilelEvent();
    self.initUEditor();
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
    var ue = UE.getEditor('editor');
};

$(function () {
    var news = new News();
    news.run();
});