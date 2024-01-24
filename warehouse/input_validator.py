import re
import click
import logging

logging.basicConfig(filename='inventory.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class InputValidator: 
    @staticmethod
    def validation(expression, error_message):
        if expression: 
            return True
        
        click.echo(f'Error: {error_message}')
        logging.error(error_message)
        return False
                
    @staticmethod   
    def validate_id(input_id):#Could I refactor this method so it uses 'validation'?
        is_valid = re.match(r"^\d{4}$", str(input_id))
        if not is_valid:
            click.echo('Error: Invalid ID. Please provide a 4-digit number')
            logging.error(f"Invalid ID: {input_id}")
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
    def validate_attribute(input_attribute, input_value): #Could I move this check to the alter command?
        if input_attribute in ["name", "location"] : 
            return True
        elif input_attribute == "quantity": 
            return InputValidator.validate_quantity(input_value)
        elif input_attribute == "price": 
            return InputValidator.validate_price(input_value)
