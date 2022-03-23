var stripe = Stripe(
    "pk_test_51KcsBHAy2cl6Tre5JpSOqBvh2j4Byp9Jj4EyRpQb53HsfxyOTKeFkPkxUC2nMFUbIByM7cLufmwOiTN20mwLAMDZ00UYYzKggf"
);

var elem = document.getElementById("submit");
clientsecret = elem.getAttribute("data-secret");

var elements = stripe.elements();
var style = {
    base: {
        color: "#000",
        lineHeight: "2.4",
        fontSize: "16px",
    },
};
var card = elements.create("card", { style: style });

card.mount("#card-element");

card.on("change", function (event) {
    var displayError = document.getElementById("card-errors");
    if (event.error) {
        displayError.textContent = event.error.message;
        $("#card-errors").addClass("aler alert-info");
    } else {
        displayError.textContent = "";
        $("#card-errors").removeClass("alert alert-info");
    }
});

var form = document.getElementById("payment-form");

form.addEventListener("submit", function (ev) {
    ev.preventDefault();

    var custName = document.getElementById("custName").value;
    var custAdd = document.getElementById("custAdd").value;
    var custAdd2 = document.getElementById("custAdd2").value;
    var postCode = document.getElementById("postCode").value;

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/orders/add/",
        data: {
            order_key: clientsecret,
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: "post",
        },
        success: function (json) {
            console.log(json.success);

            stripe
                .confirmCardPayment(clientsecret, {
                    payment_method: {
                        card: card,
                        billing_details: {
                            address: {
                                line1: custAdd,
                                line2: custAdd2,
                                postal_code: postCode,
                            },
                            name: custName,
                        },
                    },
                })
                .then(function (result) {
                    if (result.error) {
                        // Show error to your customer (for example, insufficient funds)
                        console.log(result.error.message);
                    } else {
                        // The payment has been processed!
                        if (result.paymentIntent.status === "succeeded") {
                            console.log("payment processed");
                            // Show a success message to your customer
                            // There's a risk of the customer closing the window before callback
                            // execution. Set up a webhook or plugin to listen for the
                            // payment_intent.succeeded event that handles any business critical
                            // post-payment actions.
                            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
                        }
                    }
                });
        },
    });
});
