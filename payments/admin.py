from django.contrib import admin
from django import forms
from .models import Payment
from accounts.models import User  # Import the User model

class PaymentAdminForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    # Customize the user field to show only students
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='student'),  # Filter users by 'student' role
        required=True
    )

class PaymentAdmin(admin.ModelAdmin):
    form = PaymentAdminForm  # Use the customized form
    
    list_display = ('payment_id', 'user', 'course', 'amount', 'payment_method', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'payment_method', 'created_at')
    search_fields = ('user__email', 'course__title', 'transaction_id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Payment Information", {
            "fields": ("user", "course", "amount", "payment_method", "transaction_id", "payment_status")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),  # Makes timestamps collapsible
        }),
    )

# Register the PaymentAdmin with the Payment model
admin.site.register(Payment, PaymentAdmin)

