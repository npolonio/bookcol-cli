from click.testing import CliRunner
from main import cli
import pytest

runner = CliRunner()

def test_display_command(): # Assuming there are products in the inventory
    result = runner.invoke(cli, ['display'])
    assert result.exit_code == 0
    assert 'Product' in result.output  # Assuming product information is displayed in the output

def test_add_command(): # Assuming there is no product with ID 1234 in the inventory
    result = runner.invoke(cli, ['add', '-i', '1234', '-n', 'TestProduct', '-q', '10', '-p', '19.99', '-l', 'A1'])
    assert result.exit_code == 0
    assert 'Product added successfully.' in result.output

def test_add_command_existing_id(): # Assuming there's a product with ID 1234 in the inventory
    result = runner.invoke(cli, ['add', '-i', '1234', '-n', 'NewProduct', '-q', '5', '-p', '25.99', '-l', 'B2'])
    assert result.exit_code == 0
    assert 'Product with ID 1234 already exists in the inventory.' in result.output

def test_add_command_invalid_numeric_input(): # Test case with invalid product ID
    result = runner.invoke(cli, ['add', '-i', '123456789', '-n', 'TestProduct', '-q', '10', '-p', '19.99', '-l', 'A1'])
    assert result.exit_code == 0
    assert 'Invalid ID. Please provide a 4-digit number' in result.output

def test_search_command(): # Assuming there's a product with ID 1234 in the inventory
    result = runner.invoke(cli, ['search', '-i', '1234'])
    assert result.exit_code == 0
    assert 'TestProduct' in result.output  # Assuming product name is displayed in the search result

def test_search_command_invalid_numeric_id(): # Test case with invalid product ID
    result = runner.invoke(cli, ['search', '-i', '123456789'])
    assert result.exit_code == 0
    assert 'Invalid ID. Please provide a 4-digit number' in result.output
  
def test_alter_command(): # Assuming there's a product with ID 1234 in the inventory
    result = runner.invoke(cli, ['alter', '-i', '1234', '-a', 'name', '-v', 'NewName'])
    assert result.exit_code == 0
    assert 'Product altered successfully.' in result.output

    # Test case where the product with the specified ID is not found
    result = runner.invoke(cli, ['alter', '-i', '5678', '-a', 'name', '-v', 'NewName'])
    assert result.exit_code == 0
    assert 'Product with ID 5678 not found in the inventory.' in result.output

def test_alter_command_invalid_attribute():
    # Test case with invalid attribute
    result = runner.invoke(cli, ['alter', '-i', '1234', '-a', 'invalid', '-v', 'NewValue'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for \'-a\' / \'--attribute\': \'invalid\' is not one of \'name\', \'quantity\', \'price\', \'location\'.' in result.output

def test_delete_command(): # Assuming there's a product with ID 1234 in the inventory
    result = runner.invoke(cli, ['delete', '-i', '1234'])
    assert result.exit_code == 0
    assert 'Product with ID 1234 deleted successfully.' in result.output
    
    # Test case where the product with the specified ID is not found
    result = runner.invoke(cli, ['delete', '-i', '5678'])
    assert result.exit_code == 0
    assert 'Product with ID 5678 not found in the inventory.' in result.output

def test_delete_command_invalid_id(): # Test case with invalid product ID
    result = runner.invoke(cli, ['delete', '-i', '123456789'])
    assert result.exit_code == 0
    assert 'Invalid ID. Please provide a 4-digit number' in result.output

def test_delete_command_nonexistent_id(): # Test case where the product with the specified ID is not found
    result = runner.invoke(cli, ['delete', '-i', '9999'])
    assert result.exit_code == 0
    assert 'Product with ID 9999 not found in the inventory.' in result.output

if __name__ == '__main__':
    pytest.main()
