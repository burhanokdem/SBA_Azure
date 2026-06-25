import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="CalculateArea")
def CalculateArea(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger fonksiyonu bir istek işliyor.')

    try:
        # İstek gövdesinden (JSON) verileri almaya çalışıyoruz
        req_body = req.get_json()
        shape = req_body.get('shape')
        value1 = float(req_body.get('value1', 0))
        value2 = float(req_body.get('value2', 0))
        
        result = 0
        message = ""

        # Hesaplama Mantığı (Gelen şekle göre işlem yapıyoruz)
        if shape == "square":
            result = value1 * value1
            message = f"Karenin Alanı: {result}"
        elif shape == "rectangle":
            result = value1 * value2
            message = f"Dikdörtgenin Alanı: {result}"
        elif shape == "circle":
            import math
            result = math.pi * (value1 ** 2)
            message = f"Dairenin Alanı: {round(result, 2)}"
        else:
            return func.HttpResponse(
                json.dumps({"error": "Geçersiz şekil tipi türü!"}),
                status_code=400,
                mimetype="application/json"
            )

        # Sonucu JSON formatında başarılı bir şekilde dönüyoruz
        return func.HttpResponse(
            json.dumps({
                "shape": shape,
                "result": result,
                "message": message
            }),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Lütfen geçerli sayısal değerler girin."}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": f"Bir hata oluştu: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )