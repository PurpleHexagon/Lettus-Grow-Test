
import json

from django.test import TestCase, Client

# pylint: disable=all


class CropTests(TestCase):

    fields = {'id', 'name', 'family'}

    def test_get(self):
        cli = Client()
        response = cli.get('/api/crop/')
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(data), 1)

        for crop in data['results']:
            self.assertEqual(set(crop.keys()), self.fields)

    def test_post(self):
        cli = Client()
        data = {
            'name': 'soft',
            'family': 'Mint'
        }
        response = cli.post('/api/crop/', data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        crop = json.loads(response.content.decode())

        for key in self.fields:
            if key in data:
                self.assertEqual(data[key], crop[key])

    def test_post_fails_when_name_longer_than_100_chars(self):
        cli = Client()
        data = {
            'name': 'soft soft soft soft soft soft soft soft soft soft soft soft soft soft soft soft soft soft soft soft soft',
            'family': 'Mint'
        }
        response = cli.post('/api/crop/', data, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        decoded_content = json.loads(response.content.decode())
        self.assertEqual(decoded_content['status'], 'failed')


class TrayTests(TestCase):

    fields = {'id', 'crop', 'growth_plan', 'sow_date', 'harvest_date', 'total_yield'}

    def test_get(self):
        cli = Client()
        response = cli.get('/api/tray/')
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(data['results']), 1)
        for tray in data['results']:
            self.assertEqual(set(tray.keys()), self.fields)

    def test_post(self):
        cli = Client()
        data = {
            'crop': 1,
            'growth_plan': 1,
            'sow_date': '2020-01-09T12:12:12Z'
        }
        response = cli.post('/api/tray/', data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        tray = json.loads(response.content.decode())

        for key in self.fields:
            if key in data:
                self.assertEqual(data[key], tray[key])


class GrowthPlansTests(TestCase):

    fields = {'id', 'name', 'crop', 'growth_duration', 'est_yield'}

    def test_get(self):
        cli = Client()
        response = cli.get('/api/growthplan/')
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(data['results']), 1)
        for growth_plan in data['results']:
            self.assertEqual(set(growth_plan.keys()), self.fields)

    def test_post(self):
        cli = Client()
        data = {
            'name': 'test_post Growth Plan',
            'crop': 1,
            'growth_duration': 20,
            'est_yield': 200,
        }
        response = cli.post('/api/growthplan/', data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        growth_plan = json.loads(response.content.decode())
        for key in self.fields:
            if key in data:
                self.assertEqual(data[key], growth_plan[key])