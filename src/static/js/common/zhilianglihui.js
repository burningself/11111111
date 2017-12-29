$(document).ready(function(){
    huiyi_list.init();
});

var huiyi_list = {
    commonModal_title : $("#commonModal_title"),
    commonModal_desc : $("#commonModal_desc"),
    jiyaofileStr:'',

    init : function(){
        var that = this;
        that.bindListener();
        that.uploadfileinit();
    },

    uploadfileinit:function(){
        var that = this;
        $('#uploadfile_jiyao').filer({
            showThumbs: true,
            addMore: true,
            fileMaxSize:50,
			limit:10,
            allowDuplicates: false,
            captions:{
                button: "添加文件",
                feedback: "",
                feedback2: "个文件已选择",
                drop: "拖到文件到这里",
                removeConfirmation: "确定删除该文件吗？",
                errors: {
                    filesLimit: "只能同时上传 {{fi-limit}}个文件 。",
                    filesType: "只能上传MicrosoftProject文件",
                    filesSize: "{{fi-name}} 太大! 最大允许上传 {{fi-fileMaxSize}} MB。",
                    filesSizeAll: "Files you've choosed are too large! Please upload files up to {{fi-maxSize}} MB。",
                    folderUpload: "不允许上传文件夹。"
                }
            },
            uploadFile: {
                url: "/uploadfile_conc2/",
                data: null,
                type: 'POST',
                enctype: 'multipart/form-data',
                beforeSend: function(){},
                success: function(data, el){
                    if (data.issuc=="true"){
                        el.attr("value",data.docId);
                        if(that.jiyaofileStr==""){
                            that.jiyaofileStr+=data.docId;
                        }else{
                            that.jiyaofileStr+=','+data.docId;
                        }
                    }
                },
                error: function(el){},
                statusCode: null,
                onProgress: null,
                onComplete: null
            },
            onRemove: function(itemEl, file){
                var fileid = itemEl.attr("value")
                $.post('/del_uploadfile/', {fileid: fileid});
            }
        });
    },

    bindListener : function(){
        var that = this;
        $("#truedelhuiyi").bind("click",function(){
            that.delhuiyifunc();
        });

        $("#addjiyaofile").bind("click",function(){
            var meetid = $("#currhyid").val();
            that.addjiyaofile(meetid);
        });
    },

    uploadjiyao:function(obj){
    	$(".icon-jfi-trash").click()//清空附件插件
        var that = this;
        $("#currhyid").val(obj);
        $("#jiyaodlg").modal("show");
    },
    addjiyaofile: function(obj) {
    	var that = this;
    	if(that.jiyaofileStr.length==0){
    		alert("请先添加纪要文件！");
    		return;
    	}


        $.ajax({
            type: "get",
            url: "/assist/uploadJiyao/",
            dataType: "json",
            data: { documents: that.jiyaofileStr, meetid: obj },
            success: function(data) {
                that.jiyaofileStr = '';
                if (data.issuc == "true") {
                	alert("上传纪要成功！");
                	window.location.reload();
                    $("#jiyaodlg").modal("hide");
                } else {}

            }
        });
    },

    deletehuiyi : function(obj){
        var that = this;
        $("#currhyid").val(obj)
        $("#deletehuiyiModal").modal("show");
    },

    huiyiinfo : function(mid){
        var that = this;
        $("#hyinfo_files").html("")
        $.ajax({
            type: "get",
            url: "/assist/loadHuiyiInfo/",
            dataType: "json",
            data: { meetid:mid},
            success: function(data) {
                if(data.issuc=='true'){
                	JSON.str
                    $("#hyinfo_name").val(data.meetinginfo.name);
                    $("#hyinfo_member").val(JSON.stringify(data.meetinginfo.members.map(function (obj) { return obj.name })));
                    $("#hyinfo_type").val(data.meetinginfo.meetingtypename);
                    $("#hyinfo_zhuti").val(data.meetinginfo.description);
                    $("#hyinfo_room").val(data.meetinginfo.roomname);
                    $("#hyinfo_begintime").val(data.meetinginfo.start);
                    $("#hyinfo_endtime").val(data.meetinginfo.end);
                    $("#hyinfo_files").val(data.meetinginfo.files);
                    var files = data.meetinginfo.files;
                    if(files.length>0){
                        var filestr = '<tbody>';
                        for(var i=0;i<files.length;i++){
                            var fileitem = files[i];
                            filestr+='<tr>';
                            var filenamestr = fileitem.filename;
                            if(filenamestr.length>15){
                                filenamestr = filenamestr.substring(0,15)+"..."
                            }
                            if(fileitem.isrecord=="1"){
                                filestr+='<td style="width: 75%;text-align: left;"><a href="/'+fileitem.filepath+'" style="cursor: pointer; target="_blank"">'+filenamestr+'(纪要)</a></td>';
                            }else{
                                filestr+='<td style="width: 75%;text-align: left;"><a href="/'+fileitem.filepath+'" style="cursor: pointer;" target="_blank">'+filenamestr+'</a></td>';
                            }
                            filestr+='<td><a href="/'+fileitem.filepath+'" title="查看文件" style="cursor: pointer;" target="_blank">[查看]</a></td>';
                            filestr+='</tr>';
                        }
                        filestr += '</tbody>';
                        $("#hyinfo_files").html(filestr);
                    }
                    $("#huiyidetail").modal("show");
                }else{
                    that.commonModal_title = "会议信息";
                    that.commonModal_desc = "加载会议信息异常";
                    $("#common_show").modal("show");
                }
            },
            error: function(data) {}
        });
    },

    delhuiyifunc : function(){
        $.ajax({
            type: "get",
            url: "/assist/deleteMeeting/",
            dataType: "json",
            data: { meetid:$("#currhyid").val()},
            success: function(data) {
                $("#deletehuiyiModal").modal("hide");
                window.location.reload();
            },
            error: function(data) {}
        });
    }
}
