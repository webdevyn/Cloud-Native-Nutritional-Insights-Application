import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import io
import os
import json
from process_diets import download_csv_to_df, compute_avg_macros, save_results_json

class TestProcessDiets(unittest.TestCase):

    def setUp(self):
        # Small in-memory CSV to simulate download
        self.csv_content = b"""Diet_type,Protein(g),Carbs(g),Fat(g),Recipe_name
Keto,30,10,20,A
Keto,40,15,25,B
Vegan,10,50,10,C
Vegan,15,60,15,D
Paleo,25,20,30,E
"""
        self.df = pd.read_csv(io.BytesIO(self.csv_content))

    @patch('process_diets.io')
    def test_download_csv_to_df(self, mock_io):
        # Mock the blob client download_blob().readall() to return our CSV bytes
        mock_blob = MagicMock()
        mock_blob.download_blob().readall.return_value = self.csv_content

        df = download_csv_to_df(mock_blob)
        self.assertEqual(len(df), 5)
        self.assertIn('Protein(g)', df.columns)

    def test_compute_avg_macros(self):
        avg = compute_avg_macros(self.df)
        self.assertIn('Protein(g)', avg.columns)
        self.assertEqual(len(avg), 3)  # 3 diet types

    def test_save_results_json_creates_file(self):
        avg = compute_avg_macros(self.df)
        output_dir = 'test_simulated_nosql'
        save_results_json(avg, output_dir=output_dir)
        filepath = os.path.join(output_dir, 'results.json')
        self.assertTrue(os.path.exists(filepath))
        # Clean up
        os.remove(filepath)
        os.rmdir(output_dir)

if __name__ == '__main__':
    unittest.main()
