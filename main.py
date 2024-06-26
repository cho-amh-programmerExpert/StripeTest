import stripe
import streamlit as st
import re

# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = 'rk_test_51NpGIQB18XMg1fJznbCkVWsd0m0Vhycy4Ro1LkBtgOfw3gpXgYlQjMqHKYW6Pl3QP7BVHmVNIOMfFti6UteZgnEh00L4vlXDJp'

def extract_payment_link_id_from_url(url):
    # Assuming the payment link ID follows a specific pattern, e.g., pl_XXXXXXXXXXXXXX
    match = re.search(r'pl_[A-Za-z0-9]+', url)
    if match:
        return match.group(0)
    else:
        raise ValueError("Invalid payment link URL")

def retrieve_customers_from_payment_link_url(payment_link_url):
    customers = set()
    try:
        # Extract the payment link ID from the URL
        payment_link_id = extract_payment_link_id_from_url(payment_link_url)
        
        # Fetch the payment link to get associated PaymentIntents
        payment_link = stripe.PaymentLink.retrieve(payment_link_id)
        
        # List all PaymentIntents associated with the payment link
        payment_intents = stripe.PaymentIntent.list(
            payment_link=payment_link_id
        )
        
        for payment_intent in payment_intents.auto_paging_iter():
            if payment_intent.customer:
                customers.add(payment_intent.customer)
                
    except stripe.error.StripeError as e:
        print(f"Error fetching data from Stripe: {e.user_message}")
    except ValueError as e:
        print(f"Error: {e}")
    
    return list(customers)

# Example usage:
payment_link_url = 'https://buy.stripe.com/test_4gw3cPeQh1AJ824145'
st.write(payment_link_url)
customers = retrieve_customers_from_payment_link_url(payment_link_url)
st.write(customers)
