function createCupcakehtml(cupcake) {
    return `
    <div data-id=${cupcake.id}>
        <li>
            Flavor: ${cupcake.flavor}
            Size: ${cupcake.size}
            Rating: ${cupcake.rating}
        <li>
        <img class="img-url img-fluid w-25 p-3"
            src="${cupcake.image}"
            alt="Cupcake Image">
    </div>
    `;
}

async function getCupCakes() {
    let response = await axios.get('http://127.0.0.1:5000/api/cupcakes');


    for (let cupcake of response.data.cupcakes) {
        let cupcakeSingle = $(createCupcakehtml(cupcake));
        
        $("#cupcakes").append(cupcakeSingle);
    }
}

$("#cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();

    let flavor = $("#flavor").val();
    let rating = $("#rating").val();
    let size = $("#size").val();
    let image = $("#image").val();

    const cupcakeResponse = await axios.post('http://127.0.0.1:5000/api/cupcakes',
    {flavor,rating,size,image});

    let newCupcake = $(createCupcakehtml(cupcakeResponse.data.cupcake));
    $("#cupcakes").append(newCupcake);
    $("#cupcake-form").trigger("reset");
});

$(getCupCakes);