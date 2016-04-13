"""Models for the ``booking`` app."""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

#from calendarium.models import Event
from taggit.managers import TaggableManager
#from hvad.models import TranslatableModel, TranslatedFields
#from international.models import countries




class Booking(models.Model):
    """
    Model to contain information about a booking.

    Note, that on the model itself, most of the attributes are blank=True.
    We need this behaviour to be able to create empty temporary bookings.
    You will have to take care of the field being required or not in a
    ModelForm yourself.

    :user (optional): Connection to Django's User model.
    :session (optional): Stored session to identify anonymous users.
    :member (optional): Connection to Entities' Member model.
    :camp_request (optional): A special request of the customer.
    :arrival (optional): From when the booking is active.
    :departure (optional): Until when the booking is active.
    :creation_date: Date of the booking creation.
    :edited_date: Date of the booking being edited.
    :booking_id (optional): Custom unique booking identifier.
    :tags: Current status of the booking.
    :notes (optional): Staff notes.

    """
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        related_name='bookings',
        blank=True, null=True,
    )

    session = models.ForeignKey(
        'sessions.Session',
        verbose_name=_('Session'),
        blank=True, null=True,
    )

    member = models.ForeignKey(
        'entities.Member',
        verbose_name=_('Member'),
        related_name='members',
        blank=True, null=True,
        on_delete=models.CASCADE,
        )


    camp_request = models.ForeignKey(
        'entities.Camp',
        verbose_name=_('Camp request'),
        blank=True,
        related_name='CampRequest',
        null=True,
    )

    arrival = models.DateField(
        verbose_name=_('From'),
        blank=True, null=True,
    )

    departure = models.DateField(
        verbose_name=_('Until'),
        blank=True, null=True,
    )

    creation_date = models.DateTimeField(
        verbose_name=_('Creation date'),
        auto_now_add=True,
    )
    
    edited_date = models.DateTimeField(
            verbose_name='Edited Date',
            auto_now=True,
            )

    booking_id = models.CharField(
        max_length=100,
        verbose_name=_('Booking ID'),
        blank=True,
        unique=True,
    )

    tags = TaggableManager(blank=True)

    notes = models.TextField(
        max_length=1024,
        verbose_name=('Notes'),
        blank=True,
    )

    
    
    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return '#{} ({})'.format(self.booking_id or self.pk,
                                 self.creation_date)


class BookingError(models.Model):
    """
    Holds information about an error during a booking process.

    This can be particularly useful, when many of the processes are automated
    or reliant on a third party app or API. You then can store the returned
    values directly into this model and have easy access and reference to the
    actual booking.

    :booking: The booking during this error occurred.
    :message: The short error message, that you need to store.
    :details: A more in depth text about the error or any kind of additional
      information, e.g. a traceback.
    :date: The time and date this error occured.

    """
    booking = models.ForeignKey(
        Booking,
        verbose_name=_('Booking'),
    )
    message = models.CharField(
        verbose_name=_('Message'),
        max_length=1000,
        blank=True,
    )
    details = models.TextField(
        verbose_name=_('Details'),
        max_length=4000,
        blank=True,
    )

    date = models.DateTimeField(
        verbose_name=_('Date'),
        auto_now_add=True,
    )

    def __unicode__(self):
        return '[{0}] {1} - {2}'.format(self.date, self.booking.booking_id,
                                        self.message)


class BookingItem(models.Model):
    """
    Model to connect a booking with a related object.

    :quantity: Quantity of booked items.
    :persons (optional): Quantity of persons, who are involved in this booking.
    :subtotal (optional): Field for storing the price of each individual item.
    :booked_item: Connection to related booked item.
    :booking: Connection to related booking.

    properties:
    :price: Returns the full price for subtotal * quantity.

    """
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Quantity'),
    )

    persons = models.PositiveIntegerField(
        verbose_name=_('Persons'),
        blank=True, null=True,
    )

    subtotal = models.DecimalField(
        max_digits=36,
        decimal_places=2,
        verbose_name=_('Subtotal'),
        blank=True, null=True,
    )

    # GFK 'booked_item'
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    booked_item = GenericForeignKey('content_type', 'object_id')

    booking = models.ForeignKey(
        'Booking',
        verbose_name=_('Booking'),
    )

    class Meta:
        ordering = ['-booking__creation_date']

    def __unicode__(self):
        return '{} ({})'.format(self.booking, self.booked_item)

    @property
    def price(self):
        return self.quantity * self.subtotal


class ExtraPersonInfo(models.Model):
    """
    Model to add extra information of persons/guests to a booking.

    :forename: First name of the user.
    :surname: Last name of the user.
    :arrival: Arrival date of the guest.
    :booking: Connection to related booking.
    :message: An additional message regarding this person.

    """
    forename = models.CharField(
        verbose_name=_('First name'),
        max_length=20,
    )

    surname = models.CharField(
        verbose_name=_('Last name'),
        max_length=20,
    )

    arrival = models.DateTimeField(
        verbose_name=_('Arrival'),
        blank=True, null=True,
    )

    booking = models.ForeignKey(
        'Booking',
        verbose_name=_('Booking'),
    )

    message = models.TextField(
        max_length=1024,
        verbose_name=_('Message'),
        blank=True,
    )

    class Meta:
        ordering = ['-booking__creation_date']

    def __unicode__(self):
        return '{} {} ({})'.format(self.forename, self.surname, self.booking)
