# fb_market_organizer

An automated tool that uses OpenAI's GPT-4 Vision to analyze furniture images and generate professional Facebook Marketplace listings. The bot analyzes images, generates descriptions, suggests pricing, and exports listing data to CSV format.

## Features

- AI-powered furniture image analysis using GPT-4 Vision
- Automated generation of listing titles and descriptions
- Smart price suggestions based on visual assessment
- Condition categorization (New to Used-Fair)
- Bulk image processing
- CSV export functionality

## Installation

1. Clone the repository:
```bash
git clone https://github.com/carlyleong/fb_market_organizer.git
cd fb_market_organizer
```

2. Install dependencies:
```bash
pip install pillow python-dotenv openai
```

3. Create a `.env` file and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Create a `data` directory and add your furniture images:
```
fb_market_organizer/
├── data/
│   ├── furniture1.jpg
│   ├── furniture2.png
│   └── ...
└── organizer.py
```

2. Run the script:
```bash
python organizer.py
```

The program will process all images and generate a `fb_marketplace_listings.csv` file with the listing details.

## Output

The CSV output includes:
- Title (150 char max)
- Price in USD
- Condition
- Detailed description with dimensions and delivery info
- Furniture category

## License

MIT License

## Note

This tool is for educational purposes. Please ensure compliance with Facebook Marketplace's terms of service.
