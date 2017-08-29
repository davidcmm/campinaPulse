var spotCount = 0;
var clusterCount = 0;

var spots = new Array();
var clusters = new Array();

var taskId = 0;
var currentTaskRun;

var layer = new Kinetic.Layer();
var sun;
var stage;
var scale = 1;
var imageSize = 600;/* TO DO: Images are smaller! -> 248.833 (hor) x 189.117 (ver)*/
var scaledImageSize = 600;
//var inverted = false;
var currentImage = "";
var normalImage;//, invImage;
var best_worst_stage = 0;
var clusterArea = null;
var DEFAULT_CROSS_WIDTH = 6;

var removeCursor = "url('images/removeCursor.png') 10 8, auto";

/* MISC Functions */
function ChangeImage(img, url) {
	img.src = url;
}

function openShareWindow(url) {
	window.open(url, "_blank", "toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, copyhistory=yes, width=500, height=300");
}

$('body').on('mousedown', function(evt) {
	if (evt.target.tagName == "BODY") {
		document.body.style.cursor = 'default';	
		$("#btnAddSpot").removeAttr("disabled");
		//$("#btnAddCluster").removeAttr("disabled");
		$("#removeSpotOrCluster").removeAttr("disabled");	
	}
});

$('body').on('mouseup', function(evt) {
	if (evt.target.tagName != "CANVAS" && clusterArea != null) {
		clusterArea.remove();
		clusterArea = null;
		layer.draw();
	}
});

/*** Main Functions ***/

function handleMouseOverShape() {
	if ($("#removeSpotOrCluster").is(":disabled")) {
		document.body.style.cursor = removeCursor;
	} else {
		document.body.style.cursor = 'move';	
	}
}

function handleMouseOutShape() {
	if ($("#btnAddSpot").is(":disabled") ) {//||$("#btnAddCluster").is(":disabled")
		document.body.style.cursor = 'crosshair';
	} else {
		document.body.style.cursor = 'default';	
	}
}

function handleMouseDownShape() {
	if ($("#removeSpotOrCluster").is(":disabled")) {
		this.setDraggable(false);
		removeSelectedMark(findMark(this));	
	}
}

function CrossShape(posX, posY, color, width) {
	this.width = width;

	this.shape = new Kinetic.Shape({
		x: posX,
		y: posY,
		drawFunc: function(context) {
			var halfWidth = width/2;
			context.beginPath();
			context.moveTo((-1)*halfWidth, 0);
			context.lineTo(halfWidth, 0);
			context.moveTo(0, (-1)*halfWidth);
			context.lineTo(0, halfWidth);
			context.closePath();
			context.fillStrokeShape(this);
		},
		drawHitFunc: function(context) {
			var startPointX = (-1)*(width/2);
			var startPointY = (-1)*(width/2);

			// a rectangle around the cross
			context.beginPath();
			context.moveTo(startPointX, startPointY);
			context.lineTo(startPointX+width, startPointY);
			context.lineTo(startPointX+width, startPointY+width);
			context.lineTo(startPointX, startPointY+width);
			context.closePath();
			context.fillStrokeShape(this);
		},				
		stroke: color,
		strokeWidth: 2,
		draggable: true
	});

	this.shape.on('mouseover', handleMouseOverShape);
	this.shape.on('mouseout', handleMouseOutShape);
	this.shape.on("mousedown", handleMouseDownShape);
}

CrossShape.prototype.getShape = function(){
	return this.shape;
}

CrossShape.prototype.getPosition = function(){
	return this.shape.getPosition();
}

CrossShape.prototype.getWidth = function(){
	return this.width;
}

CrossShape.prototype.getClassName = function(){
	return "Cross";
}

function createSpot(posX, posY) {
	var origX = posX / scale;
	var origY = posY / scale;
	var cross = new CrossShape(origX, origY, "yellow", DEFAULT_CROSS_WIDTH);

	spots[spotCount] = cross;
	spotCount++;
	//$('#lblspotCount').text(spotCount);

	layer.add(cross.getShape());
	layer.draw();
}

function createSpotEntry(posX, posY, shapeWidth) {
	return "~spot:{" + posX + "," + posY + "}";
}

function createClusterEntry(posX, posY, shapeWidth) {
	return "~cluster:{" + posX + "," + posY + "," + shapeWidth + "," + shapeWidth + "}";
}

