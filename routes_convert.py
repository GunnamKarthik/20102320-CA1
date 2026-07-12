# routes_convert.py - Currency conversion endpoint using ExchangeRate API
# Converts license costs from one currency to another using a free external API

from flask import Blueprint, request, jsonify
import requests

# Create a blueprint for currency conversion
convert_bp = Blueprint('convert', __name__)


@convert_bp.route('/api/convert', methods=['GET'])
def convert_currency():
    """Convert an amount from one currency to another.
    Uses the free Open ExchangeRate API (no API key needed).
    Query params: ?amount=100&from=USD&to=EUR"""

    # Get the query parameters
    amount = float(request.args.get('amount', 0))
    from_currency = request.args.get('from', 'USD').upper()
    to_currency = request.args.get('to', 'EUR').upper()

    try:
        # Call the free exchange rate API
        response = requests.get(
            f"https://open.er-api.com/v6/latest/{from_currency}",
            timeout=5
        )
        data = response.json()

        # Check if the API returned a valid response
        if data.get('result') != 'success':
            return jsonify({'error': 'Exchange rate API error'}), 502

        # Get the conversion rate for the target currency
        rate = data['rates'].get(to_currency)
        if rate is None:
            return jsonify({'error': f'Unknown currency: {to_currency}'}), 400

        # Calculate the converted amount and return it
        converted_amount = round(amount * rate, 2)
        return jsonify({
            'original': amount,
            'from': from_currency,
            'to': to_currency,
            'rate': rate,
            'converted': converted_amount
        })

    except requests.RequestException:
        # If the external API is unreachable, return a friendly error
        return jsonify({'error': 'Could not reach exchange rate service'}), 502
