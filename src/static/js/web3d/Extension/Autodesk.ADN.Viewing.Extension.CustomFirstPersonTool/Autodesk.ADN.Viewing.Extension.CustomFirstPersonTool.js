//使用方法：
//js 调用yaogan()
//html 加<canvas id="joystick" width="150" height="150" style="position: absolute;left: 5px;bottom: 40px;z-index: 200;"></canvas>
AutodeskNamespace("Autodesk.ADN.Viewing.Extension");

Autodesk.ADN.Viewing.Extension.CustomFirstPersonTool = 

 function (viewer, options) {

    Autodesk.Viewing.Extension.call(this, viewer, options);
	var _self = this;
	_self.tool = null;
	

	function AdnTool2(viewerapi, toolName) {
		var avp = Autodesk.Viewing.Private;

		var _isMac = (navigator.userAgent.search("Mac OS") != -1);
		var _navapi = viewerapi.navigation;
		var _container = viewerapi.container;
		var _camera = _navapi.getCamera();
		var _names = ["firstperson"];

		var _modifierState = {
			SHIFT: 0,
			ALT: 0,
			CONTROL: 0
		}; // TODO: Use the hotkeymanager for these.
		var _keys = Autodesk.Viewing.theHotkeyManager.KEYCODES;

		var _isActive = false;

		// true to disable mouse & keyboard navigation.  Used when a HUD is visible to simulate
		// a modal dialog.
		var _ignoreMouseAndKeyNav = false;

		// if true then mouse drag changes view orientation, otherwise just mouse move.
		// If this is set to false then auto-tracking is enabled which might be a usability
		// issue depending on where the cursor is locate when the tool is enabled.
		// Movement is based on the distance the cursor is located from the center of
		// the screen.  If the cursor is away from center when the tool is enabled then
		// in auto-tracking (non-drag) mode the camera will begin moving.  This may be
		// disconcerting to the user.
		var _mouseDraggingLookMode = true;

		var _isDragging = false;
		var _mouseButtons = 0;
		var _touchType = null;

		var _clock = new THREE.Clock(true);

		var _hudMessageStartShowTime = -1;
		var _hudMessageShowTime = 5000; // milliseconds to show HUD

		var _modelUnitScale = 1.0; // meters
		var _modelScaleFactor = 1.0;

		// These values define how fast/slow the camera movements are made.
		// Adjust these to fine tune the movement.
		var _movementSpeedDefault = 2.0;
		var _movementSpeed = 2.0;
		var _wheelMovementSpeed = 1.0;
		var _verticalMovementSpeed = 0.5;
		var _lookSpeed = 0.0035;

		// Distance from middle of screen (non-drag) or start position (drag) that's
		// considered a neutral no-move zone when in non-drag movement mode.
		var _neutralZoneDist = 40;

		var _wheelDelta = 0;

		// Current cursor
		var _mouseXstart = 0,
			_mouseDX = 0,
			_lastX = -1e20;
		var _mouseYstart = 0,
			_mouseDY = 0,
			_lastY = -1e20;

		// Limits on mouse distance to throttle look speed
		var _mouseXMaxLimit = 400;
		var _mouseYMaxLimit = 400;

		// Relative movement
		var _deltaYaw = 0;
		var _deltaPitch = 0;

		// Key movement flags
		var _moveForward = false;
		var _moveBackward = false;
		var _moveLeft = false;
		var _moveRight = false;
		var _moveUp = false;
		var _moveDown = false;

		// Previous FOV and Perspective settings
		var _previousFov = _camera.fov;
		var _restorePreviousFov = false;

		var _wasPerspective = _camera.isPerspective;
		var _restorePreviousPerspective = false;

		// Help HUD
		var _bDontShowAgain_HelpHUD = false;

		//gamepad
		var _gamepadModule;
		//if this browser supports gamepad, instantiate GamepadModule
		if(navigator.getGamepads || !!navigator.webkitGetGamepads || !!navigator.webkitGamepads) {
			_gamepadModule = new Autodesk.Viewing.Extensions.GamepadModule(viewerapi);
		}
		// ToolInterface
		Autodesk.Viewing.Viewer3D.prototype.changSpeed = function(speed) {
			_movementSpeed = speed;
		}
		Autodesk.Viewing.Viewer3D.prototype.changeDirection = function(direction) {
			_moveForward = false;
			_moveBackward = false;
			_moveLeft = false;
			_moveRight = false;
			if(direction){
				eval(direction+'= true');
			}
			
		}
		this.isActive = function() {
			return _isActive;
		};

		this.getNames = function() {
            return [toolName];
		};

		this.getName = function() {
            return toolName;
		};

		this.activate = function(name) {
			_clock.start();

			// Switch to perspective
			_wasPerspective = _camera.isPerspective;
			_navapi.toPerspective();

			// Change FOV to a wide value for a better 1st person experience
			_previousFov = _camera.fov;
			//_navapi.setVerticalFov(75, true);

			// Unit scale
			_modelUnitScale = viewerapi.model.getUnitScale();

			// Calculate a movement scale factor based on the model bounds.
			var boundsSize = viewerapi.model.getBoundingBox().size();
			_modelScaleFactor = Math.max(Math.min(Math.min(boundsSize.x, boundsSize.y), boundsSize.z) / 10.0, 0.0001);

			// HACK: Place focus in canvas so we get key events.
			viewerapi.canvas.focus();

			_isActive = true;

			// Display the HUD on startup but only if "don't show me again" wasn't requested
			if(viewerapi.getFirstPersonToolPopup() && !_bDontShowAgain_HelpHUD) {
				// showHelpHUD();
			}

			addCrosshair();

			if(_gamepadModule) {
				_gamepadModule.activate(this.getName());
			}
		};

		this.deactivate = function(name) {
			_isActive = false;

			_clock.stop();

			hideHUD();
			removeCrosshair();

			if(_restorePreviousFov) {
				_navapi.setVerticalFov(_previousFov, true);
			}

			if(_restorePreviousPerspective) {
				if(!_wasPerspective)
					_navapi.toOrthographic();
			}

			if(_gamepadModule)
				_gamepadModule.deactivate();

		};

		this.getCursor = function() {
			return "url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3goOFQoQszohGAAAA9hJREFUSMedll1oHGUUhp8zuzP5291pEvNTomgVjFCCCa0NpAqJEJTUFVv8uWxQLwKCF6IUr7wJ6J30QvBCAlZssA0EkYJaAm1FwU3iakrbVNNuutlukk3dzWyT/ZnJ7ufFTtokbmvX72Y45+N73/Oe8858I+xYSikBJJFI7AmFQh9alvVWoVC47vP5ho4cOXJeRGwqWN4yOQ2oHh0dPROJRNo7OjqIRCKPRxeiP66srBxSSn0vIsX/RaCU0gDV399vNjQ0tB8/fpxAIEAsFuP06dPEYrFvgHqguEMxIqLKdUPbmnArU52dnb2maWJUGeRyOWzbpqGxgXg87gOMncDlwLe2Y5uCwcHBFp/P90k4PE349xkWolGi0SjhPy5hF+UmIEopz/1AtxRcqmJzDQ8P7750+Wq8e9+TPGLe4sSp39jz9LMsxm/izE6gOVnquoIcOHDgnddfe/VEU3PLWkUzSCQSesCzxNtvHKZu11O0137OuTMneYY1+l+px99sci5zgU+/Pv/Z5OTkWeCvigja2tqqri3/RPbiMfSWLvY+/wJ7XwxCOoyz+gPF5C0OzsFZv8NEOOxU7KL5+fkcooFUo9avYt+4htTU43noJVTmIPYvp8hnChSKCr/fr1VMkEqlCgEATUDTAIVykhSWRtj4M4/KKzZ9Z9u2ehCCbVUYhlEaurg7m09NB/GWYhe2r69vV8UEvb29DeIWL+6uIG6w6b1SGAqF0hUTZDKZ7GLKy1w0h+Z1keQuMEDOKbK+oZFIJOyKZqCUEsuy/k4mk6kr0ZH6/Z2CkrttEl1QjuJkKI3z6KGp6vTFpYoVmKaZ9Xg8lleDoq3IzOdBILuygbVgs2YVSNrgOM7o1NTURkUE7qufX15evo5A0VHcnrNRgFgFJF6gsVmntlaIxWKNIlK/s8D/VCAianZ29spmv0vfVoVuaNT6PYhWMpGIGIZhNAGtQC3bbXDfj51YlrWObHeOKu3didfX1x3btgGqgADgu5eafyXT6XT2zmDLnVDg9Xq9uq573fMeQAeqy+HtTAgguq7h0aUsgyZCJpPZcBxnE1xz3fhACqp7enoe+3ZimVg8j6ELiIACEUETWErnsCwrD2h1dXW6C+4A2a033T0VfPD+e8dePvoFb36sM/LzKomkQ1FgMW3z7neL3Gh6jtbW1rmamhrDNM0NYAVIAYWyl06ZPwoNeHh6evqJmZmZiV8vnCBw+yLRRCv7gkdpamr6aGho6KuBgQFnfHx88V7AZQlcEt01jgD+sbGx3V+OjPR07d8fDQaDl1OpVLK7u9swTXP1Qa7NfwCi46BIaoRmhAAAAABJRU5ErkJggg==), auto";
		};

		this.adjustSpeed = function(direction) {
			if(direction === 0) { // reset to default
				_movementSpeed = _movementSpeedDefault;
			} else {
				_movementSpeed *= (direction > 0) ? 1.10 : 0.90;
				if(_movementSpeed < 0.01) {
					_movementSpeed = 0.01;
				}
			}
		};

		function getEventModifierState(event) {
			if(!!_touchType)
				return false;

			var ctrlKey = event.ctrlKey || (_isMac && event.metaKey);
			var metaKey = event.metaKey && !_isMac;

			//console.log("Mod keys: ctrl = "+ctrlKey+" meta = "+metaKey+" alt^ctrl = "+ (event.altKey ^ ctrlKey));

			return ctrlKey || metaKey || event.shiftKey || event.altKey;
		}

		/////////////////////////////////////////////////////////////////////////
		// Tool event handler callbacks - can use "this".

		this.handleGesture = function(event) {
			// Convert Hammer touch-event X,Y into mouse-event X,Y.
			if(event.pointers && event.pointers.length > 0) {
				event.pageX = event.pointers[0].pageX;
				event.pageY = event.pointers[0].pageY;
			}

			switch(event.type) {
				case "dragstart":
					_touchType = "drag";
					// Single touch, fake the mouse for now...
					return this.handleButtonDown(event, 0);

				case "dragmove":
					return(_touchType === "drag") ? this.handleMouseMove(event) : false;

				case "dragend":
					if(_touchType === "drag") {
						this.handleButtonUp(event, 0);
						_touchType = null;
						return true;
					}
					return false;
			}

			return false;
		};

		this.handleSingleClick = function(event, button) {
			return false;
		};

		this.handleButtonDown = function(event, button) {
			hideHUD();

			_mouseButtons += 1 << button;

			var modifierState = getEventModifierState(event);
			if(button === 0 && !modifierState) {

				_mouseXstart = event.pageX - window.innerWidth / 2;
				_mouseYstart = event.pageY - window.innerHeight / 2;

				_lastX = event.pageX;
				_lastY = event.pageY;

				_deltaYaw = _deltaPitch = 0;
				_mouseDX = _mouseDY = 0;
				_isDragging = true;
				return true;
			}

			return true; // Eat all these so default tools don't screw with view
		};

		this.handleMouseMove = function(event) {
			var dx = (_lastX < -1e10) ? 0 : event.pageX - _lastX;
			var dy = (_lastY < -1e10) ? 0 : event.pageY - _lastY;
			_lastX = event.pageX;
			_lastY = event.pageY;

			if((_isDragging === _mouseDraggingLookMode) && !_ignoreMouseAndKeyNav) {
				// Joystick Camera Orientation
				/** DISABLED
                 var xNew = event.pageX - window.innerWidth / 2;
                 var yNew = event.pageY - window.innerHeight / 2;
                 if (_mouseDraggingLookMode) {
                // If in drag mode then movement is relative to start point
                _mouseDX = xNew - _mouseXstart;
                _mouseDY = yNew - _mouseYstart;
            }
                 else {
                _mouseDX = xNew;
                _mouseDY = yNew;
            }
                 // A circular area in the middle of the screen or around the start point
                 // defines a neutral area in which no movement occurs.
                 var mouseMoveDist = Math.sqrt( _mouseDX * _mouseDX + _mouseDY * _mouseDY );
                 if ( mouseMoveDist < _neutralZoneDist ) {
                _mouseDX = _mouseDY = 0;
            }
                 DISABLED **/

				// Discrete Camera Orientation
				_deltaYaw += dx * _lookSpeed;
				_deltaPitch += dy * _lookSpeed;
			}

			return true; // Eat all these so default tools don't screw with view
		};

		this.handleButtonUp = function(event, button) {
			_mouseButtons -= 1 << button;

			// If are dragging for a specific button then end dragging no matter
			// what the state of the modifiers.  Otherwise you won't end dragging.
			if(button === 0 && _isDragging) {
				_deltaYaw = _deltaPitch = 0;
				_mouseDX = _mouseDY = 0;
				_isDragging = false;
				return true;
			}

			return true; // Eat all these so default tools don't screw with view
		};

		this.handleKeyDown = function(event, keyCode) {
			if(_ignoreMouseAndKeyNav) {
				return false;
			}

			hideHUD();

			var isModKey = false;
			var handled = false;

			switch(keyCode) {
				case _keys.ESCAPE:
					break;

				case _keys.TAB:
					handled = false;
					break;

					// Eat the modifiers so defualt tools don't activate and mess with cam
				case _keys.SHIFT:
					_modifierState.SHIFT = 1;
					isModKey = handled = true;
					break;
				case _keys.CONTROL:
					_modifierState.CONTROL = 1;
					isModKey = handled = true;
					break;
				case _keys.ALT:
					_modifierState.ALT = 1;
					isModKey = handled = true;
					break;
				case _keys.SPACE:
					_modifierState.SPACE = 1;
					isModKey = handled = true;
					break;

				case _keys.EQUALS:
					this.adjustSpeed(1);
					handled = true;
					break;
				case _keys.DASH:
					this.adjustSpeed(-1);
					handled = true;
					break;
				case _keys.ZERO:
					this.adjustSpeed(0);
					handled = true;
					break; // Reset dolly speed to default

				case _keys.UP:
				case _keys.w:
					_moveForward = true;
					handled = true;
					break;

				case _keys.LEFT:
				case _keys.a:
					_moveLeft = true;
					handled = true;
					break;

				case _keys.DOWN:
				case _keys.s:
					_moveBackward = true;
					handled = true;
					break;

				case _keys.RIGHT:
				case _keys.d:
					_moveRight = true;
					handled = true;
					break;

				case _keys.q:
					_moveUp = true;
					handled = true;
					break;

				case _keys.e:
					_moveDown = true;
					handled = true;
					break;

				case _keys.g:
					handled = true;
					break;

				case _keys.F1:
					handled = true;
					break;
			}

			return handled;
		};

		this.handleKeyUp = function(event, keyCode) {
			if(_ignoreMouseAndKeyNav) {
				return false;
			}

			var isModKey = false;
			var handled = false;

			switch(keyCode) {
				case _keys.TAB:
					handled = false;
					break;

					// Eat the modifiers so defualt tools don't activate and mess with cam
				case _keys.SHIFT:
					_modifierState.SHIFT = 0;
					isModKey = handled = true;
					break;
				case _keys.CONTROL:
					_modifierState.CONTROL = 0;
					isModKey = handled = true;
					break;
				case _keys.ALT:
					_modifierState.ALT = 0;
					isModKey = handled = true;
					break;
				case _keys.SPACE:
					_modifierState.SPACE = 0;
					isModKey = handled = true;
					break;

				case _keys.UP:
				case _keys.w:
					_moveForward = false;
					handled = true;
					break;

				case _keys.LEFT:
				case _keys.a:
					_moveLeft = false;
					handled = true;
					break;

				case _keys.DOWN:
				case _keys.s:
					_moveBackward = false;
					handled = true;
					break;

				case _keys.RIGHT:
				case _keys.d:
					_moveRight = false;
					handled = true;
					break;

				case _keys.q:
					_moveUp = false;
					handled = true;
					break;

				case _keys.e:
					_moveDown = false;
					handled = true;
					break;

				case _keys.g:
					_mouseDX = _mouseDY = 0;
					_mouseDraggingLookMode = !_mouseDraggingLookMode;
					showDraggingLookModeHUD(_mouseDraggingLookMode);
					handled = true;
					break;

				case _keys.F1:
					showHelpHUD();
					handled = true;
					break;
			}

			return handled;
		};

		this.handleWheelInput = function(delta) {
			if(_ignoreMouseAndKeyNav) {
				return false;
			}

			if(_navapi.getReverseZoomDirection())
				delta *= -1;

			_wheelDelta += delta;

			return true;
		};

		this.handleSingleClick = function(event, button) {
			return false;
		};

		this.handleDoubleClick = function(event, button) {
			return false;
		};

		this.handleSingleTap = function(event) {
			return this.handleSingleClick(event, 0);
		};

		this.handleDoubleTap = function(event) {
			return false;
		};

		this.handleBlur = function(event) {
			// Reset things when we lose focus...
			_moveForward = _moveBackward = false;
			_moveLeft = _moveRight = false;
			_moveUp = _moveDown = false;

			return false;
		};

		this.update = function() {
			if(!_isActive || !_navapi.isActionEnabled('walk'))
				return false;

			var delta = _clock.getDelta(); //returns delta in unit seconds

			if(_hudMessageStartShowTime > -1) {
				var curTime = new Date().getTime();
				if(curTime - _hudMessageStartShowTime > _hudMessageShowTime) { // seconds
					hideHUD();
				}
			}

			// From the Collaboration extension:
			//the "go home" call may change the camera back to ortho... and we can't do ortho while walking...
			//HACK: Really, the home view should be set once when launch the extension, then set it back.
			if(!_camera.isPerspective) {
				console.log("Lost perspective mode: resetting view.");
				_navapi.toPerspective();
			}

			var localCam = _camera.clone(); // Copy of camera to modify

			// Handle movement changes

			var actualMoveSpeed = delta * _movementSpeed * _modelScaleFactor * (_modifierState.SHIFT === 1 ? 4 : 1);
			var actualVerticalMoveSpeed = delta * _verticalMovementSpeed * _modelScaleFactor * (_modifierState.SHIFT === 1 ? 4 : 1);

			if(_wheelDelta != 0) {
				var actualWheelMoveSpeed = _wheelDelta * _wheelMovementSpeed * _modelScaleFactor * (_modifierState.SHIFT === 1 ? 4 : 1);
				localCam.translateZ(-actualWheelMoveSpeed);
				_wheelDelta = 0;
			}

			if(_moveForward) {
				localCam.translateZ(-actualMoveSpeed);
			}

			if(_moveBackward) {
				localCam.translateZ(actualMoveSpeed);
			}

			if(_moveLeft) {
				localCam.translateX(-actualMoveSpeed);
			}

			if(_moveRight) {
				localCam.translateX(actualMoveSpeed);
			}

			if(_moveUp) {
				localCam.translateY(actualVerticalMoveSpeed);
			}

			if(_moveDown) {
				localCam.translateY(-actualVerticalMoveSpeed);
			}

			var newPosition = localCam.position;
			var posChanged = (newPosition.distanceToSquared(_camera.position) !== 0);

			// Handle look changes

			var actualLookSpeed = delta * _lookSpeed;

			var newTarget = localCam.target;

			var directionFwd = _camera.target.clone().sub(_camera.position);
			//directionFwd = directionFwd.sub((directionFwd.multiply(_camera.worldup)).multiply(_camera.worldup));

			var directionRight = directionFwd.clone().cross(_camera.up).normalize();

			/** Joystick Camera Orientation
			 ** This code enabled continuous movement of camera as apposed to the
			 ** discrete movement mode below.  Moving the cursor outside of the
			 ** center of the view orients the camera in that direction and continues
			 ** moving while cursor is outside neutral center.  It works like a
			 ** virtual joystick.
			 **
			 ** Uncomment/Comment these sections to switch the style of camera orientation.
			 **/

			/** DISABLED
             var dyawAngle = 0, dpitchAngle = 0;
             if (Math.abs(_mouseDX) > _neutralZoneDist) {
            if (_mouseDX > 0) {
                _mouseDX = Math.min(_mouseDX, _mouseXMaxLimit); // Throttle look speed.
                dyawAngle = (_mouseDX - _neutralZoneDist) * actualLookSpeed;
            }
            else {
                _mouseDX = Math.max(_mouseDX, -_mouseXMaxLimit); // Throttle look speed.
                dyawAngle = (_mouseDX + _neutralZoneDist) * actualLookSpeed;
            }
        }
             if (Math.abs(_mouseDY) > _neutralZoneDist) {
            if (_mouseDY > 0) {
                _mouseDY = Math.min(_mouseDY, _mouseYMaxLimit); // Throttle look speed.
                dpitchAngle = (_mouseDY - _neutralZoneDist) * actualLookSpeed;
            }
            else {
                _mouseDY = Math.max(_mouseDY, -_mouseYMaxLimit); // Throttle look speed.
                dpitchAngle = (_mouseDY + _neutralZoneDist) * actualLookSpeed;
            }
        }
             if (dpitchAngle) {
            var pitchQ = new THREE.Quaternion();
            pitchQ.setFromAxisAngle(directionRight, -dpitchAngle);
            // Need to limit pitch to +-85 degrees so we don't create
            // camera jumping at vertical limits.
            var dirFwdTmp = directionFwd.clone();
            dirFwdTmp.applyQuaternion(pitchQ);
            var vertical = _camera.worldup.clone();
            var vertAngle = dirFwdTmp.angleTo(vertical);
            var vertLimit = THREE.Math.degToRad(5);
            // If new angle is within limits then update values; otherwise ignore
            if ( vertAngle >= vertLimit && vertAngle <= (Math.PI - vertLimit) ) {
                directionFwd.applyQuaternion(pitchQ);
                localCam.up.applyQuaternion(pitchQ);
            }
        }
             if (dyawAngle) {
            var yawQ = new THREE.Quaternion();
            yawQ.setFromAxisAngle(_camera.worldup, -dyawAngle);
            directionFwd.applyQuaternion(yawQ);
            localCam.up.applyQuaternion(yawQ);
        }
             DISABLED **/

			/** Discrete Camera Orientation
			 ** Movement based on the delta changes in position or cursor.  See the
			 ** the "Dynamic Move" code for an alternative.  In this mode the camera
			 ** is oriented based on the delta movement of the cursor.  Movement
			 ** stops as camera is oriented to new change of cursor.
			 ** TODO: Add logic to smooth motion so camera position ramps towards
			 ** the new location rather than discrete jumps.
			 **/

			if(_deltaPitch != 0) {
				var pitchQ = new THREE.Quaternion();
				pitchQ.setFromAxisAngle(directionRight, -_deltaPitch);
				// Need to limit pitch to +-85 degrees so we don't create
				// camera jumping at vertical limits.
				var dirFwdTmp = directionFwd.clone();
				dirFwdTmp.applyQuaternion(pitchQ);

				var vertical = _camera.worldup.clone();
				var vertAngle = dirFwdTmp.angleTo(vertical);
				var vertLimit = THREE.Math.degToRad(5);

				// If new angle is within limits then update values; otherwise ignore
				if(vertAngle >= vertLimit && vertAngle <= (Math.PI - vertLimit)) {
					directionFwd.applyQuaternion(pitchQ);
					localCam.up.applyQuaternion(pitchQ);
				}

				_deltaPitch = 0.0;
			}

			if(_deltaYaw != 0) {
				var yawQ = new THREE.Quaternion();
				yawQ.setFromAxisAngle(_camera.worldup, -_deltaYaw);
				directionFwd.applyQuaternion(yawQ);
				localCam.up.applyQuaternion(yawQ);
				_deltaYaw = 0.0;
			}

			// Now calc new target location and if it changed.
			newTarget = newPosition.clone().add(directionFwd);
			//now fix newPosition for lockInPlane
			var targetChanged = (newTarget.distanceToSquared(_camera.target) !== 0);
			// If position or target changed then update camera.
			if(posChanged || targetChanged) {

				_navapi.setView(newPosition, newTarget);
				//_camera.position = newPosition.clone();
				//_camera.target = newTarget.clone();
				//_camera.dirty = true;s
				// Force the camera to stay orientated up with world up.
				_navapi.orientCameraUp();
			}

			//gamepad integration
			if(_gamepadModule) {
				_camera = _gamepadModule.update(_camera);
			}

			return _camera.dirty;

		};

		/////////////////////////////////////////////////////////////////////////
		// HUD helpers

		// Show a HUD for a specific amount of time (showDelay > 0) or until closed.
		var showHUD = function(messageSpecs, showDelay, closeCB, buttonCB, checkboxCB) {
			// TODO: Tool should not be trying to interact with UI
			// Does not comply with headless viewer policy.
			if(!Autodesk.Viewing.Private.HudMessage) {
				return;
			}

			Autodesk.Viewing.Private.HudMessage.displayMessage(_container, messageSpecs, closeCB, buttonCB, checkboxCB);

			if(showDelay > 0) {
				_hudMessageStartShowTime = new Date().getTime();
				_hudMessageShowTime = showDelay;
			} else {
				_hudMessageStartShowTime = -1;
				_hudMessageShowTime = 0;
			}
		};

		var hideHUD = function() {
			// TODO: Tool should not be trying to interact with UI
			// Does not comply with headless viewer policy.
			if(Autodesk.Viewing.Private.HudMessage) {
				Autodesk.Viewing.Private.HudMessage.dismiss(); // in case it's still visible
			}
			_hudMessageStartShowTime = -1;
		};

		var showDraggingLookModeHUD = function(enabled) {
			hideHUD();

			var themessage = (enabled ?
				"Press the primary mouse button and drag to change the view orientation" :
				"Move the cursor to change the view orientation");

			var messageSpecs = {
				"msgTitleKey": "First Person Tool",
				"messageKey": themessage,
				"messageDefaultValue": themessage
			};

			var closeCallback = function() {}; // dummy callback function so that the 'X' is shown
			showHUD(messageSpecs, 0, closeCallback);
		};

		var showHelpHUD = function() {
			hideHUD();

			// TODO: Sadly, the HudMessage api doesn't support html formatted messages
			var messageSpecs = {
				"msgTitleKey": "First Person Tool",
				"messageKey": "Use the WASD and QE keys to move",
				"messageDefaultValue": "Use the WASD and QE keys to move", // simplify key and remove peroid
				"checkboxChecked": _bDontShowAgain_HelpHUD
			};

			var closeCallback = function() {}; // dummy callback function so that the 'X' is shown
			showHUD(messageSpecs, 0, closeCallback, null, function(e) {
				_bDontShowAgain_HelpHUD = e.target.checked;
				viewerapi.setFirstPersonToolPopup(!e.target.checked);
			});
		};

		addCrosshair = function() {
			if(avp.stringToDOM) {
				this.crosshair = avp.stringToDOM('<div id="remote-crosshair"><div class="crosshair-v"></div><div class="crosshair-h"></div></div>f');
				viewerapi.canvasWrap.appendChild(this.crosshair);
			}
		};

		removeCrosshair = function() {
			if(this.crosshair && this.crosshair.parentNode) {
				this.crosshair.parentNode.removeChild(this.crosshair);
			}
		};

	}

	var toolName = "Autodesk.ADN.Viewing.Tool.CustomFirstPersonTool";

	_self.load = function() {

		_self.tool = new AdnTool2(viewer, toolName);

		viewer.toolController.registerTool(_self.tool);

		viewer.toolController.activateTool(toolName);

		console.log('Autodesk.ADN.Viewing.Extension.CustomFirstPersonTool loaded');
		return true;
	};

	_self.unload = function() {

		viewer.toolController.deactivateTool(toolName);

		console.log('Autodesk.ADN.Viewing.Extension.CustomFirstPersonTool unloaded');
		return true;
	};

};

