// sprite.play("walk");
// sprite.pause();
// sprite.next();
// sprite.continue();
// sprite.set_fps(3);

// sprite.get_frame();
// sprite.get_animation();
// sprite.get_source();

// sprite.on("start", () => null);
// sprite.on("complete", () => null);
// sprite.on("frame", () => null);

class YvSpriteAnimation {
	/*  play(animation_name) - automatic process of playing, no need to create a manager
        stop() - stop automatic process
        pause(true, false) - prevent frame from going to the next frame
        next(jump) - current_frame + jump
        render() - render the sprite based on current frame

        set_animation(animation_name) - change the animation to animation_name if it exists
        set_animation_option(animation_name, opt) - fps, loop: true, sequence: [4, 3, 2, 1, 0]
        set_default_fps(new_fps) - set the default fps to new_fps
        set_frame(column) - set the current animation frame to column

        get_animation_info() - returns current animation and current frame
        get_info() - returns source, width, height, frame width, frame height */
	constructor(opt) {
		// selector (optional) - where to attach the element
		// source - spritesheet source path
		// columns - number of columns
		// rows - number of rows
		// default_fps - the target fps if animation's fps is not set
		// animations - the animations

		const { selector = null, source, columns, rows, default_fps = 10, default_animation, animations } = opt;

		if (source == null || source == "") throw new Error("'source' is undefined");
		if (columns == null || columns <= 0) throw new Error("'columns' property is invalid");
		if (rows == null || rows <= 0) throw new Error("'rows' property is invalid");
		if (default_fps == null || default_fps <= 0) throw new Error("'default_fps' property is invalid");
		if (default_animation == null || default_animation == "") throw new Error("'default_animation' must be set");
		if (Object.keys(animations).length == 0) throw new Error("'animations' is empty");

		this.current_frame = 0;
		this.current_animation = animations[default_animation];

		this.root = document.createElement("div");
		if (selector == null) document.body.append(this.root);
		else {
			const parent = document.querySelector(selector);
			if (parent) parent.append(this.root);
			else document.body.append(this.root);
		}

		const image = new Image();
		image.src = source;
		image.onload = () => {
			this.image_width = image.width;
			this.image_height = image.height;
			this.frame_width = image.width / columns;
			this.frame_height = image.height / rows;

			this.root.style.background = `url(${source})`;
			this.root.style.width = `${this.frame_width}px`;
			this.root.style.height = `${this.frame_height}px`;
		};
	}

	play(animation_name = null) {
		if (animation_name) {
			this.current_animation = this.opt.animations[animation_name];
		}

		this.player = setInterval(() => {
			this.render();
			this.next();
		}, this.current_animation.fps);
	}

	stop() {
		clearInterval(this.player);
	}

	next(jump = 1) {
		let frame = this.current_frame + jump;

		if (this.current_animation.sequence) {
			if (frame < 0) frame = this.sequence.length - 1;
			if (frame > this.sequence.length) frame = 0;
		} else {
			if (frame < 0) frame = this.current_animation.steps - 1;
			if (frame > this.current_animation.steps) frame = 0;
		}

		this.current_frame = frame;
	}

	render() {
		const frame_pointer = this.current_animation.sequence ? this.current_animation.sequence[current_frame] : this.current_frame;
		this.root.style.backgroundPosition = `-${this.frame_width * frame_pointer}px ${this.frame_height * this.current_animation.row}px`;
	}

	set_frame(row, column) {
		null;
	}
}

const sprite = new YvSpriteAnimation({
	source: "rotatoes_attack.png",
	default_animation: "walk",
	rows: 1,
	max_steps: 7,
	animations: {
		walk: { fps: 10, start: 0, steps: 5, loop: true, row: 0 },
		rev_walk: { fps: 10, start: 0, steps: 5, loop: true, row: 0, sequence: [4, 3, 2, 1, 0] },
	},
});

let frameCount = 0;
let lastTime = performance.now();
let realFps = 0;
const fpsel = document.getElementById("fps");
function updateFps() {
	const now = performance.now();
	frameCount++;
	if (now - lastTime >= 1000) {
		// 1 second passed
		realFps = frameCount;
		frameCount = 0;
		lastTime = now;
		fpsel.innerText = realFps;
	}
}

const sprites = [];
for (let i = 0; i < 3000; i++) {
	sprites.push(
		new YvSpriteAnimation({
			source: "rotatoes_attack.png",
			rows: 1,
			max_steps: 7,
			default_animation: "walk",
			animations: {
				walk: { fps: 10, start: 0, steps: 5, loop: true, row: 0 },
			},
		})
	);
}

const targetFps = 60;
const frameDuration = 1000 / targetFps;
let lastFrameTime = performance.now();

function animate(timestamp) {
	if (timestamp - lastFrameTime >= frameDuration) {
		lastFrameTime = timestamp;

		for (let i = 0; i < sprites.length; i++) {
			const sprite = sprites[i];
			if (isVisible(sprite.root)) {
				sprite.root.style.visibility = "visible";
				sprite.next();
				sprite.render();
			} else {
				sprite.root.style.visibility = "hidden";
				sprite.next();
			}
		}

		updateFps();
	}

	requestAnimationFrame(animate);
}

requestAnimationFrame(animate);

function isVisible(el) {
	const rect = el.getBoundingClientRect();
	return rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
}

document.body.style = "display: grid; grid-template-columns: repeat(15, 1fr)";
