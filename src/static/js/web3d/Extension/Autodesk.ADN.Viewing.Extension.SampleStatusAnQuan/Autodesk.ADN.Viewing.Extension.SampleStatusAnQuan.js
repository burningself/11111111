/////////////////////////////////////////////////////////////////////
// Autodesk.ADN.Viewing.Extension.SampleStatusAnQuan
// by pangubing 2016.08.01
//
/////////////////////////////////////////////////////////////////////
AutodeskNamespace("Autodesk.ADN.Viewing.Extension");

Autodesk.ADN.Viewing.Extension.SampleStatusAnQuan = function (viewer, options) {
  
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

    console.log('Autodesk.ADN.Viewing.Extension.SampleStatusAnQuan loaded');

    return true;
  }
  
  /////////////////////////////////////////////////////////////////
  //  Extension unload callback
  //
  /////////////////////////////////////////////////////////////////
  this.unload = function () {
    
    _panel.setVisible(false);
    
    console.log('Autodesk.ADN.Viewing.Extension.SampleStatusAnQuan unloaded');
    
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
      '图例');
    
    $(_thisPanel.container).addClass('sample-bootstrap-panel');
	$('#' + id).css({
      'min-width': 120 + 'px',
      'min-height':60 + 'px',
    });

    /////////////////////////////////////////////////////////////
    // Custom html
    //
    /////////////////////////////////////////////////////////////
	  var html = "";	   
	  html = "<div class='pbwell-simaple'>";
		html += "<div><label  value= '安全告警' style='border-radius: 14px;margin-right: 5px;width:14px;height:14px; vertical-align: middle;margin-bottom:4px;background-color:#ED002F;opacity: 0.70;' onMouseOver='this.title=this.innerText'></label>安全告警</div>";
		html += "<div><label  value= '危险源' style='border-radius: 14px;margin-right: 5px;width:14px;height:14px; vertical-align: middle;margin-bottom:4px;color:#9C02A7;background-color:#BAF300;opacity: 0.70;' onMouseOver='this.title=this.innerText'></label>危&nbsp;险&nbsp;源</div>";
		html += "<div><label  value= '安全检查' style='border-radius: 14px;margin-right: 5px;width:14px;height:14px; vertical-align: middle;margin-bottom:4px;background-color:#00A779;opacity: 0.70;' onMouseOver='this.title=this.innerText'></label>安全检查</div>";
		html += "</div>";
			
	
    _thisPanel.createScrollContainer({
      left: false,
      heightAdjustment: 0,
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
 var css = [

     'div.sample-bootstrap-panel {',
        'right: 15px;',
        'bottom: 15px;',
        'width: auto;',
        'height: auto;',
        'resize: none;',
        'background: rgba(34, 34, 34, 0.0);',
		//box-shadow: none;
      '}',
    
	'div.sample-bootstrap-panel:hover {',
		'background: rgba(34, 34, 34, 0.1);',
	'}',
	
	 'div.pbwell-simaple{',
		'color: #333333;',
		'font-size:14px;',
		'text-align: left;',
    'margin-left: 10px;',
	'}',

    'div.bootstrap-panel:hover {',
      'background-color: #F1F1F1;',
    '}',

    '.panel-container {',
      'margin:15px;',
    '}',
	].join('\n');
	

  $('<style type="text/css">' + css + '</style>').appendTo('head');
 };

Autodesk.ADN.Viewing.Extension.SampleStatusAnQuan.prototype =
  Object.create(Autodesk.Viewing.Extension.prototype);

Autodesk.ADN.Viewing.Extension.SampleStatusAnQuan.prototype.constructor =
  Autodesk.ADN.Viewing.Extension.SampleStatusAnQuan;

Autodesk.Viewing.theExtensionManager.registerExtension(
  'Autodesk.ADN.Viewing.Extension.SampleStatusAnQuan',
  Autodesk.ADN.Viewing.Extension.SampleStatusAnQuan);