 // 1.创建一个组件构造器
var pagination = Vue.extend({
        template:`<div id="paginationTpl">
				    <nav v-if="all > 1">
				        <ul class="pagination">
				            <li v-if="showFirst"><a href="javascript:" v-on:click="cur--">&laquo;</a></li>
				            <li v-for="index in indexes"  :class="{ 'active': cur == index}">
				                <a v-on:click="btnClick(index)" href="javascript:">[[index]] </a>
				            </li>
				            <li v-if="showLast"><a v-on:click="cur++" href="javascript:">&raquo;</a></li>
				            <li><a>共[[all]]页</a></li>
				        </ul>
				    </nav>
				</div>`,
        delimiters:["[[", "]]"],
        replace:true,
        props:['cur','all','pageNum'],
        methods:{
            //页码点击事件
            btnClick: function(index){
                if(index != this.cur){
                    this.cur = index;
                }
            }
        },
        watch:{
            "cur" : function(val,oldVal) {
                //this.$dispatch('page-to', val);
                this.$emit('page-to',val)
            }
        },
        computed:{
            indexes : function(){
                var list = [];
                //计算左右页码
                var mid = parseInt(this.pageNum / 2);//中间值
                var left = Math.max(this.cur - mid,1);
                var right = Math.max(this.cur + this.pageNum - mid -1,this.pageNum);
                if (right > this.all ) { right = this.all}
                while (left <= right){
                    list.push(left);
                    left ++;
                }
                return list;
            },
            showLast: function(){
                return this.cur != this.all;
            },
            showFirst: function(){
                return this.cur != 1;
            }
        }
    })
        
// 2.注册组件，并指定组件的标签，组件的HTML标签为<pagination>
Vue.component('pagination',pagination);
    

