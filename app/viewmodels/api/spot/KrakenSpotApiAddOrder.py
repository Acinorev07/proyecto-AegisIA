import json
import uuid
import requests
import logging
from flask import jsonify
import time
import hashlib
import hmac
import base64

logger = logging.getLogger(__name__)

class KrakenSpotApiAddOrder:
    def __init__(self):
        self.__endpoint = "https://api.kraken.com/0/private/AddOrder"
        self.data = None

    def _generate_api_sign(self, url_path, data, api_secret):
        """
        Genera el API-Sign requerido por Kraken.

        Pasos básicos (consulta la documentación de Kraken para más detalles):
          1. Concatenar el nonce y el payload (data) en una cadena.
          2. Hacer un hash SHA256 de esa cadena.
          3. Concatenar el path de la API (por ejemplo, '/0/private/AddOrder') con el hash obtenido.
          4. Usar HMAC SHA512 con la clave secreta (decodificada de base64) para firmar el resultado.
          5. Codificar el resultado en base64.
        """
        postdata = data
        # Paso 1: extraer el nonce
        nonce = postdata.get("nonce")
        postdata_encoded = (str(nonce) + json.dumps(postdata)).encode()
        # Paso 2: hash SHA256
        hash_digest = hashlib.sha256(postdata_encoded).digest()
        # Paso 3: concatenar path y hash
        message = url_path.encode() + hash_digest
        # Paso 4: HMAC SHA512 con el API secret
        secret_decoded = base64.b64decode(api_secret)
        hmac_digest = hmac.new(secret_decoded, message, hashlib.sha512).digest()
        # Paso 5: codificar en base64
        api_sign = base64.b64encode(hmac_digest)
        return api_sign.decode()

    def add_order(self, ordertype, order_type, volume, symbol, price, api_key, api_secret):
        """
        Envía una orden a Kraken.
        
        Parámetros:
          - ordertype: Tipo de orden (por ejemplo, 'limit', 'market', etc.)
          - order_type: Dirección de la orden ('buy' o 'sell')
          - volume: Volumen de la orden (en el activo base)
          - symbol: Par de trading (por ejemplo, 'XBTUSD')
          - price: Precio límite (si aplica)
          - api_key: Tu API key de Kraken.
          - api_secret: Tu API secret de Kraken.
        """

        # Genera un nonce único (por ejemplo, usando el timestamp actual)
        nonce = int(time.time() * 1000)

        # Automatiza la generación de cl_ord_id
        cl_ord_id = str(uuid.uuid4())

        # Construir el diccionario de datos
        postdata = {
            "nonce": nonce,
            "ordertype": ordertype,
            "type": order_type,
            "volume": volume,
            "pair": symbol,
            "price": price,
            "cl_ord_id": cl_ord_id
        }

        # Calcula el API-Sign usando el método helper
        url_path = "/0/private/AddOrder"
        api_sign = self._generate_api_sign(url_path, postdata, api_secret)

        # Prepara el payload y las cabeceras
        payload = json.dumps(postdata)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'API-Key': api_key,
            'API-Sign': api_sign
        }

        try:
            response = requests.post(self.__endpoint, headers=headers, data=payload)
            if response.status_code != 200:
                logger.error(f"Error en la petición: HTTP {response.status_code}")
                return jsonify({"error": "Error en la petición"}), 500
            self.data = response.json()
            if "error" in self.data and self.data["error"]:
                logger.error(f"Error en la API de Kraken: {self.data['error']}")
                return {"error": str(self.data["error"])}, 500
            return self.data

        except Exception as e:
            logger.error(f"Error al enviar la orden: {e}")
            return {"error": str(e)}, 500
