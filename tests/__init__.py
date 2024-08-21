from wiki import fetchPage, BeautifulSoup
from wiki.export_functions import exportToCsv, exportToJson
from wiki.utils import create_data_folder, uuid_to_str, clean_numeric
from database.operations import check_tables_exist, insert_records
from database.schema import AcademyAwardWinningFilms, TestTable
from scripts.wikipedia_uuid import scrape_oscar_winning_films
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class WikiFilmDataTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'test_results')
        os.makedirs(self.output_dir, exist_ok=True)
        self.output_file = open(os.path.join(self.output_dir, 'test_results.txt'), 'w')

    def addSuccess(self, test):
        super().addSuccess(test)
        self.output_file.write(f"PASS: {test}\n")

    def addError(self, test, err):
        super().addError(test, err)
        self.output_file.write(f"ERROR: {test}\n{err}\n")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.output_file.write(f"FAIL: {test}\n{err}\n")

    def close(self):
        self.output_file.close()

class TestWikiFunctions(unittest.TestCase):
    def test_fetchPage(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            response = fetchPage('https://google.com')
            self.assertEqual(response.status_code, 200)

    def test_fetchPage_exception(self):
        with patch('requests.get', side_effect=Exception('Network error')):
            with self.assertRaises(Exception):
                fetchPage('https://google.com')

class TestExportFunctions(unittest.TestCase):
    @patch('pandas.DataFrame.to_csv')
    def test_exportToCsv(self, mock_to_csv):
        # Create a sample DataFrame
        data = {'id': ['test-id'], 'name': ['Test Movie'], 'year': [2023], 'awards': [1], 'nominations': [3]}
        df = pd.DataFrame(data)
        
        # Call the export function
        exportToCsv(df, 'test.csv')
        
        # Assert that to_csv was called once with the correct arguments
        mock_to_csv.assert_called_once_with('test.csv', index=False)

    @patch('json.dump')
    def test_exportToJson(self, mock_json_dump):
        df = MagicMock()
        df.to_dict.return_value = [{'id': 'test-id', 'name': 'Test Movie'}]
        exportToJson(df, 'test.json')
        mock_json_dump.assert_called_once()

class TestUtils(unittest.TestCase):
    @patch('os.makedirs')
    def test_create_data_folder(self, mock_makedirs):
        create_data_folder('test_results/test.csv')
        mock_makedirs.assert_called_once_with('test_results')

    def test_uuid_to_str(self):
        import uuid
        test_uuid = uuid.uuid4()
        self.assertEqual(uuid_to_str(test_uuid), str(test_uuid))
        self.assertEqual(uuid_to_str('not-a-uuid'), 'not-a-uuid')

    def test_clean_numeric(self):
        self.assertEqual(clean_numeric('123'), 123)
        self.assertEqual(clean_numeric('123.45'), 123)
        self.assertEqual(clean_numeric('abc'), 'abc')

class TestDatabaseOperations(unittest.TestCase):
    @patch('sqlalchemy.inspect')
    def test_check_tables_exist(self, mock_inspect):
        mock_inspect.return_value.get_table_names.return_value = ['academy_award_winning_films', 'TestTable']
        self.assertTrue(check_tables_exist())

    @patch('sqlalchemy.orm.Session')
    def test_insert_records(self, mock_session):
        records = [MagicMock(), MagicMock()]
        insert_records(mock_session, records)
        mock_session.add_all.assert_called_once_with(records)
        mock_session.commit.assert_called_once()

class TestDatabaseSchema(unittest.TestCase):
    def test_AcademyAwardWinningFilms(self):
        film = AcademyAwardWinningFilms('test-id', 'Test Film', 2020, 1, 5)
        self.assertEqual(film.id, 'test-id')
        self.assertEqual(film.film, 'Test Film')
        self.assertEqual(film.year, 2020)
        self.assertEqual(film.awards, 1)
        self.assertEqual(film.nominations, 5)

    def test_TestTable(self):
        test_entry = TestTable('test-id', 'Test Entry')
        self.assertEqual(test_entry.id, 'test-id')
        self.assertEqual(test_entry.text, 'Test Entry')

class TestWikipediaUUID(unittest.TestCase):
    @patch('wiki.fetchPage')
    @patch('bs4.BeautifulSoup')
    def test_scrape_oscar_winning_films(self, mock_bs, mock_fetchPage):
        mock_response = MagicMock()
        mock_fetchPage.return_value = mock_response
        mock_soup = MagicMock()
        mock_bs.return_value = mock_soup

        mock_tr = MagicMock()
        mock_tr.find_all.return_value = [MagicMock(text='Film'), MagicMock(text='2020'), MagicMock(text='1'), MagicMock(text='5')]
        mock_soup.find.return_value.find.return_value.find_all.return_value = [mock_tr]

        results = scrape_oscar_winning_films()
        self.assertEqual(len(results), 1373)
        self.assertEqual(len(results[0]), 5)  # id, film, year, awards, nominations

if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(resultclass=WikiFilmDataTestResult))