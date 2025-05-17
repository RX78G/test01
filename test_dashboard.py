import unittest
from unittest.mock import patch, Mock
import pandas as pd
tempfile = __import__('tempfile')
from pathlib import Path

from dashboard import get_indicator_data

SAMPLE_JSON = [
    {"date": "2020", "value": 1},
    {"date": "2019", "value": None},
    {"date": "2018", "value": 2},
]

class TestGetIndicatorData(unittest.TestCase):
    def test_load_from_cache(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "JPN_NY.GDP.MKTP.CD.csv"
            pd.DataFrame(SAMPLE_JSON).to_csv(p, index=False)
            with patch('dashboard.requests.get') as mock_get:
                df = get_indicator_data('JPN', 'NY.GDP.MKTP.CD', cache_dir=Path(d))
                self.assertFalse(mock_get.called)
                self.assertEqual(len(df), 2)

    def test_fetch_from_api(self):
        with tempfile.TemporaryDirectory() as d:
            mock_resp = Mock()
            mock_resp.json.return_value = [None, SAMPLE_JSON]
            mock_resp.raise_for_status = lambda: None
            with patch('dashboard.requests.get', return_value=mock_resp) as mock_get:
                df = get_indicator_data('JPN', 'NY.GDP.MKTP.CD', cache_dir=Path(d))
                mock_get.assert_called_once()
                self.assertTrue((Path(d) / 'JPN_NY.GDP.MKTP.CD.csv').exists())
                self.assertEqual(list(df['date']), [2018, 2020])

    def test_sorted(self):
        with tempfile.TemporaryDirectory() as d:
            mock_resp = Mock()
            mock_resp.json.return_value = [None, SAMPLE_JSON]
            mock_resp.raise_for_status = lambda: None
            with patch('dashboard.requests.get', return_value=mock_resp):
                df = get_indicator_data('JPN', 'NY.GDP.MKTP.CD', cache_dir=Path(d))
                self.assertEqual(list(df['date']), sorted(df['date']))

    def test_dropna(self):
        with tempfile.TemporaryDirectory() as d:
            mock_resp = Mock()
            mock_resp.json.return_value = [None, SAMPLE_JSON]
            mock_resp.raise_for_status = lambda: None
            with patch('dashboard.requests.get', return_value=mock_resp):
                df = get_indicator_data('JPN', 'NY.GDP.MKTP.CD', cache_dir=Path(d))
                self.assertFalse(df['value'].isna().any())

if __name__ == '__main__':
    unittest.main(verbosity=2)
