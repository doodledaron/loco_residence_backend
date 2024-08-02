from django.db import models
from users.models import Resident

class Invoice(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT, related_name='invoices')  # Foreign key to Resident with related name
    invoice_no = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Example field for invoice amount
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the invoice was created
    status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])  # Status of the invoice

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            #count the current number of invoices for the resident
            count = Invoice.objects.filter(resident=self.resident).count()
            self.invoice_no = f"R{self.resident.id}_{count}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice #{self.id} for Resident {self.resident.id} - Amount: {self.amount}"

#history is the paid invoicesP
class PaidHistory:
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT, related_name='paid_history')
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='paid_history')
    paid_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"History #{self.id} for Resident {self.resident.id} - Amount: {self.amount}"

class Card:
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT, related_name='card')
    card_no = models.CharField(max_length=20, unique=True)
    card_type = models.CharField(max_length=20, choices=[('visa', 'Visa'), ('mastercard', 'Mastercard'), ('amex', 'Amex')])
    card_expiry = models.DateField()
    card_cvv = models.CharField(max_length=4)
    card_name = models.CharField(max_length=100)
    card_address = models.CharField(max_length=200)
    card_city = models.CharField(max_length=100)
    card_state = models.CharField(max_length=100)
    card_zip = models.CharField(max_length=10)
    card_country = models.CharField(max_length=100)
    card_phone = models.CharField(max_length=20)
    card_email = models.EmailField()
    card_dob = models.DateField()
    card_ssn = models.CharField(max_length=11)
    card_status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    card_created_at = models.DateTimeField(auto_now_add=True)
    card_updated_at = models.DateTimeField(auto_now=True)
    card_deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Card #{self.id} for Resident {self.resident.id} - Card Type: {self.card_type}"
    