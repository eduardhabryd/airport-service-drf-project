from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
	"""Define a model manager for User model with no username field."""
	
	use_in_migrations = True
	
	def _create_user(self, email, password, **extra_fields):
		"""Create and save a User with the given email and password."""
		if not email:
			raise ValueError("The given email must be set")
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_user(self, email, password=None, **extra_fields):
		"""Create and save a regular User with the given email and password."""
		extra_fields.setdefault("is_staff", False)
		extra_fields.setdefault("is_superuser", False)
		return self._create_user(email, password, **extra_fields)
	
	def create_superuser(self, email, password, **extra_fields):
		"""Create and save a SuperUser with the given email and password."""
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)
		
		if extra_fields.get("is_staff") is not True:
			raise ValueError("Superuser must have is_staff=True.")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must have is_superuser=True.")
		
		return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
	username = None
	email = models.EmailField(_("email address"), unique=True)
	
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = []
	
	objects = UserManager()


class Airport(models.Model):
	name = models.CharField()
	closest_big_city = models.CharField()


class Route(models.Model):
	source = models.ForeignKey(Airport, related_name="routes", on_delete=models.CASCADE)
	destination = models.ForeignKey(Airport, related_name="routes", on_delete=models.CASCADE)
	distance = models.IntegerField()


class AirplaneType(models.Model):
	name = models.CharField()


class Airplane(models.Model):
	name = models.CharField()
	rows = models.IntegerField()
	seats_in_row = models.IntegerField()
	airplane_type = models.ForeignKey(AirplaneType, related_name="airplanes", on_delete=models.CASCADE)


class Crew(models.Model):
	first_name = models.CharField()
	last_name = models.CharField()


class Flight(models.Model):
	route = models.ForeignKey(Route, related_name="flights", on_delete=models.CASCADE)
	airplane = models.ForeignKey(Airplane, related_name="flights", on_delete=models.CASCADE)
	departure_time = models.DateTimeField()
	arrival_time = models.DateTimeField()


class Order(models.Model):
	created_at = models.DateTimeField()
	user = models.ForeignKey(get_user_model(), related_name="orders", on_delete=models.CASCADE)


class Ticket(models.Model):
	row = models.IntegerField()
	seat = models.IntegerField()
	flight = models.ForeignKey(Flight, related_name="tickets", on_delete=models.CASCADE)
	order = models.ForeignKey(Order, related_name="tickets", on_delete=models.CASCADE)
