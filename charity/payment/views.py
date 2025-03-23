from click_up import ClickUp
from payme.views import PaymeWebHookAPIView
from payme import Payme
from rest_framework import views
from rest_framework import response
from click_up.views import ClickWebhook
from .models import Order
from .serializers import OrderCreateSerializer

from payme.models import PaymeTransactions
from click_up.models import ClickTransaction

# from ..charity.settings import PAYME_ID, CLICK_SERVICE_ID, CLICK_MERCHANT_ID
#
# payme = Payme(payme_id=PAYME_ID)


class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def handle_created_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction created for this params: {params} and cr_result: {result}")

    def handle_successfully_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        transaction = PaymeTransactions.get_by_transaction_id(
            transaction_id=params["id"]
        )

        order = Order.objects.get(id=transaction.account.id)
        order.is_paid = True
        order.save()

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        """
        Handle the cancelled payment. You can override this method
        """
        transaction = PaymeTransactions.get_by_transaction_id(
            transaction_id=params["id"]
        )

        if transaction.state == PaymeTransactions.CANCELED:
            order = Order.objects.get(id=transaction.account.id)
            order.is_paid = False
            order.save()


class ClickWebhookAPIView(ClickWebhook):
    def successfully_payment(self, params):
        """
        successfully payment method process you can ovveride it
        """
        transaction = PaymeTransactions.get_by_transaction_id(
            transaction_id=params["id"]
        )

        if transaction.state == PaymeTransactions.CANCELED:
            order = Order.objects.get(id=transaction.account.id)
            order.is_paid = True
            order.save()

    def cancelled_payment(self, params):
        """
        cancelled payment method process you can ovveride it
        """
        transaction = PaymeTransactions.get_by_transaction_id(
            transaction_id=params["id"]
        )

        if transaction.state == PaymeTransactions.CANCELED:
            order = Order.objects.get(id=transaction.account.id)
            order.is_paid = False
            order.save()


# click_up = ClickUp(
#     service_id=CLICK_SERVICE_ID,
#     merchant_id=CLICK_MERCHANT_ID
# )
#
#
# class OrderCreate(views.APIView):
#     serializer_class = OrderCreateSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         result = {
#             "order": serializer.data
#         }
#         if serializer.data['payment_method'] == 'payme':
#             payment_link = payme.initializer.generate_pay_link(
#                 id=serializer.data['id'],
#                 amount=serializer.data['total_cost'],
#                 return_url='https://uzum.uz'
#             )
#             result['payment_link'] = payment_link
#         elif serializer.data['payment_method'] == 'click':
#             payment_link = payme.initializer.generate_pay_link(
#                 id=serializer.data['id'],
#                 amount=serializer.data['total_cost'],
#                 return_url='https://uzum.uz'
#             )
#             result['payment_link'] = payment_link
#         return response.Response(result)
