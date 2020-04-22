$(async function () {
	const $submitForm = $('#submit-form');
	$submitForm.on('submit', async function (evt) {
		evt.preventDefault();
		let guess = $('#answer').val();
		try {
			const res = await axios.post(`/answer`, {
				"answer": guess,
			});
			console.log(res);
		} catch (error) {
			console.log('error :', error);
		}
	});
});