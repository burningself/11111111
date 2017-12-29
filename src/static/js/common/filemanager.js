
$(function () {
	var height = $(window).height() - 129;
	
	 elFinder.prototype.i18.en.messages['cmddownloadcustom'] = '下载';          
				elFinder.prototype._options.commands.push('downloadcustom');
				elFinder.prototype.commands.downloadcustom = function() {
					var self  = this,
					fm    = self.fm;
					this.exec = function(hashes) {
						var fm = this.fm;
						var files = this.files(hashes);
						
						if(files.length==1&&files[0].dirs!=1){
							var a = document.getElementById("downhref");  
							a.href=files[0].url;  
							a.download=files[0].name;  
							a.click();  
							return;
						}
						
						//js方法  
						for(i=0;i<files.length;i++)
						{
							if(files[i].dirs==1)
							{
								var dirId =files[i].hash.split("_")[0];
								$.ajax({
									type: "get",
									url:"/task/ziliao/dirdownload/",
									cache: false,
									async: false,
									dataType: "json",
									data: {"dirId":dirId},
									success: function(data) {
										if(data.issuc == "true" ) {
											 var a = document.getElementById("downhref");  
										     a.href=data.url;  
										     a.download=files[i].name+".zip";  
										     a.click();  
										}else{
											alert(data.error);
										}
									}
								});
								break;	
							}else{
								 var a = document.getElementById("downhref");  
							     a.href=files[i].url;  
							     a.download=files[i].name;  
							     a.click();  
							}
						}

					}
					this.getstate = function(sel) {
						//return 0 to enable, -1 to disable icon access
						var fm = this.fm;
						var sel = sel || fm.selected();
						sel = this.files(sel);
				
						cnt = sel.length;
						if (cnt < 1) {
							return -1;
						}
						
						var hasDir = false;
						var hasFile = false;
						for(i=0;i<cnt;i++)
						{
							if(sel[i].dirs==1){
								hasDir = true;
							}else{
								hasFile = true;
							}
						}
						
						if(hasDir&&hasFile){
							return -1;
						}

						// Rule 1 and 2 exclude itself. By this I mean that rule nr 2
						// takes precedence over rule nr 1, so you just need to check
						// if the selected hash is a root folder.
						result=0;

						return result;
					}
				}
			
		 elFinder.prototype.i18.en.messages['cmduploadcustom'] = '上传文件';          
				elFinder.prototype._options.commands.push('uploadcustom');
				elFinder.prototype.commands.uploadcustom = function() {
					var self  = this,
					fm    = self.fm;
					this.exec = function(hashes) {
						var dirId = $('#elfinder')[0].elfinder.cwd().hash.split("_")[0];
						window.open("/task/ziliao/uploadview/?uploaddir="+dirId);
					}
					this.getstate = function(sel) {
						//return 0 to enable, -1 to disable icon access
						var fm = this.fm;
						var sel = sel || fm.selected();
						sel = this.files(sel);
				
						cnt = sel.length;
						if (cnt != 1) {
							return -1;
						}
						
						for(i=0;i<cnt;i++)
						{
							if(sel[i].dirs==1){
								if(sel[i].write==1){
									return 0;
								}else{
									return -1;
								}
								
							}else{
								return -1;
							}
								
						}
						result=-1;

						return result;
					}
				}
				
			elFinder.prototype.i18.en.messages['cmdhisversion'] = '查看历史版本';          
				elFinder.prototype._options.commands.push('hisversion');
				elFinder.prototype.commands.hisversion = function() {
					var self  = this,
					fm    = self.fm;
					this.exec = function(hashes) {
						var fileId = hashes[0].split("_")[0];
						window.open("/task/ziliao/filehisversion/?fileId="+fileId);
					}
					this.getstate = function(sel) {
						//return 0 to enable, -1 to disable icon access
						
						// Rule 1 and 2 exclude itself. By this I mean that rule nr 2
						// takes precedence over rule nr 1, so you just need to check
						// if the selected hash is a root folder.
						var fm = this.fm;
						var sel = sel || fm.selected();
						sel = this.files(sel);
				
						cnt = sel.length;
						if (cnt != 1) {
							return -1;
						}
						
						for(i=0;i<cnt;i++)
						{
							if(sel[i].dirs==1)
								return -1;
						}

						result=0;

						return result;
					}
				}
	// 修改关联元素
			elFinder.prototype.i18.en.messages['cmdeditmessage'] = '修改信息';          
						elFinder.prototype._options.commands.push('editmessage');
						elFinder.prototype.commands.editmessage = function() {
							var self  = this,
							fm    = self.fm;
							this.exec = function(hashes) {
								var fileId = hashes[0].split("_")[0];
								edit_content( fileId );
							}
							this.getstate = function(sel) {
								//return 0 to enable, -1 to disable icon access
								// Rule 1 and 2 exclude itself. By this I mean that rule nr 2
								// takes precedence over rule nr 1, so you just need to check
								// if the selected hash is a root folder.
								var fm = this.fm;
								var sel = sel || fm.selected();
								sel = this.files(sel);
						
								cnt = sel.length;
								if (cnt != 1) {
									return -1;
								}
								
								for(i=0;i<cnt;i++)
								{
									if(sel[i].dirs==1)
										return -1;
								}

								result=0;

								return result;
							}
						}
			function edit_content( fileId ) {
				 zeroModal.show({
			            title: '修改信息',
			            iframe: true,
			            url: '/task/ziliao/editproperty/?fileId='+fileId,
			            width: '80%',
			            height: '80%'
			        });
		    }	


			elFinder.prototype.i18.en.messages['cmdpreview'] = '查看图纸';          
				elFinder.prototype._options.commands.push('preview');
				elFinder.prototype.commands.preview = function() {
					var self  = this,
					fm    = self.fm;
					this.exec = function(hashes) {
						var fileId = hashes[0].split("_")[0];
						window.open("/task/ziliao/previewfile/?fileId="+fileId);
					}
					this.getstate = function(sel) {
						//return 0 to enable, -1 to disable icon access
						
						// Rule 1 and 2 exclude itself. By this I mean that rule nr 2
						// takes precedence over rule nr 1, so you just need to check
						// if the selected hash is a root folder.
						var fm = this.fm;
						var sel = sel || fm.selected();
						sel = this.files(sel);
				
						cnt = sel.length;
						if (cnt != 1) {
							return -1;
						}
						
						for(i=0;i<cnt;i++)
						{
							if(sel[i].dirs==1)
								return -1;
						}

						if(sel[0].mime!="application/dwg")
							return -1;

						result=0;

						return result;
					}
				}

	var startPathHash = $("#startPathHash").val();
	var rememberLastDir = false;
	if($("#startPathHash").val()){
		rememberLastDir = false;
	}
	
	$('#elfinder').elfinder({
					url : '/task/ziliao/connector/',  // connector URL (REQUIRED)
					lang: 'zh_CN',                    // language (OPTIONAL)
					urlUpload:'/task/ziliao/connector_upload/',
					height:height,
					rememberLastDir:rememberLastDir,
					startPathHash : startPathHash,
			    uiOptions: {
					// toolbar configuration
							toolbar : [
							['back', 'forward'],
							['home','reload'],
							['mkdir', 'uploadcustom'],
							['open', 'downloadcustom', 'getfile'],
							['info', 'quicklook'],
							['copy', 'cut', 'paste'],
							['rm'],
//							['duplicate', 'rename'],
							['view', 'sort'],
							// ['search'],
							// extra options
							{
								// auto hide on initial open
								autoHideUA: ['Mobile']
							}
						],
					cwd : {
								// display parent folder with ".." name :)
								oldSchool : false,
								
								// fm.UA types array to show item select checkboxes e.g. ['All'] or ['Mobile'] etc. default: ['Touch']
								showSelectCheckboxUA : ['Touch'],
								
								// file info columns displayed
								listView : {
									// name is always displayed, cols are ordered
									// e.g. ['perm', 'date', 'size', 'kind', 'owner', 'group', 'mode']
									// mode: 'mode'(by `fileModeStyle` setting), 'modestr'(rwxr-xr-x) , 'modeoct'(755), 'modeboth'(rwxr-xr-x (755))
									// 'owner', 'group' and 'mode', It's necessary set volume driver option "statOwner" to `true`
									columns : ['date', 'remark','size', 'kind'],
									// override this if you want custom columns name
									// example
									// columnsCustomName : {
									//		date : 'Last modification',
									// 		kind : 'Mime type'
									// }
									columnsCustomName : {
										
								  },
									// fixed list header colmun
									fixedHeader : true
								}
							},	
						},
						commands : [
							'custom','open', 'opendir', 'reload', 'home', 'up', 'back', 'forward', 'getfile', 'quicklook', 
							'downloadcustom', 'rm',  'mkdir', 'mkfile', 'uploadcustom', 'copy', 
							'cut', 'paste', 'edit', 'extract', 'archive', 'search', 'info', 'view', 'help',
							'resize', 'sort', 'places', 'chmod','zipdl','hisversion','editmessage','preview'
						],
					contextmenu : {
							// navbarfolder menu
							navbar : ['open', 'downloadcustom', '|', 'uploadcustom', '|', 'copy', 'cut', 'paste', '|', 'rm', '|', 'rename', '|', 'archive', '|', 'places', 'info', 'chmod', 'netunmount'],
							// current directory menu
							cwd    : ['reload', 'back', '|', 'uploadcustom', 'mkdir', 'mkfile', 'paste', '|', 'sort', '|', 'info'],
							// current directory file menu
							files  : ['getfile', '|' ,'custom','open', 'downloadcustom', 'opendir', 'quicklook','preview', 'hisversion','|', 'uploadcustom', 'mkdir', '|', 'copy', 'cut', 'paste', '|', 'rm', '|',  'info', 'chmod','editmessage']
						},

				});
				
				
	
});




