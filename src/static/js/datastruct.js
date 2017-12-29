/**
 * js模拟List
 */

 function UserList()
 {
	 this.list = new Array();

	/**
	 * 添加
	 * @param {Object} object
	 */
	this.add = function(object) {
		this.list[this.list.length] = object;
	}

	/** 
	 * 移除此列表中指定位置上的元素。 
	 * @param index 指定位置 
	 * @return 此位置的元素 
	 */
	this.removeIndex = function(index) {
		var object = this.list[index];
		this.list.splice(index, 1);
		return object;
	}

	/** 
	 * 移除此列表中指定元素。 
	 * @param object 指定元素 
	 * @return 此位置的元素 
	 */
	this.remove = function(object) {
		var i = 0;
		for (; i < this.list.length; i++) {
			if (this.list[i] === object) {
				break;
			}
		}
		if (i >= this.list.length) {
			return null;
		} else {
			return this.removeIndex(i);
		}
	}

	/** 
	 * 获得列表中指定元素。 
	 * @param object 指定元素 
	 * @return 此位置的元素 
	 */
	this.get = function(index) {  
		return this.list[index];  
	}  

	/** 
	 * 移除此列表中的所有元素。 
	 */  
	this.removeAll = function() {  
		this.list.splice(0, this.list.length);  
	}

	/** 
	 * 返回此列表中的元素数。 
	 * @return 元素数量 
	 */  
	this.size = function() {  
		return this.list.length;  
	} 
	   
	  
	/** 
	 *  如果列表不包含元素，则返回 true。 
	 * @return true or false 
	 */  
	this.isEmpty = function() {  
		return this.list.length == 0;  
	} 
	 
	 /**  
     * 重写toString   
     */  
    this.toString = function(){   
        var s = "";   
        for(var i=0;i<this.list.length;i++){   
            s += this.list[i]; 
			if(i!=this.list.length-1)
				s+=',';
        }   
        return s;   
    };   
 }

 Array.prototype.remove = function(s) {   
    for (var i = 0; i < this.length; i++) {   
        if (s == this[i])   
            this.splice(i, 1);   
    }   
}   
  
/**  
 * Simple Map  
 *   
 */  
function UserMap() {   
    /** 存放键的数组(遍历用到) */  
    this.keys = new Array();   
    /** 存放数据 */  
    this.data = new Object();   
       
    /**  
     * 放入一个键值对  
     * @param {String} key  
     * @param {Object} value  
     */  
    this.put = function(key, value) {   
        if(this.data[key] == null){   
            this.keys.push(key);   
        }   
        this.data[key] = value;   
    };   
       
    /**  
     * 获取某键对应的值  
     * @param {String} key  
     * @return {Object} value  
     */  
    this.get = function(key) {   
        return this.data[key];   
    };   
       
    /**  
     * 删除一个键值对  
     * @param {String} key  
     */  
    this.remove = function(key) {   
        this.keys.remove(key);   
        this.data[key] = null;   
    };   
       
    /**  
     * 遍历Map,执行处理函数  
     *   
     * @param {Function} 回调函数 function(key,value,index){..}  
     */  
    this.each = function(fn){   
        if(typeof fn != 'function'){   
            return;   
        }   
        var len = this.keys.length;   
        for(var i=0;i<len;i++){   
            var k = this.keys[i];   
            fn(k,this.data[k],i);   
        }   
    };   
       
    /**  
     * 获取键值数组(类似Java的entrySet())  
     * @return 键值对象{key,value}的数组  
     */  
    this.entrys = function() {   
        var len = this.keys.length;   
        var entrys = new Array(len);   
        for (var i = 0; i < len; i++) {   
            entrys[i] = {   
                key : this.keys[i],   
                value : this.data[i]   
            };   
        }   
        return entrys;   
    };   
       
    /**  
     * 判断Map是否为空  
     */  
    this.isEmpty = function() {   
        return this.keys.length == 0;   
    };   
       
    /**  
     * 获取键值对数量  
     */  
    this.size = function(){   
        return this.keys.length;   
    };   
       
    /**  
     * 重写toString   
     */  
    this.toString = function(){   
        var s = "{";   
        for(var i=0;i<this.keys.length;i++,s+=','){   
            var k = this.keys[i];   
            s += k+"="+this.data[k];   
        }   
        s+="}";   
        return s;   
    };   
}   
  
  