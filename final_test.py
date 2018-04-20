# final_test.py
from final import *
from forflask import *
import unittest

class TestYelpResturant(unittest.TestCase):

	def res_is_in_res_list(self, res_name, res_list):
		for r in res_list:
			if res_name == r.name:
				return True
		return False

	def test_resturant_search(self):

		resturants = get_yelp_resturant()

		self.assertTrue(self.res_is_in_res_list('SWeL', resturants))
		self.assertTrue(self.res_is_in_res_list('The Pink Door', resturants))
		self.assertTrue(self.res_is_in_res_list('Radiator Whiskey', resturants))
		self.assertTrue(self.res_is_in_res_list('List', resturants))

class TestYelpEvent(unittest.TestCase):

	def event_is_in_event_list(self, eve_name, eve_list):
		for e in eve_list:
			if eve_name == e.name:
				return True
		return False

	def test_event_search(self):

		events = get_yelp_event()

		self.assertTrue(self.event_is_in_event_list('9th Annual Pike Place Market Flower Festival', events))
		self.assertTrue(self.event_is_in_event_list('Metamorphosis... by Emerald City Music', events))
		self.assertTrue(self.event_is_in_event_list('2018 International Bubble Flashmob', events))
		self.assertTrue(self.event_is_in_event_list('Flashmob Water Gun Fight', events))

class TestTripAdvisor(unittest.TestCase):

	def tres_is_in_tres_list(self, tres_name, tres_list):
		for t in tres_list:
			if tres_name == t.name:
				return True
		return False

	def test_tres_search(self):

		tres = get_ta_resturant()

		self.assertTrue(self.tres_is_in_tres_list('Chan', tres))
		self.assertTrue(self.tres_is_in_tres_list('Altura Restaurant', tres))
		self.assertTrue(self.tres_is_in_tres_list('The Pink Door', tres))
		self.assertTrue(self.tres_is_in_tres_list("Shiro's", tres))



class TestPlotly(unittest.TestCase):

	def test_show_plotly(self):
		try:
			plot_yelp_resturant()
			plot_yelp_event()
		except:
			self.fail()

class TestFlask(unittest.TestCase):
	
	def setUp(self):
		# creates a test client
		self.app = app.test_client()
		# propagate the exceptions to the test client
		self.app.testing = True 


	def test_home_status_code(self):
		# sends HTTP GET request to the application
		# on the specified path
		result = self.app.get('/') 

		# assert the status code of the response
		self.assertEqual(result.status_code, 200) 


if __name__ == '__main__':
	unittest.main()