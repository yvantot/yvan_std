// This Gumroad API is for simple frontend-only payment solutions.
// No server required, Gumroad API handles everything.

async function fetch_product_data(product_id, license_key) {
	const response = await fetch("https://api.gumroad.com/v2/licenses/verify", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			product_id,
			license_key,
		}),
	});
	const data = await response.json();
	return data;
}

function verify_product_purchase(data) {
	if (data.success == false) return false;
	const p = data.purchase;
	if (p.refunded || p.chargebacked) return false;
	return true;
}

function verify_subscription_validity(data) {
	if (data.success == false) return false;
	const now = new Date();
	const p = data.purchase;
	if (p.refunded) return false;
	if (p.subscription_cancelled_at && new Date(p.subscription_cancelled_at) <= now) {
		return false;
	}
	if (p.subscription_ended_at && new Date(p.subscription_ended_at) <= now) {
		return false;
	}
	return true;
}

function test() {
	// User will get a random key like this one
	const prod_key = "A3F5797E-72BC461D-BAAB02C0-C2DC5177";
	// And this is the product id
	const prod_id = "mIIKA9_sNEi5lq4XwHh4jg==";

	const sub_key = "7135C168-01404FA4-AB7FEA78-D51F3BC3";
	const sub_id = "bRRhfinv0lmStPYG_T2a6w==";

	fetch_product_data(prod_id, prod_key).then((val) => console.log(verify_product_purchase(val)));
	fetch_product_data(sub_id, sub_key).then((val) => console.log(verify_subscription_validity(val)));
}

test();
