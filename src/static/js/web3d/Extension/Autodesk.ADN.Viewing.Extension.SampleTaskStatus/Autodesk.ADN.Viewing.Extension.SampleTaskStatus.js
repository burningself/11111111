/////////////////////////////////////////////////////////////////////
// Autodesk.ADN.Viewing.Extension.SampleTaskStatus
// by pangubing 2016.08.01
//
/////////////////////////////////////////////////////////////////////
AutodeskNamespace("Autodesk.ADN.Viewing.Extension");

Autodesk.ADN.Viewing.Extension.SampleTaskStatus = function(viewer, options) {

	Autodesk.Viewing.Extension.call(this, viewer, options);

	var _panel = null;
	var _curUnitPrjId = "";
	var _curPbMajor = "";
	var _isWhole = false;
	/////////////////////////////////////////////////////////////////
	// Extension load callback
	//
	/////////////////////////////////////////////////////////////////
	this.load = function() {

		console.log('Autodesk.ADN.Viewing.Extension.SampleTaskStatus loaded');

		return true;
	}

	/////////////////////////////////////////////////////////////////
	//  Extension unload callback
	//
	/////////////////////////////////////////////////////////////////
	this.unload = function() {

		_panel.setVisible(false);

		console.log('Autodesk.ADN.Viewing.Extension.SampleTaskStatus unloaded');

		return true;
	}

	/////////////////////////////////////////////////////////////////
	// Generates random guid to use as DOM id
	//
	/////////////////////////////////////////////////////////////////
	function guid() {

		var d = new Date().getTime();

		var guid = 'xxxx-xxxx-xxxx-xxxx'.replace(
			/[xy]/g,
			function(c) {
				var r = (d + Math.random() * 16) % 16 | 0;
				d = Math.floor(d / 16);
				return(c == 'x' ? r : (r & 0x7 | 0x8)).toString(16);
			});

		return guid;
	}

	Autodesk.Viewing.Viewer3D.prototype.createSamplePanel = function(unitPrj, major,isWhole) {
		
			_curUnitPrjId = unitPrj;
			_curPbMajor = major;
			_isWhole = isWhole;
			
			_panel = new Panel(
			viewer.container,
			guid());

		_panel.setVisible(true);
			
	}

	/////////////////////////////////////////////////////////////////
	// The demo Panel
	//
	/////////////////////////////////////////////////////////////////
	var Panel = function(parentContainer, id) {

		var _thisPanel = this;

		_thisPanel.content = document.createElement('div');

		Autodesk.Viewing.UI.DockingPanel.call(
			this,
			parentContainer,
			id,
			'图例', {
				shadow: true
			});

		$(_thisPanel.container).addClass('bootstrap-panel');

		/////////////////////////////////////////////////////////////
		// Custom html
		//
		/////////////////////////////////////////////////////////////
		var html = "";
		$.ajax({
			type: "get",
			url: "/task/modelview/getcounttypelist",
			cache: false,
			async: false,
			dataType: "json",
			data: {
				"_curUnitId":_curUnitPrjId,
				"_curMajor":_curPbMajor,
				"_isWholeModel":_isWhole
			},
			success: function(data) {
				if(data.issuc = "true") {
					html = `<div class="pbwell-simaple">`;
					labelhtml = "<a class= 'label label-danger' style='margin-right: 5px;'  onclick='filterPbByCountType(0,this)'>全部</a>";;
					for(var each in data.counttypelist) {
						if(each == "remove")
							continue;
						html += "<div><label  value= " + data.counttypelist[each].name + " style='border-radius: 14px;margin-right: 5px;width:14px;height:14px;vertical-align: middle;background-color:" + data.counttypelist[each].color + ";opacity: 0.70;' onMouseOver='this.title=this.innerText'></label>" + data.counttypelist[each].name + "</div>";
						labelhtml+= "<a class= 'label label-default' style='margin-right: 5px;'  onclick='filterPbByCountType("+data.counttypelist[each].id+",this)'>" + data.counttypelist[each].name + "</a>";
					}
					
					console.log(labelhtml);
					$("#labelCountType").html(labelhtml);

				}
			}
		});

		_thisPanel.createScrollContainer({
			left: false,
			heightAdjustment: 25,
			marginTop: 0
		});

		$(_thisPanel.scrollContainer).append(html);

		/////////////////////////////////////////////////////////////
		// initialize override
		//
		/////////////////////////////////////////////////////////////
		_thisPanel.initialize = function() {

			this.title = this.createTitleBar(
				this.titleLabel ||
				this.container.id);

			this.closer = this.createCloseButton();

			this.container.appendChild(this.title);
			this.title.appendChild(this.closer);
			this.container.appendChild(this.content);

			this.initializeMoveHandlers(this.title);
			this.initializeCloseHandler(this.closer);
		};

	};

	/////////////////////////////////////////////////////////////
	// Set up JS inheritance
	//
	/////////////////////////////////////////////////////////////
	Panel.prototype = Object.create(
		Autodesk.Viewing.UI.DockingPanel.prototype);

	Panel.prototype.constructor = Panel;

	Panel.prototype.initialize = function() {
		// Override DockingPanel initialize() to:
		// - create a standard title bar
		// - click anywhere on the panel to move
		// - create a close element at the bottom right
		//
		//	this.title = this.createTitleBar(this.titleLabel || this.container.id);
		//	this.container.appendChild(this.title);
		//
		//	this.container.appendChild(this.content);
		this.initializeMoveHandlers(this.container);
		//
		//	this.closer = document.createElement("div");
		//	this.closer.className = "simplePanelClose";
		//	this.closer.textContent = "Close";
		//	this.initializeCloseHandler(this.closer);
		//	this.container.appendChild(this.closer);
	};

	/////////////////////////////////////////////////////////////
	// Add needed CSS
	//
	/////////////////////////////////////////////////////////////
	var css = `
     div.bootstrap-panel {
        bottom:15px;
        right:5px;
        width: auto;
        height: auto;
        resize: none;
        background: rgba(34, 34, 34, 0.0);
		padding:5px;
      }
    
	 div.pbwell-simaple{
		color: #333333;
	}

	.dockingPanel{
		    min-height:0px;
	}
	
    div.bootstrap-panel:hover {
      background: rgba(34, 34, 34, 0.1);
    }

    .panel-container {
      margin:15px;
    }`;

	$('<style type="text/css">' + css + '</style>').appendTo('head');
};

Autodesk.ADN.Viewing.Extension.SampleTaskStatus.prototype =
	Object.create(Autodesk.Viewing.Extension.prototype);

Autodesk.ADN.Viewing.Extension.SampleTaskStatus.prototype.constructor =
	Autodesk.ADN.Viewing.Extension.SampleTaskStatus;

Autodesk.Viewing.theExtensionManager.registerExtension(
	'Autodesk.ADN.Viewing.Extension.SampleTaskStatus',
	Autodesk.ADN.Viewing.Extension.SampleTaskStatus);