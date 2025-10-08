import unittest
import pandas as pd
from data_analysis import (
    load_and_clean_data,
    compute_avg_macros,
    top_protein_recipes,
    highest_protein_diet,
    most_common_cuisine,
    add_ratio_columns,
)

class TestDataAnalysis(unittest.TestCase):

    def setUp(self):
        # Create a small mock dataset
        self.df = pd.DataFrame({
            'Diet_type': ['Keto', 'Keto', 'Vegan', 'Vegan', 'Paleo'],
            'Protein(g)': [30, 40, 10, 15, 25],
            'Carbs(g)': [10, 15, 50, 60, 20],
            'Fat(g)': [20, 25, 10, 15, 30],
            'Cuisine_type': ['American', 'Mexican', 'Indian', 'Indian', 'Thai'],
            'Recipe_name': ['A', 'B', 'C', 'D', 'E']
        })

    def test_compute_avg_macros(self):
        avg = compute_avg_macros(self.df)
        self.assertIn('Protein(g)', avg.columns)
        self.assertEqual(len(avg), 3)

    def test_top_protein_recipes(self):
        top = top_protein_recipes(self.df)
        self.assertTrue('Protein(g)' in top.columns)
        self.assertTrue(all(top['Protein(g)'].values >= 10))

    def test_highest_protein_diet(self):
        avg = compute_avg_macros(self.df)
        diet = highest_protein_diet(avg)
        self.assertIn(diet, ['Keto', 'Vegan', 'Paleo'])

    def test_most_common_cuisine(self):
        cuisine = most_common_cuisine(self.df)
        self.assertTrue(isinstance(cuisine, pd.Series))

    def test_add_ratio_columns(self):
        df_with_ratios = add_ratio_columns(self.df.copy())
        self.assertIn('Protein_to_Carbs_ratio', df_with_ratios.columns)
        self.assertFalse(df_with_ratios['Protein_to_Carbs_ratio'].isnull().any())

if __name__ == '__main__':
    unittest.main()

