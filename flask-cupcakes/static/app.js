let form = document.querySelector('#form-target');

const init = async () => {
    let req = await fetch('/api/cupcakes')
    let res = await req.json()
    console.log('res :>> ', res);
    let output = '';
    res.data.forEach((item) => {
        output += `
                <li style="margin-left:25px; list-style:none; margin-bottom:25px">
                    <img style="max-width:200px;max-height:200px" src="${item.image}" alt="cake">
                    <p>flavor: ${item.flavor}</p>
                    <p>size: ${item.size}</p>
                    <p>rating: ${item.rating}</p>
                    <hr>
                </li>`
    })
    document.querySelector('#target').innerHTML = output
}

form.addEventListener('submit', async function (e) {
    e.preventDefault()
    let req = await fetch('/api/cupcakes', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            flavor: document.querySelector('#flavor').value,
            size: document.querySelector('#size').value,
            rating: document.querySelector('#rating').value,
            image: document.querySelector('#image').value
        })
    })

    let res = await req.json()
    let li = document.createElement("LI");
    li.style = "margin-left:25px; list-style:none; margin-bottom:25px"
    let html = `
                <img style="max-width:200px;max-height:200px" src="${res.data.image}" alt="cake">
                <p>${res.data.flavor}</p>
                <p>${res.data.size}</p>
                <p>${res.data.rating}</p>`
    li.innerHTML = html
    document.querySelector('#target').appendChild(li);
})

window.addEventListener('load', init);