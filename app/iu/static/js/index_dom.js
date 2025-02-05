
import hamburguerMenu from "./header.js";
import TvWidget from "./TvWidget.js";
import get_cryptos from "./get_cryptos.js";
import InversionTron from "./InversionTron.js";
import ReferralLink from "./ReferralLink.js";



const d = document;


d.addEventListener("DOMContentLoaded",(e)=>{
    const tvWidget = new TvWidget();
    const inversion = new InversionTron();
    const link_ref = new ReferralLink();
    
    //Menu desplegable que permite navegar entre las rutas de la pagina
    hamburguerMenu('mobile-menu-button-div','mobile-menu');

    //Clase que permite cargar el widget de trading view en el cuerpo del documento
    tvWidget.loadTradingSymbol().then(() => {
        // console.log(`El símbolo actual es: ${tvWidget.getCurrentTradingSymbol()}`); 
        
        // console.log(`El símbolo actual guardado en localStorage es: ${localStorage.getItem("symbol")}`);
    });
    //Funcion que permite obtener una lista detallada de los pares de divisas disponibles en la API de kraken
    get_cryptos('fetchCryptos','crypto-list','crypto-search')
   
    //Inversion en la cuenta de tron
    inversion.showInvestmentWarning('investment-btn');

    //Generar link de referidos
    link_ref.detectarClick('generate-referral-btn')
 
   

});
