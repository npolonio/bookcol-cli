import re

class InputValidator: 

#VALIDATE-ID:
    @staticmethod
    def validate_id(input_id):      
        return bool(re.match(r"^\d{4}$", str(input_id))) #return true if compliant

