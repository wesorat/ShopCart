from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'country', 'city', 'zip_code')
    empty_value_display = "-empty-"
    list_filter = ('user', 'country', 'city')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['price', 'product', "quantity", "user"]
        return super().get_readonly_fields(request, obj)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'shipping_address', 'amount',
                    'created', 'updated', 'paid', 'discount',
]
    list_filter = ['paid', 'updated', 'created',]
    inlines = [OrderItemInline]
    list_per_page = 15
    list_display_links = ['id', 'user']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress, ShippingAddressAdmin)

