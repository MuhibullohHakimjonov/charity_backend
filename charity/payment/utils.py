# import hashlib
# from django.conf import settings
#
#
# def generate_click_signature(click_trans_id, service_id, merchant_trans_id, amount, action, sign_time):
#     sign_string = f"{click_trans_id}{service_id}{settings.CLICK_SECRET_KEY}{merchant_trans_id}{amount}{action}{sign_time}"
#     return hashlib.md5(sign_string.encode()).hexdigest()
