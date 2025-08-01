const stripe = Stripe("pk_test_51RpRywGaYCvNHBeXxOBMxdvK8NvfXpwcxrCo7UP1WPCiyyaRb6p8lwCABzqcbDhwaJy3hIhTpZXKq0NlwVlpSvTg00ffPqYbGD");
const elements = stripe.elements();
const cardElement = elements.create("card");
cardElement.mount("#card_element");

const form = document.getElementById("payment_form");
const resultDiv = document.getElementById("payment_result");

const orderId = form.getAttribute("data-order-id");
const getClientSecretUrl = `/buy/${orderId}/`;

let clientSecret = "";

fetch(getClientSecretUrl, {
    method: 'GET',
    headers: {
        'X-Requested-With': 'XMLHttpRequest'
    }
})
.then(response => response.json())
.then(data => {
    if (!data.error) {
        clientSecret = data.content.client_secret;

        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const { error, paymentIntent } = await stripe.confirmCardPayment(
                clientSecret,
                {
                    payment_method: {
                        card: cardElement,
                    }
                }
            );

            if (error) {
                resultDiv.textContent = "Ошибка: " + error.message;
            } else if (paymentIntent.status === "succeeded") {
                resultDiv.textContent = "Оплата прошла успешно!";
            }
        });
    } else {
        alert("Ошибка при обработке запроса. Пожалуйста, попробуйте позже.");
    }
})
.catch(error => {
    console.error("Ошибка:", error);
    alert(error);
});
