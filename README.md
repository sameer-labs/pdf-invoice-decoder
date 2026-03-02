# 📄 PDF Invoice Decoder

*Because copy-pasting invoice data like it's 1995 is beneath us.*

## What's This About?

I needed to extract data from a bunch of invoices for... reasons. Typing everything manually? No thanks. So I learned PDFplumber and built this parser that pulls out all the important stuff:

- Invoice numbers
- Dates
- Customer names
- Line items (with all the details)
- Totals, tax, discounts - the whole financial breakdown

Now I can just point it at an invoice PDF and get clean JSON out. Much better.

## Why I Built This

**The real reason:** I'm building a larger AI study assistant (name hasn't been decided) that processes PDFs, YouTube videos, and other content to help me learn better. To do that properly, I needed to actually *understand* PDF processing, not just use it superficially.

So I decided to learn PDFplumber by building something practical - an invoice parser. Why invoices?

1. **They have structure** - Tables, key-value pairs, totals. Perfect for learning extraction techniques.
2. **Real-world use case** - Business students deal with invoices all the time (looking at you, accounting majors 👀)
3. **Transferable skills** - Once you can parse an invoice, you can parse lecture notes, financial statements, research papers, whatever.

**The business student angle:** If you're in business school and drowning in case studies about invoice processing, supply chain management, or financial analysis... this might actually save you some time. Instead of manually entering data from invoice PDFs into Excel for your assignments, just run this and get JSON out. Convert to CSV, import to Excel, done. You're welcome.

## Features That Work

✅ **Extracts everything:**
- Invoice number (INV-2025-001234)
- Invoice date (MM/DD/YYYY)
- Customer name
- Full line items table (item, description, quantity, price, amount)
- Financial breakdown (subtotal, tax, discount, total)

✅ **Multiple output formats:**
- Pretty console display (for humans)
- Clean JSON export (for machines/APIs)

✅ **Clean code:**
- Well-commented (I tried)
- Object-oriented design
- Error handling that doesn't crash silently

✅ **Sample invoice included:**
- Realistic fake invoice to test with
- Generated with reportlab (thanks, Claude, for that part!)

## Getting Started

### Install Dependencies
```bash
pip install pdfplumber reportlab
```

### Generate Sample Invoice
```bash
python create_sample_invoice.py
```

This creates `sample_invoice.pdf` with fake data you can test on.

### Parse the Invoice
```bash
python invoice_parser.py
```

You'll get:
1. Formatted console output (easy to read)
2. JSON file (`invoice_data.json`)

### Use Your Own Invoice
```python
from invoice_parser import InvoiceParser

parser = InvoiceParser("your_invoice.pdf")
data = parser.parse()
parser.display()
parser.save_json("output.json")
```

## Project Structure
```
pdf-invoice-decoder/
│
├── create_sample_invoice.py   # Generates sample invoice PDF
├── invoice_parser.py           # Main parser (the good stuff)
├── sample_invoice.pdf          # Example invoice (generated)
├── invoice_data.json           # Parsed output (generated)
├── requirements.txt            # Dependencies
└── README.md                   # You are here
```

## Example Output

**Console:**
```
============================================================
📄 INVOICE PARSER RESULTS
============================================================

📋 Invoice Details:
   Invoice #: INV-2025-001234
   Date: 03/02/2025
   Customer: Bob Marley

📦 Line Items (5 items):

   1. Web Development
      Description: Custom website design and development
      Qty: 1 | Unit Price: $2,500.00 | Amount: $2,500.00

   2. API Integration
      Description: Third-party API setup and testing
      Qty: 3 | Unit Price: $450.00 | Amount: $1,350.00
   
   [... more items ...]

💰 Financial Summary:
   Subtotal: $5,400.00
   Tax: $540.00
   Discount: -$100.00
   TOTAL: $5,840.00
```

**JSON:**
```json
{
  "invoice_number": "INV-2025-001234",
  "date": "03/02/2025",
  "customer": "Sameer Ahmed",
  "items": [
    {
      "item": "Web Development",
      "description": "Custom website design and development",
      "quantity": "1",
      "unit_price": "$2,500.00",
      "amount": "$2,500.00"
    }
  ],
  "total": "$5,840.00"
}
```

## How It Works

1. **Opens PDF** with pdfplumber
2. **Extracts text** from first page (invoices are usually single-page)
3. **Uses regex** to find invoice number, date, customer name
4. **Extracts table** for line items
5. **Parses totals** (subtotal, tax, discount, final amount)
6. **Outputs** to console and JSON

The code is heavily commented, so you can see what's happening at each step. I learned this stuff so you can too.

## What I Learned

**pdfplumber is powerful, but PDFs are messy:**
- Text extraction works well for typed PDFs
- Tables are tricky but doable with `extract_table()`
- Scanned PDFs (images) won't work without OCR
- Every invoice format is different (regex patterns need tweaking)

**Regex is your friend:**
- Pattern matching is essential for extracting structured data
- Multiple patterns needed for flexibility (different date formats, etc.)
- Test with real-world examples, not just perfect data

**Error handling matters:**
- PDFs fail in creative ways
- Always use try/except blocks
- Validate extracted data before using it

## Limitations (Being Honest)

- **Only works with typed PDFs** - Scanned/image PDFs need OCR (not included)
- **Single page assumed** - Multi-page invoices might break
- **Format-specific** - Different invoice layouts need pattern adjustments
- **No validation** - Doesn't check if totals add up (could add this though)
- **Basic parsing** - Won't handle super complex invoices with weird layouts

Basically, it works great for standard invoices, but YMMV with exotic formats.

## Ideas I Didn't Implement (Yet)

Could add:
- Batch processing (parse entire folders of invoices)
- Export to CSV/Excel for easy analysis
- Validation (check if line items sum to subtotal)
- Support for multi-page invoices
- OCR for scanned invoices (pytesseract)
- Web interface (Flask/Streamlit)
- Database storage (SQLite)

## Credits & Thanks

- **Claude Sonnet 4.5** for generating the sample invoice PDF and helping structure the parser when my brain was fried from exams
- **pdfplumber library** for making PDF extraction actually possible
- **reportlab** for PDF generation

## Related Projects

Check out my other learning projects:
- [youtube-quote-hunter](https://github.com/yourusername/youtube-quote-hunter) - Search YouTube transcripts
- [pdf-study-buddy](https://github.com/yourusername/pdf-study-buddy) - AI-powered study guide generator
- [grade-guardian](https://github.com/yourusername/grade-guardian) - Student performance tracker

All part of building my personal AI learning companion. We're getting there, one PDF at a time.

## License

MIT - Use it, modify it, sell it, I don't care. If it saves you from manually typing invoice data, that's payment enough.

Just don't blame me if it parses your invoice wrong and you accidentally pay $5,840 instead of $584.00. Double-check your numbers, friends.

---

**Made by an Engineering student during exam season who'd rather code than study. 

*If this saved you time, ⭐ it. If it didn't work, open an issue, and I'll fix it when exams are over.*

**Current status: Drowning in exams, but at least I'm learning coding** 📚😅
```