Autodesk.ADN.Viewing.Extension.CustomFirstPersonTool.prototype =
	Object.create(Autodesk.Viewing.Extension.prototype);

Autodesk.ADN.Viewing.Extension.CustomFirstPersonTool.prototype.constructor =
	Autodesk.ADN.Viewing.Extension.CustomFirstPersonTool;

Autodesk.Viewing.theExtensionManager.registerExtension(
	'Autodesk.ADN.Viewing.Extension.CustomFirstPersonTool',
	Autodesk.ADN.Viewing.Extension.CustomFirstPersonTool);

function yaogan(){
    var ji = new Image(); //内摇杆图片
    var jo = new Image(); //外摇杆图片
    var joystick = document.getElementById('joystick'); //画板
    var josize = joystick.height; //外摇杆大小
    var jisize = josize * 0.4; //内摇杆大小
    var centerX = josize / 2; //摇杆中心x坐标
    var centerY = josize / 2; //摇杆中心y坐标
    var touchX = joystick.offsetLeft,
        touchY = joystick.offsetTop;
    window.addEventListener('load', load, false);
    var jc = joystick.getContext('2d'); //画布

    //摇杆头应当移动到的位置
    var jx = 0,
        jy = 0;

    //图片加载完成时执行这俩函数
    ji.onload = function() {
        jc.drawImage(ji, centerX - jisize / 2, centerY - jisize / 2, jisize, jisize); //首次绘制内摇杆
    };
    jo.onload = function() {
        jc.drawImage(jo, centerX - josize / 2, centerY - josize / 2, josize, josize);
    };

    //绘图函数（绘制图形的时候就是用户观察到摇杆动了，所以取名是move）
    function move() {
        jc.clearRect(centerX - josize / 2, centerY - josize / 2, josize, josize); //清空画板
        jc.drawImage(jo, centerX - josize / 2, centerY - josize / 2, josize, josize); //画底座
        jc.drawImage(ji, centerX - jisize / 2 + jx, centerY - jisize / 2 + jy, jisize, jisize); //画摇杆头
        requestAnimationFrame(move); //下一次绘图
    }
    ji.src = '/img/joy.png'; //加载图片
    jo.src = '/img/background.png'; //加载图片

    //页面加载时执行该函数
    function load() {
        joystick.addEventListener('touchstart', touch, false);
        joystick.addEventListener('touchmove', touch, false);
        joystick.addEventListener('touchend', touch, false);

        //加载的时候先把摇杆绘制出来再说
        move();
        var effectiveFinger = -1; //当前有效手指

        //触摸事件触发函数
        function touch(event) {
            var event = event || window.event;
            var oInp = document.getElementById("inp");
            switch(event.type) {
                case "touchstart":
                    //判断是否击中摇杆头
                    for(var i = 0; i < event.touches.length; i = i + 1) {
                        if(Math.sqrt(Math.pow(event.touches[i].clientX - centerX - touchX, 2) +
                                Math.pow(event.touches[i].clientY - centerY - touchY, 2)) <=
                            josize / 2 - jisize / 2) {
                            effectiveFinger = i;
                            console.log("finger No." + i + " is effectiveFinger now.");
                        }
                        // _viewer.toolController.activateTool("firstperson")
                    }
                    _viewer.loadExtension("Autodesk.ADN.Viewing.Extension.CustomFirstPersonTool");
                    break;
                case "touchend": //手指离开的时候
                    //若有效手指离开,那就把内摇杆放中间
                    if(event.touches[effectiveFinger] == null) {
                        if(event.touches[0] == null) {
                            jx = 0;
                            jy = 0;
                        }
                        effectiveFinger -= 1;
                        _viewer.unloadExtension("Autodesk.ADN.Viewing.Extension.CustomFirstPersonTool");
                        _viewer.changeDirection();
                    }
                    break;
                case "touchmove": //手指移动的时候：
                    //是否触摸点在摇杆上
                    let X = event.touches[effectiveFinger].clientX - centerX - touchX;
                    let Y = -(event.touches[effectiveFinger].clientY - centerY - touchY);
                    let bool1 = Y - X;
                    let bool2 = Y + X;
                    console.log(X,Y);
                    if(bool1>0&&bool2>0){
                        console.log('up');
                        _viewer.changeDirection('_moveForward');
                    } else if(bool1>0&&bool2<0){
                        console.log('left');
                        _viewer.changeDirection('_moveLeft');
                    } else if (bool1<0&&bool2<0){
                        console.log('bottom');
                        _viewer.changeDirection('_moveBackward');
                    } else if (bool1<0&&bool2>0){
                        console.log('right');
                        _viewer.changeDirection('_moveRight');
                    } else if (bool1===0&&bool2===0){
                        console.log('bingo')
                    }
                    if(effectiveFinger != -1)
                        if(Math.sqrt(Math.pow(event.touches[effectiveFinger].clientX - centerX - touchX, 2) +
                                Math.pow(event.touches[effectiveFinger].clientY - centerY - touchY, 2)) <=
                            josize / 2 - jisize / 2) {
                            jx = event.touches[effectiveFinger].clientX - centerX - touchX;
                            jy = event.touches[effectiveFinger].clientY - centerY - touchY;
                        } else
                        //否则计算摇杆最接近的位置
                        {
                            var x = event.touches[effectiveFinger].clientX - touchX,
                                y = event.touches[effectiveFinger].clientY - touchY,
                                r = josize / 2 - jisize / 2;

                            var ans = GetPoint(centerX, centerY, r, centerX, centerY, x, y);
                            //圆与直线有两个交点，计算出离手指最近的交点
                            if(Math.sqrt((ans[0] - x) * (ans[0] - x) + (ans[1] - y) * (ans[1] - y)) < Math.sqrt((ans[2] - x) * (ans[2] - x) + (ans[3] - y) * (ans[3] - y))) {
                                jx = ans[0] - centerX;
                                jy = ans[1] - centerY;
                            } else {
                                jx = ans[2] - centerX;
                                jy = ans[3] - centerY;
                            }
                        }
                    //move();
                    event.preventDefault(); //防止页面滑动，取消掉默认的事件
                    break;
            }
        }
        requestAnimationFrame(move); //开始绘图
    }

    //计算圆于直线的交点（这一块好难啊）
    //圆的坐标为cx，cy 半径为r
    //直线上两点的坐标分别为(stx,sty)、(edx,edy)
    function GetPoint(cx, cy, r, stx, sty, edx, edy) {
        //(x-cx)^2+(y-cy)^2=r^2
        //y=k*x+b
        var k = (edy - sty) / (edx - stx);
        var b = edy - k * edx;
        //(1 + k^2)*x^2 - x*(2*cx -2*k*(b -cy) ) + cx*cx + ( b - cy)*(b - cy) - r*r = 0
        var x1, y1, x2, y2;
        var c = cx * cx + (b - cy) * (b - cy) - r * r;
        var a = (1 + k * k);
        var b1 = (2 * cx - 2 * k * (b - cy));

        var tmp = Math.sqrt(b1 * b1 - 4 * a * c);

        x1 = (b1 + tmp) / (2 * a);
        y1 = k * x1 + b;

        x2 = (b1 - tmp) / (2 * a);
        y2 = k * x2 + b;
        return [x1, y1, x2, y2];
    }
}


function FirstPersonInit(){
    
     
}
