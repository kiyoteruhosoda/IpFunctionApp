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
        ip_list = []
        if ip:
            # カンマ区切りで複数IPが入る場合に対応
            for ip_entry in ip.split(','):
                ip_only = ip_entry.strip()
                # IP:ポート形式の場合はIPだけにする
                if ':' in ip_only:
                    ip_only = ip_only.split(':')[0]
                ip_list.append(ip_only)

        result = {"ip": ip_list} if len(ip_list) > 1 else {"ip": ip_list[0] if ip_list else "unknown"}
        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200
        )