import paypalrestsdk  
  
  
  
def payment(request):  
  
    paypalrestsdk.configure({  
     "Modo": "Sandbox", # Sandbox representa la caja de arena  
     "Client_ID": "Your Client_ID,  
     "Client_Secret": "Your Client_Secret"})  
  
    payment = paypalrestsdk.Payment({  
        "intent": "sale",  
        "payer": {  
            "payment_method": "paypal"},  
        "redirect_urls": {  
                         "return_url": "http: // localhost: 127.0.0.1 / palpay / paga /", # pague la página de salto sucesivo  
                         "Cancel_url": "http: // localhost: 127.0.0.2/ Pay / Can /"}, #Página de pago  
        "transactions": [{  
            "amount": {  
                "total": "5.00",  
                "currency": "USD"},  
                         "Descripción": "Esta es una prueba de pedido"}]})  
  
    if payment.create():  
        print("Payment created successfully")  
        for link in payment.links:  
            if link.rel == "approval_url":  
                approval_url = str(link.href)  
                print("Redirect for approval: %s" % (approval_url))  
                return redirect(approval_url)  
    else:  
        print(payment.error)  
                 Devuelve HTTPRESPONSE ("FACIDAD DE PAGO")