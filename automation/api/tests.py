from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

from django.test import TestCase
from .models import Calendarlist


# Create your tests here.
class ModelTestCase(TestCase):
    """This class defines the test suite for the calendarlist model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.calendarlist_name = "Write world class code"
        self.calendarlist = Bucketlist(name=self.calendarlist_name)

    def test_model_can_create_a_calendarlist(self):
        """Test the calendarlist model can create a calendarlist."""
        old_count = Calendarlist.objects.count()
        self.calendarlist.save()
        new_count = Calendarlist.objects.count()
        self.assertNotEqual(old_count, new_count)
		
	def test_api_can_get_a_calendarlist(self):
        """Test the api can get a given bucketlist."""
        calendarlist = Calendarlist.objects.get()
        response = self.client.get(
            reverse('details',
            kwargs={'pk': calendarlist.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, calendarlist)
		

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
	
	 def __str__(self):
		"""Return a human readable representation of the model instance."""
		return "{}".format(self.name)
		

# Define this after the ModelTestCase
class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.calendarlist_data = {'name': 'Go to Ibiza'}
        self.response = self.client.post(
            reverse('create'),
            self.calendarlist_data,
            format="json")

    def test_api_can_create_a_calendarlist(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)