function setupKinect() {
	stage = new Kinetic.Stage({
		container: 'pictureCanvas',
		width: imageSize,
		height: imageSize,
		x: 0,
		y: 0,
		draggable: false,
	});

	sun = new Kinetic.Image({
		x: 0,
		y: 0,
		id: "sunPicture",
		image: normalImage,
		width: imageSize,
		height: imageSize
	});

	// add the shape to the layer
	layer.add(sun);

	// add the layer to the stage
	stage.add(layer);

	stage.getContainer().addEventListener('mousedown', function(evt) {
		var target = evt.targetNode;

		if ($("#btnAddSpot").is(":enabled") || 
				typeof target != "undefined" && target.className != "Image") return; //&& $("#btnAddCluster").is(":enabled")

		var pos = stage.getMousePosition();
		pos.x -= stage.attrs.x;
		pos.y -= stage.attrs.y;

		if ($("#btnAddSpot").is(":disabled")) {
			createSpot(pos.x, pos.y);
		} /*else {
			createCluster(pos.x, pos.y);
		}*/
		evt.cancelBubble = true;
	});

	//stage.getContainer().addEventListener('mouseup', function(evt) {
	//	if ($("#btnAddCluster").is(":enabled")) return;
//
	//	addCluster();
	//});

	/*stage.getContainer().addEventListener('mousemove', function(evt) {

		if ($("#btnAddCluster").is(":enabled")) return;

		if (clusterArea != null) {
			var pos = stage.getMousePosition();
			pos.x -= stage.attrs.x;
			pos.y -= stage.attrs.y;
			pos.x /= scale;
			pos.y /= scale;
			clusterArea.attrs.width = pos.x - clusterArea.attrs.x;
			clusterArea.attrs.height = clusterArea.attrs.width;
			layer.draw();
			evt.cancelBubble = true;
		}
	});*/

	// Keep the picture inside the div
	stage.on("dragmove", keepInViewPort);
	// Zoom events
	stage.getContainer().addEventListener("mousewheel", zoom, false);
	stage.getContainer().addEventListener("DOMMouseScroll", zoom, false); // firefox

	// Key mapping
	window.addEventListener('keydown', function(e) {
		var x = stage.attrs.x;
		var y = stage.attrs.y;
		if (e.keyCode == 37) //Left Arrow Key
			x += 10;
		if (e.keyCode == 38) //Up Arrow Key
			y += 10;
		if (e.keyCode == 39) //Right Arrow Key
			x -= 10;
		if (e.keyCode == 40) //Top Arrow Key
			y -= 10;

		// Refresh
		if (e.keyCode == 40 || e.keyCode == 39 || e.keyCode == 38 || e.keyCode == 37) {
			stage.setPosition(x, y);
			keepInViewPort();
			stage.draw();
		}
	});
}

function zoom(evt) {
        // cross-browser wheel delta
        var e = window.event || evt; // old IE support
        var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));

        doZoom(delta * 0.030);
};

function doZoom(level) {
        stage.setScale(stage.getScale().x + level);
        // Avoid zoom-out
        if (stage.getScale().x < 1)
                stage.setScale(1);

        if (level > 0) {
                stage.setPosition(stage.attrs.x - 2, stage.attrs.y - 2);
        }
        else {
                stage.setPosition(stage.attrs.x + 2, stage.attrs.y + 2);
        }

        keepInViewPort();
        stage.draw();

        scale = stage.getScale().x;
        scaledImageSize = imageSize * scale;
}

function keepInViewPort(e) {
	if (stage.attrs.x < (imageSize - scaledImageSize)) {
		stage.attrs.x = imageSize - scaledImageSize;
	}
	if (stage.attrs.y < (imageSize - scaledImageSize)) {
		stage.attrs.y = imageSize - scaledImageSize;
	}
	if (stage.attrs.x > 0)
		stage.attrs.x = 0;
	if (stage.attrs.y > 0)
		stage.attrs.y = 0;
};

function reset() {
	scale = 1;
	inverted = false;
	imageSize = 600;
	scaledImageSize = 600;
	stage.setPosition(0, 0);
	stage.setScale(scale);
	stage.draw();
}

