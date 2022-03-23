
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from basket.basket import Basket
from orders.views import payment_confirmation
import stripe
import json

# Create your views here.


@login_required
def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace(".", "")
    total = int(total)

    stripe.api_key = settings.STRIPE_API_KEY
    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency="usd",
            metadata={"userid": request.user.id}
        )
        return render(request, "payment/index.html", {
            'client_secret': intent.client_secret
        })

    except:
        return


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


@login_required
def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "payment/orderplaced.html", {})
