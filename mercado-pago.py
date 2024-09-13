import mercadopago
from config import MERCADO_PAGO_ACCESS_TOKEN

sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)


def process_payment(valor, descricao):
    pagamento = {
        "transaction_amount": valor,
        "description": descricao,
        "payment_method_id": "pix",
        "payer": {
            "email": "email_do_cliente@email.com"
        }
    }
    resposta = sdk.payment().create(pagamento)
    return resposta
