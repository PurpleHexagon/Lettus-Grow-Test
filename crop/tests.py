
import json

from django.test import TestCase, Client

# pylint: disable=all


class CropTests(TestCase):

    fields = {'name', 'family'}

    def test_get(self):
        cli = Client()
        responce = cli.get('/api/crop/')
        data = json.loads(responce.content.decode())
        self.assertGreater(len(data), 1)
        for crop in data:
            self.assertEqual(set(crop.keys()), self.fields)

    def test_post(self):
        cli = Client()
        data = {
            'name': 'soft',
            'family': 'Mint'
        }
        responce = cli.post('/api/crop/', data, content_type="application/json")
        crop = json.loads(responce.content.decode())
        for key in self.fields:
            self.assertEqual(data[key], crop[key])


class TrayTests(TestCase):

    fields = {'crop_id', 'growth_plan_id', 'sow_date', 'harvest_date', 'total_yield'}

    def test_get(self):
        cli = Client()
        responce = cli.get('/api/tray/')
        data = json.loads(responce.content.decode())
        self.assertGreater(len(data), 1)
        for tray in data:
            self.assertEqual(set(tray.keys()), self.fields)

    def test_post(self):
        cli = Client()
        data = {
            'crop_id': 1,
            'growth_plan_id': 1,
            'sow_date': '2020-1-9T12:12:12'
        }
        responce = cli.post('/api/tray/', data, content_type="application/json")
        tray = json.loads(responce.content.decode())
        for key in self.fields:
            if key in data:
                self.assertEqual(data[key], tray[key])


