from django.contrib import admin
from .models import Category, Transaction, Balance


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category_name', 'total')


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'amount_of_transaction', 'time_of_transaction', 'date_of_transaction',
        'category', 'organisation', 'comment'
    )


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Balance, BalanceAdmin)
