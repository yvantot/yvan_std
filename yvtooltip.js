// prefer_position = ["top", "left", "right", "bottom"]
// This would be better if its inside the shadow DOM and we use css all to reset its style
class YvTooltip {
	constructor(name, disappear_before) {
		this.tooltip_name = name;
		this.disappear_before = disappear_before;
		this.timer = null;
		this.tooltip = document.createElement("div");

		this.tooltip.style.display = "none";
		this.tooltip.style.contain = "paint layout content";
		this.tooltip.style.position = "fixed";

		this.tooltip.style.top = "0px";
		this.tooltip.style.left = "0px";

		this.tooltip.style.border = "1px solid hsl(0, 0%, 10%)";
		this.tooltip.style.backgroundColor = "white";
		this.tooltip.style.color = "hsl(0, 0%, 10%)";
		this.tooltip.style.padding = "0.5rem";
		this.tooltip.style.borderRadius = "0.5rem";
		this.tooltip.style.boxShadow = "0px 5px 5px hsla(0, 0%, 50%, 0.5)";

		document.body.append(this.tooltip);
	}

	start() {
		document.addEventListener("mouseover", (e) => {
			const target = e.target;
			if (target.dataset?.[this.tooltip_name]) {
				this.tooltip.innerText = target.dataset?.[this.tooltip_name];

				const { x: target_x, y: target_y, height: target_height } = target.getBoundingClientRect();
				const { width: tooltip_width, height: tooltip_height } = this.tooltip.getBoundingClientRect();
				const offset_height = target_y + target_height;
				const top = parseInt(offset_height + tooltip_height > innerHeight ? target_y - tooltip_height : offset_height) + "px";
				const left = parseInt(target_x + tooltip_width > innerWidth ? innerWidth - tooltip_width : e.x) + "px";

				this.tooltip.style.transform = `translate(${left}, ${top})`;
				this.tooltip.style.display = "block";

				this.clear_timer();
			} else if (target == this.tooltip) {
				this.clear_timer();
			} else {
				this.start_timer(() => this.hide_tooltip(), this.disappear_before);
			}
		});
	}

	hide_tooltip() {
		this.tooltip.style.display = "none";
	}

	start_timer(callback, disappear_before) {
		this.timer = setTimeout(() => callback(), disappear_before);
	}

	clear_timer() {
		if (this.timer) clearTimeout(this.timer);
	}
}

const tooltip = new YvTooltip("tooltip", 1000);
tooltip.start();
