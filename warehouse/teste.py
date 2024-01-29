from unittest.mock import patch
from click.testing import CliRunner
from main import cli 

#1
def test_display_command_successfully(): #working
    runner = CliRunner()
    result = runner.invoke(cli, ['display'])

    assert result.exit_code == 0

#2
def test_add_command_successfully(): #working
    runner = CliRunner()
    result = runner.invoke(cli, ['add', '-i', '1234', '-n', 'Test Product', '-q', '10', '-p', '25.99', '-l', 'Warehouse'])

    assert result.exit_code == 0
    assert 'Product added successfully.' in result.output

#3
def test_add_command_invalid_id(): #working
    runner = CliRunner()
    result = runner.invoke(cli, ['add', '-i', '123456789', '-n', 'Test Product', '-q', '10', '-p', '25.99', '-l', 'Warehouse'])

    assert result.exit_code == 0
    assert 'Error: Invalid ID. Please provide a 4-digit number' in result.output

#4
def test_search_command_successfully(): #working
    runner = CliRunner()
    result = runner.invoke(cli, ['search', '-i', '1234'])

    assert result.exit_code == 0

    expected_output = """
--------------------
Product found with ID 1234:
Product Name: Test Product
Product Quantity: 10
Product Price: 25.99
Product Location: Warehouse
--------------------
"""
    assert result.output.strip() == expected_output.strip()

#5
def test_search_command_invalid_id(): #working
    runner = CliRunner()
    result = runner.invoke(cli, ['search', '-i', '123456789'])

    assert result.exit_code == 0
    assert 'Error: Invalid ID. Please provide a 4-digit number' in result.output

#6
def test_alter_command_successfully_change_name(): #working
    runner = CliRunner()
    result = runner.invoke(cli, ['alter', '-i', '1234', '-a', 'name', '-v', 'New Name' ])

    assert result.exit_code == 0
    assert 'Product altered successfully.' in result.output

#7
def test_alter_command_successfully_change_quantity(): #working
    runner = CliRunner()
    result = runner.invoke(cli, ['alter', '-i', '1234', '-a', 'quantity', '-v', '20' ])

    assert result.exit_code == 0
    assert 'Product altered successfully.' in result.output

#8
def test_alter_command_successfully_change_price(): #working
    runner = CliRunner()
    result = runner.invoke(cli, ['alter', '-i', '1234', '-a', 'price', '-v', '20.00' ])

    assert result.exit_code == 0
    assert 'Product altered successfully.' in result.output

#9
def test_alter_command_successfully_change_location(): #working
    runner = CliRunner()
    result = runner.invoke(cli, ['alter', '-i', '1234', '-a', 'location', '-v', 'New Location' ])

    assert result.exit_code == 0
    assert 'Product altered successfully.' in result.output

#10
@patch('click.confirm')
def test_delete_command_abort(mock_confirm): #working
    mock_confirm.return_value = False

    runner = CliRunner()
    result = runner.invoke(cli, ['delete', '-i', '1234'])

    assert result.exit_code == 0
    assert 'Deletion canceled.' in result.output

#11
@patch('click.confirm')
def test_delete_command_successfully(mock_confirm): #working
    mock_confirm.return_value = True

    runner = CliRunner()
    result = runner.invoke(cli, ['delete', '-i', '1234'])

    assert result.exit_code == 0
    assert 'Product with ID 1234 deleted successfully.' in result.output

#12
def test_delete_command_invalid_id(): #working
    runner = CliRunner()
    result = runner.invoke(cli, ['delete', '-i', '123456789'])

    assert result.exit_code == 0
    assert 'Error: Invalid ID. Please provide a 4-digit number' in result.output


