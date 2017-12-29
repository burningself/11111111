/////////////////////////////////////////////////////////////////////
// Autodesk.ADN.Viewing.Extension.SampleTask
// by pangubing 2016.08.01
//
/////////////////////////////////////////////////////////////////////
AutodeskNamespace("Autodesk.ADN.Viewing.Extension");

Autodesk.ADN.Viewing.Extension.SampleTask = function (viewer, options) {
  
  Autodesk.Viewing.Extension.call(this, viewer, options);
  
  var _panel = null;
  
  /////////////////////////////////////////////////////////////////
  // Extension load callback
  //
  /////////////////////////////////////////////////////////////////
  this.load = function () {

    _panel = new Panel(
      viewer.container,
      guid());

    _panel.setVisible(true);

    console.log('Autodesk.ADN.Viewing.Extension.SampleTask loaded');

    return true;
  }
  
  /////////////////////////////////////////////////////////////////
  //  Extension unload callback
  //
  /////////////////////////////////////////////////////////////////
  this.unload = function () {
    
    _panel.setVisible(false);
    
    console.log('Autodesk.ADN.Viewing.Extension.SampleTask unloaded');
    
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
      function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x7 | 0x8)).toString(16);
      });
    
    return guid;
  }
  
  /////////////////////////////////////////////////////////////////
  // The demo Panel
  //
  /////////////////////////////////////////////////////////////////
  var Panel = function(
    parentContainer, id) {
    
    var _thisPanel = this;
    
    _thisPanel.content = document.createElement('div');
    
    Autodesk.Viewing.UI.DockingPanel.call(
      this,
      parentContainer,
      id,
      '图例',
      {shadow:true});
    
    $(_thisPanel.container).addClass('bootstrap-panel');
	

    /////////////////////////////////////////////////////////////
    // Custom html
    //
    /////////////////////////////////////////////////////////////
    var html = `<div class="pbwell-simaple">
						<div><label  value="未开始" style="border-radius: 14px;margin-right: 5px;width:14px;height:14px; vertical-align: middle;background-color:rgba(249,177,245,1);" onMouseOver="this.title=this.innerText"></label>未开始</div>
						<div><label  value="进行中" style="border-radius: 14px;margin-right: 5px;width:14px;height:14px; vertical-align: middle;background-color:rgba(58,132,195,1);" onMouseOver="this.title=this.innerText"></label>进行中</div>
						<div><label  value="完成" style="border-radius: 14px;margin-right: 5px;width:14px;height:14px; vertical-align: middle;background-color:rgba(80,193,58,1);" onMouseOver="this.title=this.innerText"></label>完成</div>
			  		<div><label  value="超时未完成" style="border-radius: 14px;margin-right: 5px;width:14px;height:14px; vertical-align: middle;background-color:rgba(247,228,56,1) ;" onMouseOver="this.title=this.innerText"></label>超时未完成</div>
			  		<div><label  value="超时未开始" style="border-radius: 14px;margin-right: 5px;width:14px;height:14px; vertical-align: middle;background-color:rgba(196,58,58,1) ;" onMouseOver="this.title=this.innerText"></label>超时未开始</div>
			  </div>`;

    _thisPanel.createScrollContainer({
      left: false,
      heightAdjustment: 25,
      marginTop:0
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

  
   Panel.prototype.initialize = function()
	{
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
        bottom: 15px;
        right: 15px;
        width: auto;
        height: auto;
        resize: none;
        background: rgba(34, 34, 34, 0.0);
		padding:5px;
      }
    
	 div.pbwell-simaple{
		color: #4A4A4A;

	}

    div.bootstrap-panel:hover {
      background: rgba(34, 34, 34, 0.1);
    }

    .panel-container {
      margin:15px;
    }`;

  $('<style type="text/css">' + css + '</style>').appendTo('head');
 };

Autodesk.ADN.Viewing.Extension.SampleTask.prototype =
  Object.create(Autodesk.Viewing.Extension.prototype);

Autodesk.ADN.Viewing.Extension.SampleTask.prototype.constructor =
  Autodesk.ADN.Viewing.Extension.SampleTask;

Autodesk.Viewing.theExtensionManager.registerExtension(
  'Autodesk.ADN.Viewing.Extension.SampleTask',
  Autodesk.ADN.Viewing.Extension.SampleTask);