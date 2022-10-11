from datetime import datetime

from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from apps.payments.models import LNMOnline, C2BPayments
from apps.payments.api.serializers import LNMOnlineSerializer, C2BPaymentSerializer


class LNMCallbackUrlAPIView(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
        checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
        result_code = request.data["Body"]["stkCallback"]["ResultCode"]
        result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
        amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
        mpesa_receipt_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
        balance = ""
        transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
        phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
        str_transaction_date = str(transaction_date)
        transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")

        our_model = LNMOnline.objects.create(
            CheckoutRequestID=checkout_request_id,
            MerchantRequestID=merchant_request_id,
            Amount=amount,
            ResultCode=result_code,
            ResultDesc=result_description,
            MpesaReceiptNumber=mpesa_receipt_number,
            Balance=balance,
            TransactionDate=transaction_datetime,
            PhoneNumber=phone_number,
        )
        our_model.save()
        from rest_framework.response import Response
        return Response({"OurResultDesc": "YEEY!!! It worked!"})


class C2BValidationAPIView(CreateAPIView):
    queryset = C2BPayments.objects.all()
    serializer_class = C2BPaymentSerializer
    permission_classes = [AllowAny]

    # def create(self, request):
    #     print(request.data, "this is request.data in Validation")

    #     from rest_framework.response import Response
    #     my_headers = self.get_success_headers(request.data)

    #     return Response({
    #         "ResultCode": 1,
    #         "ResponseDesc":"Failed!"
    #     },
    #     headers=my_headers)


class C2BConfirmationAPIView(CreateAPIView):
    queryset = C2BPayments.objects.all()
    serializer_class = C2BPaymentSerializer
    permission_classes = [AllowAny]

    # def create(self, request):
    #     print(request.data, "this is request.data in Confirmation")

    #     """
    #     {'TransactionType': 'Pay Bill',
    #     'TransID': 'NCQ61H8BK4',
    #      'TransTime': '20190326210441',
    #       'TransAmount': '2.00',
    #       'BusinessShortCode': '601445',
    #        'BillRefNumber': '12345678',
    #        'InvoiceNumber': '',
    #        'OrgAccountBalance': '18.00',
    #        'ThirdPartyTransID': '',
    #        'MSISDN': '254708374149',
    #        'FirstName': 'John',
    #        'MiddleName': 'J.',
    #        'LastName': 'Doe'
    #        }
    #        this is request.data in Confirmation
    #        """

    #     from rest_framework.response import Response

    #     return Response({"ResultDesc": 0})
