import json
from click.testing import CliRunner
from main import cli

runner = CliRunner()

def test_display_command():
    result = runner.invoke(cli, ['display'])
    assert result.exit_code == 0
    assert json.loads(result.output)  # Assuming it's a valid JSON output

def test_add_command():
    result = runner.invoke(cli, ['add', '-i', '1234', '-n', 'TestProduct', '-q', '10', '-p', '19.99', '-l', 'A1'])
    assert result.exit_code == 0
    assert 'Product added successfully.' in result.output

def test_search_command():
    # Assuming there's a product with ID 1234 in the inventory
    result = runner.invoke(cli, ['search', '-i', '1234'])
    assert result.exit_code == 0
    assert 'TestProduct' in result.output  # Assuming product name is displayed in the search result

# Add more test cases as needed
    
def test_alter_command():
    # Assuming there's a product with ID 1234 in the inventory
    result = runner.invoke(cli, ['alter', '-i', '1234', '-a', 'name', '-v', 'NewName'])
    assert result.exit_code == 0
    assert 'Product altered successfully.' in result.output

    # Test case where the product with the specified ID is not found
    result = runner.invoke(cli, ['alter', '-i', '5678', '-a', 'name', '-v', 'NewName'])
    assert result.exit_code == 0
    assert 'Product with ID 5678 not found in the inventory.' in result.output
    
def test_delete_command():

    # Assuming there's a product with ID 1234 in the inventory
    
    result = runner.invoke(cli, ['delete', '-i', '1234'])
    assert result.exit_code == 0
    assert 'Product with ID 1234 deleted successfully.' in result.output
    
    # Test case where the product with the specified ID is not found
    result = runner.invoke(cli, ['delete', '-i', '5678'])
    assert result.exit_code == 0
    assert 'Product with ID 5678 not found in the inventory.' in result.output
    


if __name__ == '__main__':
    test_add_command()
    test_display_command()
    test_search_command()
    test_delete_command()
    test_alter_command()