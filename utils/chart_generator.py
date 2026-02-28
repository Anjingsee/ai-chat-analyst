import json
import logging

logger = logging.getLogger(__name__)

class ChartGenerator:
    """Generate chart configurations for frontend visualization"""
    
    async def generate_config(self, data: dict, chart_type: str) -> dict:
        """Generate chart configuration"""
        try:
            if chart_type == "bar":
                return self._generate_bar_chart(data)
            elif chart_type == "line":
                return self._generate_line_chart(data)
            elif chart_type == "pie":
                return self._generate_pie_chart(data)
            elif chart_type == "scatter":
                return self._generate_scatter_chart(data)
            elif chart_type == "heatmap":
                return self._generate_heatmap(data)
            else:
                return self._generate_default_chart(data)
        except Exception as e:
            logger.error(f"Error generating chart config: {str(e)}")
            return {"error": str(e)}
    
    def _generate_bar_chart(self, data: dict) -> dict:
        """Generate bar chart configuration"""
        return {
            "type": "bar",
            "title": "Bar Chart Analysis",
            "data": data,
            "options": {
                "responsive": True,
                "maintainAspectRatio": True
            }
        }
    
    def _generate_line_chart(self, data: dict) -> dict:
        """Generate line chart configuration"""
        return {
            "type": "line",
            "title": "Line Chart Analysis",
            "data": data,
            "options": {
                "responsive": True,
                "maintainAspectRatio": True
            }
        }
    
    def _generate_pie_chart(self, data: dict) -> dict:
        """Generate pie chart configuration"""
        return {
            "type": "pie",
            "title": "Pie Chart Analysis",
            "data": data,
            "options": {
                "responsive": True
            }
        }
    
    def _generate_scatter_chart(self, data: dict) -> dict:
        """Generate scatter chart configuration"""
        return {
            "type": "scatter",
            "title": "Scatter Chart Analysis",
            "data": data,
            "options": {
                "responsive": True,
                "maintainAspectRatio": True
            }
        }
    
    def _generate_heatmap(self, data: dict) -> dict:
        """Generate heatmap configuration"""
        return {
            "type": "heatmap",
            "title": "Heatmap Analysis",
            "data": data,
            "options": {
                "responsive": True
            }
        }
    
    def _generate_default_chart(self, data: dict) -> dict:
        """Generate default chart configuration"""
        return {
            "type": "generic",
            "title": "Data Visualization",
            "data": data
        }
