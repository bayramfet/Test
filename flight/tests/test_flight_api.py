from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from datetime import datetime, date

from flight.views import FlightView
from flight.models import Flight


class FlightViewTestCase(APITestCase):

    def create_flight(self):
        now = datetime.now()
        curren_time = now.strftime('%H:%M:%S')
        today = date.today()
        flight = Flight.objects.create(
            flight_number='456dfg',
            operation_airlines='THY',
            departure_city='İstanbul',
            arrival_city='London',
            date_of_departure=f'{today}',
            estimated_time_departure=f'{curren_time}'
        )
        return flight

    def setUp(self):
        self.factory = APIRequestFactory()
        self.flight = self.create_flight()
        self.user = User.objects.create_user(
            username='admin', email='a@a.com', password='Aa654321*'
        )
        self.token = Token.objects.create(user=self.user)

    def test_flight_list_as_non_authenticate_user(self):
        request = self.factory.get('/flight/flights/')
        response = FlightView.as_view({'get': 'list'})(request)
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, 'reservation')
        self.assertEquals(response.data, [])

    def test_flight_list_as_staff_user(self):
        request = self.factory.get(
            '/flight/flights/', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        self.user.is_staff = True
        self.user.save(),
        # Eğer token kullanmadan test ortamında authenticate olarak simule etmek istersek
        # force_authenticate(request, user=self.user)
        request.user = self.user
        response = FlightView.as_view({'get': 'list'})(request)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'reservation')
        self.assertTrue(len(response.data) > 0)

    def test_flight_create_as_non_authenticated_user(self):
        request = self.factory.post('/flight/flights/')
        response = FlightView.as_view({'post': 'create'})(request)
        self.assertEquals(response.status_code, 401)

    def test_flight_create_as_authenticated_user(self):
        request = self.factory.post(
            '/flight/flights/', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        resonse = FlightView.as_view({'post': 'create'})(request)
        self.assertEquals(resonse.status_code, 403)

    def test_flight_cerate_as_staff_user(self):
        data = {
            "flight_number": "456df456",
            "operation_airlines": "THY",
            "departure_city": "Istanbul",
            "arrival_city": "Berlin",
            "date_of_departure": "2023-01-07",
            "estimated_time_departure": "09:16:47"
        }

        self.user.is_staff = True
        self.user.save()
        request = self.factory.post(
            '/flight/flights/', data, HTTP_AUTHORIZATION='Token {}'.format(self.token))
        response = FlightView.as_view({'post': 'create'})(request)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Flight.objects.count(), 2)

    def test_flight_update_as_staff_user(self):
        data = {
            "flight_number": "456df456",
            "operation_airlines": "THY",
            "departure_city": "Istanbul",
            "arrival_city": "London",
            "date_of_departure": "2023-01-07",
            "estimated_time_departure": "09:16:47"
        }
        self.user.is_staff = True
        self.user.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {}'.format(self.token))
        response = self.client.put('/flight/flights/1/', data)
        print(response.data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['flight_number'], '456df456')

    def test_flight_delete_as_staff_user(self):
        self.user.is_staff = True
        self.user.save()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {}'.format(self.token))
        response = self.client.delete('/flight/flights/1/')
        self.assertEquals(response.status_code, 204)
        self.assertEquals(Flight.objects.count(), 0)

    def test_flight_model_str_method(self):
        self.assertEquals(str(
            self.flight), f'{self.flight.flight_number} - {self.flight.departure_city} - {self.flight.arrival_city}')