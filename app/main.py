from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.utils.config_loader import ConfigLoader
from app.utils.data_processor import DataProcessor
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path

app = FastAPI()

# Get the current directory (data-ai)
CURRENT_DIR = Path(__file__).parent

# Initialize configuration
config_loader = ConfigLoader()
data_processor = DataProcessor(config_loader)
dashboard_config = config_loader.get_dashboard_config()

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(CURRENT_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(CURRENT_DIR / "templates"))

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "dashboard_config": dashboard_config,
            "categories": config_loader.get_categories_config()
        }
    )

@app.get("/api/data")
async def get_chart_data(
    x_column: str = None,
    y_column: str = None,
    chart_type: str = None
):
    try:
        # Use default columns if not specified
        x_column = x_column or 'publishedAt'
        y_column = y_column or 'count'
        
        # Fetch and process data
        df = data_processor.fetch_data()
        
        # Process chart data
        return data_processor.process_for_chart(df, x_column, y_column)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/news")
async def get_news_data(x_column: str = None, y_column: str = None):
    try:
        # Fetch categorized news data
        categorized_data = data_processor.fetch_news_data()
        
        # Process chart data for each category
        charts_data = {}
        for cat_id, cat_df in categorized_data.items():
            charts_data[cat_id] = data_processor.process_for_chart(
                cat_df, 
                x_column or 'publishedAt', 
                y_column or 'count'
            )
        
        return charts_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"An error occurred: {str(exc)}"}
    )