//Called when an image must be loaded for evaluation
function loadImages() {
	// Loading..
	$("#imgs-wrapper").empty();
	if(bestWorstStage === 1){
		$("#imgs-wrapper").append('<div class="col-xs-10 col-sm-9"> <p class="title-cg"> Marque até 3 pontos na imagem que justifiquem o porquê ele ter sido o <strong class="up">melhor local</strong>!</p> </div> <label id="lblImage">City Image</label> <img style="width: 600px; height: 600px; border: solid;" src="https://contribua.org/sun4allfiles/images/loading.gif" id="loadingPicture" /> <div id="pictureCanvas" style="width: 608px; height: 608px; position: absolute; left: 0; display: none; border: solid; background-color: white"></div> <div style="position: relative; top: 0px; left: 620px; width: 300px; height: 380px; border: solid; padding: 10px;"> <fieldset> <button id="btnAddSpot" class="btn btn-warning" type="button" style="width: 100%;" onclick="javascript:enableAddSpot();"></button> <button id="removeSpotOrCluster" class="btn" type="button" style="width: 100%; margin-top: 10px" onclick="javascript:enableRemoveMark();"></button> <button id="btnFinish" class="btn btn-success" type="button" style="width: 100%; height: 60px; margin-top: 5px" onclick="javascript:done();"> <i class="icon-ok icon-white"></i> </button> </fieldset> </div>');
	}else{
		$("#imgs-wrapper").append('<div class="col-xs-10 col-sm-9"> <p class="title-cg"> Marque até 3 pontos na imagem que justifiquem o porquê ele ter sido o <strong class="up">pior local</strong>!</p> </div> <label id="lblImage">City Image</label> <img style="width: 600px; height: 600px; border: solid;" src="https://contribua.org/sun4allfiles/images/loading.gif" id="loadingPicture" /> <div id="pictureCanvas" style="width: 608px; height: 608px; position: absolute; left: 0; display: none; border: solid; background-color: white"></div> <div style="position: relative; top: 0px; left: 620px; width: 300px; height: 380px; border: solid; padding: 10px;"> <fieldset> <button id="btnAddSpot" class="btn btn-warning" type="button" style="width: 100%;" onclick="javascript:enableAddSpot();"></button> <button id="removeSpotOrCluster" class="btn" type="button" style="width: 100%; margin-top: 10px" onclick="javascript:enableRemoveMark();"></button> <button id="btnFinish" class="btn btn-success" type="button" style="width: 100%; height: 60px; margin-top: 5px" onclick="javascript:done();"> <i class="icon-ok icon-white"></i> </button> </fieldset> </div>');
	}

	//Adding buttons texts!
	$("#btnAddSpot").text("Adicionar ponto");
	$("#removeSpotOrCluster").text("Remover ponto");
	if(bestWorstStage == 1){
		$("#btnFinish").text("Próxima imagem");
	}else{
		$("#btnFinish").text("Tarefa concluída!");
	}


	$('#pictureCanvas').hide();
	$('#loadingPicture').show();
	//$("#btnInvert").attr('disabled', 'disabled');

	// Set the image description
	//var parts = currentImage.split("_");
	//var date = new Date('19' + parts[3], parts[2] - 1, parts[1]);
	//$('#lblImage').text(getDataTakenInfo(date));

	normalImage = new Image();
	normalImage.onload = function () {
		// Show image
		$('#pictureCanvas').show();
		$('#loadingPicture').hide();

		sun.setImage(normalImage);
		stage.draw();
	};
	//normalImage.src = "https://contribua.org/sun4allfiles/" + currentImage;
	normalImage.src = currentImage;

	//invImage = new Image();
	//invImage.onload = function() {
	//	$("#btnInvert").removeAttr("disabled");
	//};
	//invImage.src = "https://contribua.org/sun4allfiles/inv/" + currentImage;
}

function findMark(shape) {
	var marks = shape.getClassName() == 'Rect' ? clusters : spots;
	for (var i = 0; i < marks.length; i++) {
		var pos = shape.getPosition();
		var markPos = marks[i].getPosition();
		if (pos.x == markPos.x && pos.y == markPos.y) {
			return marks[i];
		}
	}
	return null;
}

function enableRemoveMark() {
	document.body.style.cursor = 'default';
	$("#removeSpotOrCluster").prop("disabled", 'true');
	$("#btnAddCluster").removeAttr("disabled");
	$("#btnAddSpot").removeAttr("disabled");
}

