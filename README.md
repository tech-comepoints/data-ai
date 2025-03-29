# Data Analytics Dashboard

A configurable data analytics dashboard built with Python, FastAPI, and Plotly.

## Features

- Configurable data sources via API
- Custom data categorization
- Interactive charts and visualizations
- Real-time data updates
- Flexible dashboard layout

## Installation

1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/data-dashboard.git
cd data-dashboard
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure the dashboard
- Edit `app/config/config.yaml` with your settings

5. Run the application
```bash
uvicorn app.main:app --reload
```

## Configuration

The dashboard can be configured through `app/config/config.yaml`:

- API endpoints and authentication
- Data categories and filtering rules
- Chart types and layout
- Refresh intervals

## Usage

1. Access the dashboard at `http://localhost:8000`
2. Select data columns for X and Y axes
3. Choose chart types
4. View categorized data visualizations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 