from django.db import models
from users.models import Resident
from django.db import transaction

class Invoice(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT, related_name='invoices')  # Foreign key to Resident with related name
    invoice_no = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Example field for invoice amount
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the invoice was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the invoice was last updated
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete field
    status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])  # Status of the invoice

    def mark_as_paid(self):
        with transaction.atomic():
            # Step 1: Mark the invoice as paid
            self.status = 'paid'
            self.save()

            # Step 2: Create a PaidHistory entry
            PaidHistory.objects.create(resident=self.resident, invoice=self)

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            #count the current number of invoices for the resident
            count = Invoice.objects.filter(resident=self.resident).count()
            self.invoice_no = f"R{self.resident.id}_{count}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice #{self.id} for Resident {self.resident.id} - Amount: {self.amount}"

#history is the paid invoices
class PaidHistory(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='paid_history')
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History #{self.id} for Resident {self.invoice.resident} - Amount: {self.invoice.amount}"

class Card(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT, related_name='card')
    card_no = models.CharField(max_length=20, unique=True)
    card_type = models.CharField(max_length=20, choices=[('visa', 'Visa'), ('mastercard', 'Mastercard')])
    card_expiry = models.DateField()
    card_cvv = models.CharField(max_length=4)
    card_name = models.CharField(max_length=100)
    card_status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    card_created_at = models.DateTimeField(auto_now_add=True)
    card_updated_at = models.DateTimeField(auto_now=True)
    card_deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Card #{self.id} for Resident {self.resident.id} - Card Type: {self.card_type}"
    
    