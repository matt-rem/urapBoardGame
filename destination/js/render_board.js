let gameContainer = document.getElementById("game");
let app = new PIXI.Application();
let sprites = [];

document.getElementById('game').appendChild(app.view)

var board_texture = PIXI.Texture.from("{{ url_for('static', filename=board) }}");
board_texture.on('update', () => { 
scaleTo(board, app.renderer.width, app.renderer.height);
app.renderer.render(app.stage);
});

let board = new PIXI.Sprite(board_texture)
board.interactive = true;

sprites.push(board);

board.anchor.x = .5;
board.anchor.y = .5;
board.position.x = app.renderer.width/2;
board.position.y = app.renderer.height/2;
app.stage.addChild(board)
resize();
scaleTo(board, app.renderer.width, app.renderer.height);

function scaleTo(target, width, height) {
if (target.width > target.height) {
var ratio = width / target.width;
} else {
var ratio = height / target.height;
}
target.scale.x *= ratio
target.scale.y *= ratio
}

function resize() {
let ratio = gameContainer.clientWidth / gameContainer.clientHeight;
if (gameContainer.clientWidth / gameContainer.clientHeight >= ratio) {
var w = gameContainer.clientHeight * ratio;
var h = gameContainer.clientHeight;
} else {
var w = gameContainer.clientWidth;
var h = gameContainer.clientWidth / ratio;
}
app.renderer.view.style.width = w + "px";
app.renderer.view.style.height = h + "px";
}

window.onresize = resize;