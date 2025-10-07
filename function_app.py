import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

def extract_ip_list(ip_header: str) -> list:
    ip_list = []
    if ip_header:
        for ip_entry in ip_header.split(','):
            ip_only = ip_entry.strip()
            if ':' in ip_only:
                ip_only = ip_only.split(':')[0]
            ip_list.append(ip_only)
    return ip_list


@app.route(route="GetIpFunction", auth_level=func.AuthLevel.ANONYMOUS)
def GetIpFunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # X-Forwarded-For ヘッダーがあればそちらを優先
    ip_header = req.headers.get('X-Forwarded-For', req.headers.get('x-forwarded-for'))
    ip_list = extract_ip_list(ip_header)
    if not ip_list:
        # それ以外は X-Real-IP も試す
        ip_header = req.headers.get('X-Real-IP', req.headers.get('x-real-ip'))
        ip_list = extract_ip_list(ip_header)

    result = {"ip": ip_list} if len(ip_list) > 1 else {"ip": ip_list[0] if ip_list else "unknown"}
    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json",
        status_code=200
    )