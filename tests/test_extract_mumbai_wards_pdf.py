import os
import unittest

from backend.data.extract_mumbai_wards_pdf import scrape_mumbai_pdf
import pandas as pd

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestExtractMumbaiWardsPDF(unittest.TestCase):
    def test_extract_sample_2020_01_02(self):
        expected = (24, 8)
        expected_first = ['RC', '21197', '19981', '600', '586', pd.to_datetime('2021-01-01 00:00:00'), 'Mumbai', 'MH']
        expected_last = ['B', '2153', '1942', '144', '60', pd.to_datetime('2021-01-01 00:00:00'), 'Mumbai', 'MH']

        sample = os.path.join(THIS_DIR, 'samples/mumbai_dashboard_2020_01_02.pdf')
        result = scrape_mumbai_pdf(sample)
        result_first = result.iloc[0].values
        result_last = result.iloc[-1].values

        self.assertIsNotNone(result)

        self.assertEqual(expected, result.shape)

        self.assertCountEqual(result_first, expected_first)
        self.assertCountEqual(result_last, expected_last)

    def test_extract_sample_2020_01_04(self):
        expected = (24, 8)
        expected_first = ['RC', '21264', '20064', '601', '568', pd.to_datetime('2021-01-03 00:00:00'), 'Mumbai', 'MH']
        expected_last = ['B', '2158', '1949', '144', '58', pd.to_datetime('2021-01-03 00:00:00'), 'Mumbai', 'MH']

        sample = os.path.join(THIS_DIR, 'samples/mumbai_dashboard_2020_01_04.pdf')
        result = scrape_mumbai_pdf(sample)
        result_first = result.iloc[0].values
        result_last = result.iloc[-1].values

        self.assertIsNotNone(result)

        self.assertEqual(expected, result.shape)

        self.assertCountEqual(result_first, expected_first)
        self.assertCountEqual(result_last, expected_last)

    def test_extract_sample_2020_01_20(self):
        # alignment issues in this pdf
        expected = (24, 8)
        expected_first = ['RC', '21813', '20679', '615', '488', pd.to_datetime('2021-01-18 00:00:00'), 'Mumbai', 'MH']
        expected_last = ['B', '2195', '1995', '144', '49', pd.to_datetime('2021-01-18 00:00:00'), 'Mumbai', 'MH']
        sample = os.path.join(THIS_DIR, 'samples/mumbai_dashboard_2021_01_20.pdf')
        result = scrape_mumbai_pdf(sample)
        result_first = result.iloc[0].values
        result_last = result.iloc[-1].values

        self.assertIsNotNone(result)

        self.assertEqual(expected, result.shape)

        self.assertCountEqual(result_first, expected_first)
        self.assertCountEqual(result_last, expected_last)
