/***
 *  @author misaka
 *  @date 2017/12/6
 */
var MEditor = {
    template:`
    <Tooltip content="单击编辑" v-if="!edit" @click.native="edit=true" placement="top">
        <span class="m-span"><slot></slot></span>
    </Tooltip>
    <div v-else-if="type=='input'">
            <Input class="c-input" v-model="currentValue" :type="inputType" @keydown.native.enter="close" :autofocus="true"/></Input>
            <Button class="c-btn"  type="text" icon="checkmark-round" @click="close"></Button>
            <Button class="c-btn-red" type="text" icon="close-round" @click="cancelClose"></Button>
    </div>
    <div  v-else-if="type=='select'">
         <i-select
            class="c-input" 
            v-model="selectValue"
            :label-in-value="true"
            :filterable="filterable"
            :multiple="multiple"
            :loading="loading"
            @on-query-change = 'onQuery'
            @on-change="changeSelect">
            <i-option v-for="item in List" :value="item.url" :key="item.id">{{item.name}}</i-option>
    </i-select>
     <i-button class="c-btn"  type="text" icon="checkmark-round" @click="closeSelect(changeData)"></i-button>
     <i-button class="c-btn-red" type="text" icon="close-round" @click="closeSelect(0)"></i-button>
    </div>
    `,
    props:{
        List:{
            type:Array,
            default: function () {
                return []
            }
        },
        value:{
            type:[String,Number,Object,Array]
        },
        seleValue:{
            type:[String,Number,Object,Array]
        },
        type:{
            type:String,
            validator(value){
                return ['input','select'].indexOf(value)>-1;
            },
            default:'input'
        },
        inputType:{
            type:String,
            default:'text'
        },
        filterable:{
            type:Boolean,
            default:false
        },
        multiple:Boolean,
        loading:{
            type:Boolean,
            default:false
        }
    },
    data(){
        return {
            edit:false,
            originalData:null,
            currentValue:this.value,
            currentSelectValue:this.value,
            selectValue: this.seleValue,
            changeData:null
        };
    },
    methods:{
        close(){
            this.edit = false;
            this.$emit('input',this.currentValue);
            this.originalData = this.currentValue;
        },
        cancelClose (){
            this.edit = false;
            this.$emit('input',this.originalData);
            this.currentValue = this.originalData;
        },
        changeSelect(value){
            this.changeData = value;
        },
        closeSelect(value){
            if(!this.multiple){
                this.edit = false;
            }
            if( value == 0 || this.changeData == null ){
                this.$emit('input',this.seleValue);
                this.selectValue = this.seleValue;
                this.changeData = null;
            }else {
                this.$emit('input',value);
            }
        },
        onQuery(value){
            this.$emit('on-query',value);
        },
        finish(){
            this.edit = false;
        }
    },
    mounted(){
        let style=document.createElement('style');
        style.type='text/css';
        style.href='style.css';
        style.textContent = '.m-span:hover{background-color: lightgoldenrodyellow;}';
        document.getElementsByTagName('head')[0].appendChild(style);
        this.originalData = this.value;
    }
};
