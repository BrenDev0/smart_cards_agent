import pandas as pd
import io
from typing import Dict, Any, List

class SheetsService:
    """Service for parsing spreadsheet files (CSV, Excel) to structured data."""
    
    SUPPORTED_EXTENSIONS = (".csv", ".xlsx", ".xls")
    
    def __init__(self, encodings: List[str] = None):
        """Initialize with optional custom encodings for CSV files."""
        self.encodings = encodings or ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
    
    def parse_file_to_dicts(self, filename: str, content: bytes) -> List[Dict[str, Any]]:
        """Parse file content directly to list of dictionaries."""
        df = self.parse_file(filename, content)
        return self.convert_to_dicts(df)
    
    def parse_file(self, filename: str, content: bytes) -> pd.DataFrame:
        """Parse file content to DataFrame with automatic cleanup."""
        if not filename.lower().endswith(self.SUPPORTED_EXTENSIONS):
            raise ValueError(f"Unsupported file type. Supported: {', '.join(self.SUPPORTED_EXTENSIONS)}")
        
        try:
            if filename.lower().endswith(".csv"):
                df = self._read_csv(content)
            elif filename.lower().endswith((".xlsx", ".xls")):
                df = self._read_excel(content, filename)
            else:
                raise ValueError(f"Unsupported file extension: {filename}")
            
            return self._cleanup_dataframe(df)
            
        except Exception as e:
            raise ValueError(f"Error parsing {filename}: {str(e)}")
    
    def _read_csv(self, content: bytes) -> pd.DataFrame:
        """Read CSV with encoding detection."""
        for encoding in self.encodings:
            try:
                return pd.read_csv(io.BytesIO(content), encoding=encoding)
            except UnicodeDecodeError:
                continue
        
        raise ValueError(f"Unable to decode CSV with encodings: {', '.join(self.encodings)}")
    
    def _read_excel(self, content: bytes, filename: str) -> pd.DataFrame:
        """Read Excel file."""
        engine = "openpyxl" if filename.lower().endswith(".xlsx") else "xlrd"
        return pd.read_excel(io.BytesIO(content), engine=engine)
    
    def _cleanup_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean up DataFrame: remove empty rows, detect headers, clean column names."""
        if df.empty:
            return df
        
        # Drop fully empty rows
        df = df.dropna(how="all").reset_index(drop=True)
        
        if df.empty:
            return df
        
        # Try to detect header row (if not already set)
        if df.columns.dtype == 'object':  # Headers already detected
            # Clean existing column names
            df.columns = self._clean_column_names(df.columns)
        else:
            # Auto-detect header row
            header_row_idx = self._detect_header_row(df)
            df.columns = self._clean_column_names(df.iloc[header_row_idx])
            df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
        
        # Replace NaN with None for clean JSON serialization
        df = df.where(pd.notnull(df), None)
        
        return df
    
    def _detect_header_row(self, df: pd.DataFrame) -> int:
        """Detect which row contains the headers."""
        max_rows_to_check = min(5, len(df))
        
        for i in range(max_rows_to_check):
            row = df.iloc[i]
            # Count non-null string values
            string_count = sum(1 for x in row if isinstance(x, str) and x.strip())
            ratio = string_count / len(row) if len(row) > 0 else 0
            
            # If 75% or more are meaningful strings, likely a header
            if ratio >= 0.75:
                return i
        
        return 0
    
    def _clean_column_names(self, columns) -> List[str]:
        """Clean and normalize column names."""
        cleaned = []
        for i, col in enumerate(columns):
            if pd.isna(col) or str(col).strip() == "":
                clean_name = f"column_{i}"
            else:
                clean_name = (str(col)
                             .strip()
                             .lower()
                             .replace(" ", "_")
                             .replace("-", "_")
                             .replace(".", "_"))
            cleaned.append(clean_name)
        
        return cleaned
    
    def convert_to_dicts(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Convert DataFrame to list of dictionaries."""
        if df.empty:
            return []
        
        return df.to_dict(orient="records")
