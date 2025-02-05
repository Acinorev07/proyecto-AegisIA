
export default async function get_cryptos(boton,cryptoList,cryptoSearch) {
    const d = document;
    const $fetchCryptos = d.getElementById(boton);
    const $txtBox = d.getElementById(cryptoSearch);
    const $cryptoList = d.getElementById(cryptoList);
    let searchTerm = null;
    const ls = localStorage;

    d.addEventListener("click", async e => {

        //  console.log(`Estamos dentro del evento clic del dom en el archivo get_cryptos: ${e.target}`);

         $txtBox.addEventListener('input', function() {
            searchTerm = $txtBox.value;
            // console.log('Texto ingresado por el usuario:', searchTerm);
        });

        if ($fetchCryptos.contains(e.target)) {

            // console.log(`Estamos dentro del evento clic del boton crypto-search: ${e.target}`);

          
            if(searchTerm != null){

                // console.log(`Estamos dentro del evento clic del boton crypto-search ytambien dentro del condicional searchTerm: ${e.target}`);
                // console.log(`SearchTerm: ${searchTerm}`);

                try {
                    let response = await fetch('/get_cryptos');
                    let json = await response.json();

                    // console.log(`Respuesta desde /get_cryptos en routes.py:`, json);

                    // Verificar si hay errores en la respuesta
                    if (json.error && json.error.length > 0) {
                        console.error('Error en la respuesta de la API de Kraken:', json.error);
                        return;
                    }

                     let cryptos = json.cryptos;


                     $cryptoList.innerHTML = '';

                     cryptos.forEach(crypto=>{
                        if (crypto.symbol.toLowerCase().includes(searchTerm)) {
                            // console.log("Simbolo", crypto.symbol);

                            const $li = d.createElement('li');
                            $li.textContent = `${crypto.symbol}: $${parseFloat(crypto.price).toFixed(2)}`;
                           
                            $cryptoList.appendChild($li);
                            $li.addEventListener('click', (e) => {

                                // console.log("clic dentro de un objeto de la lista: ",crypto.symbol)

                                ls.setItem('symbol',crypto.symbol);
                                // recargar pagina
                                location.reload();
                                $cryptoList.classList.add('show');

                            });
                            $cryptoList.classList.remove('show');
                         }
                        });

                } catch (error) {
                    console.error('Error:', error);
                }


            }



        }
    });
}
