import re


class DetailsExtractor:
    def __init__(self, input_str: str):
        self.input_str = input_str

    def extract_details(self) -> dict:
        details = {}
        details['Name'] = self._extract_detail(r'Name:\s*(.*?)(?:\r\n|<)')
        details['Phone'] = self._extract_detail(r'Phone:\s*(\d+)(?:\r\n|<)')
        details['City'] = self._extract_detail(r'City:\s*(.*?)(?:\r\n|<)')
        return details

    def _extract_detail(self, pattern: str) -> str:
        match = re.search(pattern, self.input_str)
        return match.group(1).strip() if match else None