function removeSelectedMark(mark) {
	if (mark == null) return; 

	var entryType = mark.getClassName() == 'Cross' ? 'spot' : 'cluster';

	if (entryType == 'spot') {
		spots.splice(spots.indexOf(mark), 1);
		spotCount--;
		//$('#lblspotCount').text(spotCount);
		mark.getShape().remove();

	} /*else {
		clusters.splice(clusters.indexOf(mark), 1);
		clusterCount--;
		$('#lblclusterCount').text(clusterCount);
		mark.remove();
	}*/

	layer.draw();
}

function enableAddSpot() {
	document.body.style.cursor = "crosshair";

	$("#btnAddSpot").prop("disabled", 'true');
	//$("#btnAddCluster").removeAttr("disabled");
	$("#removeSpotOrCluster").removeAttr("disabled");
}

function enableAddCluster() {
	document.body.style.cursor = "crosshair";

	//$("#btnAddCluster").prop("disabled", 'true');
	$("#btnAddSpot").removeAttr("disabled");
	$("#removeSpotOrCluster").removeAttr("disabled");
}

function startOver() {
	//reset canvas
	for (var i = 0; i < spots.length; i++)
		spots[i].getShape().remove();

	//for (var i = 0; i < clusters.length; i++)
	//	clusters[i].remove();

	spotCount = 0;
	//clusterCount = 0;
	spots = new Array();
	//clusters = new Array();
	//$('#lblclusterCount').text(clusterCount);
	//$('#lblspotCount').text(spotCount);

	reset();
	layer.draw();

	//reset textbox
	$('#txtObservation').val('');
}

//Start a new game round: sun-spot
function start(data) {

	var task = data.task;
	if ($.isEmptyObject(task)) {
            reset();
            $("#mainDivGame").hide();
            $("#finish").fadeIn(500);
            return;
        }

	// Get task info
	taskId = task.id;

	// start!
	currentImage = task.info.image;/* TO DO: Change to save both images, the best one and the worst one!*/
	inverted = true;
	reset();
	loadImages();
}

//Start a new game round for Como é Campina? where the worker is asked to add spots to the images that are related to the reasons why they selected those images!
function start_comoecampina(taskrun) {

	//TO DO: start hiding all images: $("#imgs-wrapper").hide() or (var img = document.getElementById("imgA"), img.style.visibility = "visible") or ($("container").empty(), $("container").append(...)) and then presenting only two selected images!
	if ($.isEmptyObject(taskrun)) {
            reset();
            $("#mainDivGame").hide();
            $("#finish").fadeIn(500);
            return;
        }
	taskId = taskrun.task_id;
	currentTaskRun = taskrun;
	
	// start!
	if (bestWorstStage === 0){
		currentImage = taskrun.info.theMost;
	}else{
		currentImage = taskrun.info.theLess;
	}
	bestWorstStage = bestWorstStage + 1;
	reset();
	loadImages();
}

//Called when the evaluation of a certain image has finished (after adding spots to it!)
function done() {
	if (bestWorstStage == 1){//Presenting next image!
		start_comoecampina(currentTaskRun);
	}else{
	//	var answer = spotCount + "~" + clusterCount + "~" + $('#txtObservation').val();
		var answer = spotCount + "~" + $('#txtObservation').val();
		// add spots
		for (i = 0; i < spotCount; i++) {
			var spot = spots[i];
			var pos = spot.getPosition();
			answer += createSpotEntry(pos.x, pos.y);
		}
		// add clusters
		/*for (i = 0; i < clusterCount; i++) {
			var cluster = clusters[i];
			var pos = cluster.getPosition();
			answer += createClusterEntry(pos.x, pos.y, cluster.getWidth());
		}*/
		currentTaskRun['spots'] = answer;
		taskrunString = JSON.stringify(currentTaskRun);

		//Saving in database!
		$http.post('https://contribua.org/api/taskrun', taskrun).then(function(response) {
			// console.log('Saved!');
			$("#skeleton").fadeOut(0);
			$("#success").fadeIn();
			// After save, calls a new task again
			newTask();
			$("#skeleton").fadeIn(1000);
			setTimeout(function() { $("#success").fadeOut() }, 1000);
		}, function saveTaskErrorCallback(response) {
			$('#error').show();
		});
	}
}
