class YvSPrite {
	constructor(opt) {
		const { selector = null, source, columns, rows, default_fps = 10, default_animation, animations } = opt;
		this.opt = opt;

		if (source == null || source == "") throw new Error("'source' is undefined");
		if (columns == null || columns <= 0) throw new Error("'columns' property is invalid");
		if (rows == null || rows <= 0) throw new Error("'rows' property is invalid");
		if (default_fps == null || default_fps <= 0) throw new Error("'default_fps' property is invalid");
		if (default_animation == null || default_animation == "") throw new Error("'default_animation' must be set");
		if (Object.keys(animations).length == 0) throw new Error("'animations' is empty");

		this.current_frame = 0;
		this.is_pause = false;
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

			if (this.on_ready) this.on_ready();
		};
	}

	play(animation_name = null, render_visible = false) {
		this.current_frame = 0;

		if (animation_name) {
			this.current_animation = this.opt.animations[animation_name];
		}

		if (this.player) clearInterval(this.player);
		this.player = setInterval(() => {
			if (this.is_pause) return;
			if (render_visible) this.render_visible();
			else this.render();
			this.next();
		}, 1000 / (this.current_animation.fps ?? this.opt.default_fps));
		return this;
	}

	get_root() {
		return this.root;
	}

	get_animation_info() {
		return { current_animation: this.current_animation, current_frame: this.current_frame };
	}

	get_opt() {
		return this.opt;
	}

	get_info() {
		return { frame_width: this.frame_width, frame_height: this.frame_height, image_width: this.image_width, image_height: this.image_height };
	}

	pause(bool) {
		this.is_pause = bool;
		return this;
	}

	stop() {
		clearInterval(this.player);
		return this;
	}

	set_sequence(sequence) {
		this.current_animation.sequence = sequence;
		return this;
	}

	set_loop(bool) {
		this.current_animation.loop = bool;
		return this;
	}

	set_default_fps(fps) {
		this.default_fps = fps;
		return this;
	}

	set_fps(fps) {
		this.current_animation.fps = fps;
		if (this.player) {
			this.stop();
			this.play();
		}
		return this;
	}

	next(jump = 1) {
		let frame = this.current_frame + jump;

		if (this.current_animation.sequence) {
			if (frame < 0) frame = this.current_animation.sequence.length - 1;
			if (frame > this.current_animation.sequence.length - 1) {
				if (this.current_animation.loop) {
					frame = 0;
					if (this.on_complete) this.on_complete();
				} else return this;
			}
		} else {
			if (frame < 0) frame = this.current_animation.steps - 1;
			if (frame > this.current_animation.steps - 1) {
				if (this.current_animation.loop) {
					frame = 0;
					if (this.on_complete) this.on_complete();
				} else return this;
			}
		}

		this.current_frame = frame;
		return this;
	}

	render() {
		const frame_pointer = this.current_animation.sequence ? this.current_animation.sequence[this.current_frame] : this.current_frame;
		this.root.style.backgroundPosition = `-${this.frame_width * frame_pointer}px ${this.frame_height * this.current_animation.row}px`;
		return this;
	}

	render_visible() {
		if (this.is_visible()) this.render();
		return this;
	}

	is_visible() {
		const rect = this.root.getBoundingClientRect();
		return rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
	}

	set_frame(column) {
		this.current_frame = column;
		return this;
	}
}

const sprite = new YvSPrite({
	source: "rotatoes_attack.png",
	default_animation: "idle",
	default_fps: 10,
	columns: 7,
	rows: 1,
	animations: {
		idle: { fps: 8, steps: 7, row: 0, loop: true },
		rev_idle: { row: 0, sequence: [6, 6, 6, 6, 6, 5, 4, 3, 2, 1, 0] },
	},
});

sprite.play("idle");
