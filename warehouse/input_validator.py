import re
import click

class InputValidator: 
    @staticmethod
    def validation(expression, error_message):
        if expression: return True
        
        click.echo(error_message)
        return False
                
    @staticmethod   
    def validate_id(input_id):
        is_valid = re.match(r"^\d{4}$", str(input_id))
        if not is_valid:
            click.echo('Invalid ID. Please provide a 4-digit number')
        return is_valid

    @staticmethod
    def validate_quantity(input_quantity):
        is_valid = re.match(r"^[0-9]+$", str(input_quantity))
        return InputValidator.validation(is_valid, 'Invalid Quantity. Please provide a number')

    @staticmethod
    def validate_price(input_price):
        is_valid = re.match(r"^[0-9]+(\.[0-9]+)?$", str(input_price))
        return InputValidator.validation(is_valid, 'Invalid Price. Please provide a number')

    @staticmethod
    def validate_attribute(input_attribute, input_value):
        if input_attribute in ["name", "location"] : 
            return True
        elif input_attribute == "quantity": 
            return InputValidator.validate_quantity(input_value)
        elif input_attribute == "price": 
            return InputValidator.validate_price(input_value)
