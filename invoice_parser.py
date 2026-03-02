# invoice_parser.py
import pdfplumber
import re
import json
from datetime import datetime

class InvoiceParser:
    """
    PDF Invoice Parser
    Extracts structured data from invoice PDFs
    """
    
    def __init__(self, pdf_path):
        """
        Initialize parser with PDF file path
        
        Args:
            pdf_path: Path to the invoice PDF file
        """
        self.pdf_path = pdf_path
        self.data = {
            "invoice_number": None,
            "date": None,
            "customer": None,
            "items": [],
            "subtotal": None,
            "tax": None,
            "discount": None,
            "total": None
        }
    
    def parse(self):
        """
        Main parsing function - extracts all invoice data
        
        Returns:
            dict: Structured invoice data
        """
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                # Get first page (invoices are usually single page)
                page = pdf.pages[0]
                
                # Extract raw text for pattern matching
                text = page.extract_text()
                
                # Extract each component
                self._extract_invoice_number(text)
                self._extract_date(text)
                self._extract_customer(text)
                self._extract_line_items(page)
                self._extract_totals(text)
                
                return self.data
                
        except Exception as e:
            print(f"❌ Error parsing invoice: {e}")
            return None
    
    def _extract_invoice_number(self, text):
        """
        Extract invoice number using regex pattern matching
        
        Looks for patterns like:
        - Invoice #: INV-2025-001234
        - Invoice: 001234
        - INV-001234
        """
        # Try different invoice number patterns
        patterns = [
            r"Invoice\s*#?:?\s*([A-Z0-9-]+)",  # Invoice #: INV-2025-001234
            r"Invoice\s*Number:?\s*([A-Z0-9-]+)",  # Invoice Number: 001234
            r"INV[-\s]?(\d+)",  # INV-001234 or INV 001234
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                self.data["invoice_number"] = match.group(1)
                break
    
    def _extract_date(self, text):
        """
        Extract invoice date
        
        Supports multiple date formats:
        - MM/DD/YYYY (03/02/2025)
        - DD-MM-YYYY (02-03-2025)
        - YYYY-MM-DD (2025-03-02)
        """
        # Try different date patterns
        patterns = [
            r"Date:?\s*(\d{2}/\d{2}/\d{4})",  # MM/DD/YYYY
            r"Date:?\s*(\d{2}-\d{2}-\d{4})",  # DD-MM-YYYY
            r"Date:?\s*(\d{4}-\d{2}-\d{2})",  # YYYY-MM-DD
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                self.data["date"] = match.group(1)
                break
    
    def _extract_customer(self, text):
        """
        Extract customer name
        
        Looks for:
        - Bill To: Customer Name
        - Customer: Customer Name
        """
        patterns = [
            r"Bill\s+To:?\s+([A-Za-z\s]+)",
            r"Customer:?\s+([A-Za-z\s]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Get customer name and clean it
                customer = match.group(1).strip()
                # Take only the first line (name only, not address)
                customer = customer.split('\n')[0]
                self.data["customer"] = customer
                break
    
    def _extract_line_items(self, page):
        """
        Extract line items table
        
        Looks for a table with columns like:
        Item | Description | Qty | Unit Price | Amount
        """
        # Extract all tables from the page
        tables = page.extract_tables()
        
        if not tables:
            return
        
        # Find the items table (usually the largest table)
        items_table = None
        for table in tables:
            # Items table should have at least 5 columns and multiple rows
            if table and len(table) > 1 and len(table[0]) >= 4:
                items_table = table
                break
        
        if not items_table:
            return
        
        # First row is headers, rest are items
        headers = items_table[0]
        rows = items_table[1:]
        
        # Convert to list of dictionaries
        for row in rows:
            # Skip rows that look like subtotals/totals
            if any(keyword in str(row[0]).lower() 
                   for keyword in ['subtotal', 'tax', 'total', 'discount']):
                continue
            
            # Create item dictionary
            item = {
                "item": row[0] if len(row) > 0 else "",
                "description": row[1] if len(row) > 1 else "",
                "quantity": row[2] if len(row) > 2 else "",
                "unit_price": row[3] if len(row) > 3 else "",
                "amount": row[4] if len(row) > 4 else ""
            }
            
            # Only add if item has a name
            if item["item"] and item["item"].strip():
                self.data["items"].append(item)
    
    def _extract_totals(self, text):
        """
        Extract subtotal, tax, discount, and final total
        
        Looks for patterns like:
        - Subtotal: $5,400.00
        - Tax (10%): $540.00
        - Discount: -$100.00
        - Total: $5,840.00
        """
        # Pattern to match currency amounts
        # Matches: $1,234.56 or 1234.56 or $1234.56
        amount_pattern = r"\$?\s*[\d,]+\.?\d*"
        
        # Subtotal
        subtotal_match = re.search(
            rf"Subtotal:?\s*({amount_pattern})", 
            text, 
            re.IGNORECASE
        )
        if subtotal_match:
            self.data["subtotal"] = subtotal_match.group(1)
        
        # Tax
        tax_match = re.search(
            rf"Tax[^:]*:?\s*({amount_pattern})", 
            text, 
            re.IGNORECASE
        )
        if tax_match:
            self.data["tax"] = tax_match.group(1)
        
        # Discount
        discount_match = re.search(
            rf"Discount:?\s*(-?{amount_pattern})", 
            text, 
            re.IGNORECASE
        )
        if discount_match:
            self.data["discount"] = discount_match.group(1)
        
        # Total (final amount)
        # Look for "Total:" that's NOT "Subtotal:"
        total_match = re.search(
            rf"(?<!Sub)Total:?\s*({amount_pattern})", 
            text, 
            re.IGNORECASE
        )
        if total_match:
            self.data["total"] = total_match.group(1)
    
    def save_json(self, output_path="invoice_data.json"):
        """
        Save parsed data to JSON file
        
        Args:
            output_path: Path for output JSON file
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved to {output_path}")
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
    
    def display(self):
        """
        Print formatted invoice data to console
        """
        print("\n" + "="*60)
        print("📄 INVOICE PARSER RESULTS")
        print("="*60)
        
        # Basic info
        print(f"\n📋 Invoice Details:")
        print(f"   Invoice #: {self.data['invoice_number']}")
        print(f"   Date: {self.data['date']}")
        print(f"   Customer: {self.data['customer']}")
        
        # Line items
        print(f"\n📦 Line Items ({len(self.data['items'])} items):")
        for i, item in enumerate(self.data['items'], 1):
            print(f"\n   {i}. {item['item']}")
            if item['description']:
                print(f"      Description: {item['description']}")
            print(f"      Qty: {item['quantity']} | "
                  f"Unit Price: {item['unit_price']} | "
                  f"Amount: {item['amount']}")
        
        # Totals
        print(f"\n💰 Financial Summary:")
        if self.data['subtotal']:
            print(f"   Subtotal: {self.data['subtotal']}")
        if self.data['tax']:
            print(f"   Tax: {self.data['tax']}")
        if self.data['discount']:
            print(f"   Discount: {self.data['discount']}")
        if self.data['total']:
            print(f"   TOTAL: {self.data['total']}")
        
        print("\n" + "="*60 + "\n")


def main():
    """
    Main function - demonstrates usage
    """
    # Parse the invoice
    parser = InvoiceParser("sample_invoice.pdf")
    
    print("🔍 Parsing invoice...")
    data = parser.parse()
    
    if data:
        # Display results
        parser.display()
        
        # Save to JSON
        parser.save_json("invoice_data.json")
        
        # Also print raw JSON
        print("📄 JSON Output:")
        print(json.dumps(data, indent=2))
    else:
        print("❌ Failed to parse invoice")


if __name__ == "__main__":
    main()

