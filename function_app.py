import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="GetIpFunction", auth_level=func.AuthLevel.ANONYMOUS)
def GetIpFunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # X-Forwarded-For ヘッダーがあればそちらを優先
    ip = req.headers.get('X-Forwarded-For', req.headers.get('x-forwarded-for'))
    if ip:
        # 複数IPがカンマ区切りで入る場合があるので最初を取得
        ip = ip.split(',')[0].strip()
        # IP:ポート形式の場合はIPだけにする
        if ':' in ip:
            ip = ip.split(':')[0]
    else:
        # それ以外は req.headers["X-Real-IP"] か req.headers["x-real-ip"] も試す
        ip = req.headers.get('X-Real-IP', req.headers.get('x-real-ip'))
        if not ip:
            # それもなければ req.remote_addr (ただしAzure Functionsでは未サポートの場合あり)
            ip = req.headers.get('REMOTE_ADDR', 'unknown')

    result = {"ip": ip}
    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json",
        status_code=200
    )