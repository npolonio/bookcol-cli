import re
import click
import logging


class InputValidator:
    LOG_FILE_NAME = 'inventory.log'
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO, format=LOG_FORMAT)

    ID_PATTERN = re.compile(r"^\d{4}$")
    QUANTITY_PATTERN = re.compile(r"^[0-9]+$")
    PRICE_PATTERN = re.compile(r"^[0-9]+(\.[0-9]+)?$")


    @staticmethod
    def configure_logging(log_file_name='inventory.log', log_level=logging.INFO, log_format='%(asctime)s - %(levelname)s - %(message)s'):
        logging.basicConfig(filename=log_file_name, level=log_level, format=log_format)


    @staticmethod
    def validation(expression, error_message):
        if expression:
            return True

        click.echo(f'Error: {error_message}')
        logging.error(error_message)
        return False


    @staticmethod
    def validate_id(input_id):
        is_valid = InputValidator.ID_PATTERN.match(str(input_id))
        if not is_valid:
            click.echo('Error: Invalid ID. Please provide a 4-digit number')
            logging.error(f"Invalid ID: {input_id}")
        return is_valid


    @staticmethod
    def validate_quantity(input_quantity):
        return InputValidator.validation(InputValidator.QUANTITY_PATTERN.match(str(input_quantity)), 'Invalid Quantity. Please provide a number')


    @staticmethod
    def validate_price(input_price):
        return InputValidator.validation(InputValidator.PRICE_PATTERN.match(str(input_price)), 'Invalid Price. Please provide a number')


    @staticmethod
    def validate_attribute(input_attribute, input_value):
        VALID_ATTRIBUTES = ["name", "location", "quantity", "price"]
        if input_attribute in VALID_ATTRIBUTES:
            if input_attribute == "quantity":
                return InputValidator.validate_quantity(input_value)
            elif input_attribute == "price":
                return InputValidator.validate_price(input_value)
            return True
        else:
            return InputValidator.validation(False, f'Invalid attribute: {input_attribute}')

