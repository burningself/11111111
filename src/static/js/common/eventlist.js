       
!function (){
    intVue();
    _app.init();
}();

$(function() {

					$('.TimeRangeCustom').daterangepicker({
						ranges: {
								'今天': [moment(), moment()],
								'昨天': [moment().subtract('days', 1), moment().subtract('days', 1)],
								'最近7天': [moment().subtract('days', 6), moment()],
								'最近30天': [moment().subtract('days', 29), moment()],
								'本月': [moment().startOf('month'), moment().endOf('month')],
								'上个月': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
							},
							locale: {
								applyLabel: '确定',
								cancelLabel: '取消',
								fromLabel: '起始时间',
								toLabel: '结束时间',
								customRangeLabel: '自定义',
								daysOfWeek: ['日', '一', '二', '三', '四', '五', '六'],
								monthNames: ['一月', '二月', '三月', '四月', '五月', '六月',
									'七月', '八月', '九月', '十月', '十一月', '十二月'
								],
								firstDay: 1,
								format: 'YYYY/MM/DD'
							},
					});
					
					

});

function intVue(){
	//Vue.component('pagination');
	
	
    _app = new Vue({
        el:"#app",
        delimiters:["[[", "]]"],
        data :{
        	 issuetype:'',
             items : [],
             issueListPending:true,
             total:0,
             //分页参数
              page:1,
              pageAll:0, //总页数,根据服务端返回total值计算
              perPage:10, //每页数量
              //筛选条件
              filterval:{
              	//   status:[],
				  stepIds:[],//问题
	              priority:[],
	              fuzefenbao:[],//负责方，数组
				  issuecategorys:[],//专业类别
	              createuser:[],
	              createtime:[],
	              deadline:[],  //时间段
				  
              }

           },
          watch:{
			filterval: {
			    handler: function (val, oldVal) { 
			    	var that = this;
			    	console.log(JSON.stringify(this.filterval.status));
			    	console.log(JSON.stringify(this.filterval.createtime));
			    	that.loadList(1);
			    },
			   deep: true
			}
        },
        methods:{
        		init:function(){
		            this.loadList(1);
		            
		        },
		        loadList:function(page){
	                var that = this;
	                that.page = page;
	                that.issueListPending=true;
	                that.items = [];
	                $.ajax({
	                    url : "/task/issue/list/",
	                    type:"post",
	                    data:{"issuetype":that.issuetype,"page":page,"perPage":that.perPage,"filterval":JSON.stringify(that.filterval)},
	                    dataType:"json",
	                    error:function(){alert('请求列表失败')},
	                    success:function(res){
	                        if (res.issuc == "true") {
	                            that.items = res.issuelist;
	                            that.perPage = res.perPage;
	                            that.pageAll = Math.ceil(res.total / that.perPage);//计算总页数
	                            that.total =res.total; 
	                        }
	                        that.issueListPending=false;
	                    }
	                });
	           },
		       clearFilter:function(){
		           	this.filterval={
		              status:[],
		              priority:[],
		              fuzefenbao:"",
		              createuser:"",
		              createtime:"",
		              deadline:"",
	              };
		         },
	            getReadHref:function(val){
	                return '/task/issue/read/'+val
	            },
                getDealHref:function(val){
	                return '/task/issue/issuedeal/'+val
	            },
                getEditHref:function(val){
	                return '/task/issue/update/?issueId='+val
	            },
	            deleteIssue(val,index){
	            var that = this;
	            	  zeroModal.confirm({
			            content: '确定删除事件吗？',
			            contentDetail: '删除后不能恢复！',
			            okFn: function() {
			               $.ajax({
			                    url : "/task/projectevents/"+val+"/",
			                    type:"delete",
			                    error:function(){alert('删除失败');},
			                    success:function(res){
			                        success_prompt("删除成功！");
			                        that.items.splice(index,1);
			                        that.total =that.total-1; 
			                        that.pageAll = Math.ceil(that.total / that.perPage);//计算总页数
	                            	
			                    }
			                });
			            }
			        });
	            	

	            },
               createEvent: function(){
                     var that = this;
                    if(that.issuetype=="xianchangqianzheng"){
                    	window.open("/task/issue/qianzhengcreate/"); 
                    }else if(that.issuetype=="gcjdksq"){
                    	window.open("/task/issue/gcjdksqcreate/"); 
                    }else if(that.issuetype=="sjbgtz"){
                    	window.open("/task/issue/sjbgtzcreate/"); 
                    }else if(that.issuetype=="bgsjba"){
                    	window.open("/task/issue/bgsjbacreate/"); 
                    }
                    else if(that.issuetype=="xietiao"){
                    	window.open("/task/issue/shiyicreate"); 
                    }
                    else if(that.issuetype=="tzhs"){
                    	window.open("/task/issue/tzhscreate"); 
                    }
                    else if(that.issuetype=="bimsh"){
                    	window.open("/task/issue/bimshcreate"); 
                    }else{
                    	window.open("/task/issue/createh?issuetype="+that.issuetype); 
                    	
                    }
                    
                },
               dateDefind () {
				    var that = this;

					$('#createTimeRange').on('apply.daterangepicker', function (ev, picker) {
					      
					      that.filterval.createtime = $('#createTimeRange').val();
					});
					
					$('#deallineTimeRange').on('apply.daterangepicker', function (ev, picker) {
					     
					      that.filterval.deadline = $('#deallineTimeRange').val();
					});

			},
          },
        mounted: function () {
		   this.dateDefind();
		}
    })
}
