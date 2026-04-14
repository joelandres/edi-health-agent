import re

class EDIParser:
    def __init__(self, raw_data):
        # EDI segments are usually separated by ~
        self.segments = raw_data.strip().split('~')

    def get_codes(self):
        extracted = {"diagnosis": [], "procedure": []}
        for segment in self.segments:
            parts = segment.split('*')
            # HI segment usually contains ICD-10 Diagnosis codes
            if parts[0] == 'HI':
                # Example: HI*BK:M17.11 (M17.11 is the code)
                code = parts[1].split(':')[-1]
                extracted["diagnosis"].append(code)
            # SVC segment usually contains CPT Procedure codes
            elif parts[0] == 'SVC':
                # Example: SVC*HC:73721 (73721 is the code)
                code = parts[1].split(':')[-1]
                extracted["procedure"].append(code)
        return extracted

# Quick Test
if __name__ == "__main__":
    sample_278 = "ISA*00*...~HI*BK:M17.11~SVC*HC:73721*1~SE*10*0001~"
    parser = EDIParser(sample_278)
    print(f"Extracted Data: {parser.get_codes()}")