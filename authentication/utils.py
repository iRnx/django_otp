import qrcode
from io import BytesIO
import base64


def criar_qr_code(config_url):
    qr_code_img = qrcode.make(config_url)
    buffer = BytesIO()
    qr_code_img.save(buffer)
    buffer.seek(0)
    encoded_img = base64.b64encode(buffer.read()).decode()
    qr_code_data = f'data:image/png;base64,{encoded_img}'

    return qr_code_data
