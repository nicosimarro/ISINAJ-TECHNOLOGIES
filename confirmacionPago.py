def payment_execute(request):  
  
    PAGO PAGOTY.GET.GET ("PAGO PAGO") #   I  
         PAYERID = SOLICITUD.GET.GET ("PAGADORIDAD") # ID de carga útil  
  
    payment = paypalrestsdk.Payment.find(paymentid)  
  
  
    if payment.execute({"payer_id": payerid}):  
        print("Payment execute successfully")  
                 Devuelve HTTPRESPONSE ("PAGO EXITAL")  
    else:  
        print(payment.error) # Error Hash  
                 Devuelve HTTPRESPONSE ("FACIDAD DE PAGO")