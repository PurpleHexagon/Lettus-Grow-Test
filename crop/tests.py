
import json

from django.test import TestCase, Client

# pylint: disable=all


class CropTests(TestCase):

    fields = {'name', 'family'}

    def test_get(self):
        cli = Client()
        response = cli.get('/api/crop/')
        data = json.loads(response.content.decode())
        self.assertGreater(len(data), 1)
        for crop in data:
            self.assertEqual(set(crop.keys()), self.fields)

    def test_post(self):
        cli = Client()
        data = {
            'name': 'soft',
            'family': 'Mint'
        }
        response = cli.post('/api/crop/', data, content_type="application/json")
        crop = json.loads(response.content.decode())
        for key in self.fields:
            self.assertEqual(data[key], crop[key])


class TrayTests(TestCase):

    fields = {'crop_id', 'growth_plan_id', 'sow_date', 'harvest_date', 'total_yield'}

    def test_get(self):
        cli = Client()
        response = cli.get('/api/tray/')
        data = json.loads(response.content.decode())
        self.assertGreater(len(data), 1)
        for tray in data:
            self.assertEqual(set(tray.keys()), self.fields)

    def test_post(self):
        cli = Client()
        data = {
            'crop_id': 1,
            'growth_plan_id': 1,
            'sow_date': '2020-01-09 12:12:12+00:00'
        }
        response = cli.post('/api/tray/', data, content_type="application/json")
        tray = json.loads(response.content.decode())

        for key in self.fields:
            if key in data:
                self.assertEqual(data[key], tray[key])


class GrowthPlansTests(TestCase):

    fields = {'name', 'crop_id', 'growth_duration', 'est_yield'}

    def test_get(self):
        cli = Client()
        response = cli.get('/api/growthplan/')
        data = json.loads(response.content.decode())
        self.assertGreater(len(data), 1)
        for growth_plan in data:
            self.assertEqual(set(growth_plan.keys()), self.fields)

    def test_post(self):
            cli = Client()
            data = {
                'name': 'test_post Growth Plan',
                'crop_id': 1,
                'growth_duration': 20,
                'est_yield': 200,
            }
            response = cli.post('/api/growthplan/', data, content_type="application/json")
            growth_plan = json.loads(response.content.decode())
            for key in self.fields:
                self.assertEqual(data[key], growth_plan[key])