"""Forms for Inventory app."""
from django import forms
from .models import Product, StockTransaction, Category


class CategoryForm(forms.ModelForm):
    """Category creation/edit form."""
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description'
            }),
        }


class ProductForm(forms.ModelForm):
    """Product creation/edit form."""
    class Meta:
        model = Product
        fields = [
            'sku', 'name', 'description', 'category', 'unit',
            'minimum_stock', 'reorder_quantity', 'price', 'image', 'is_active'
        ]
        widgets = {
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SKU/Product Code (e.g., PROD-001)'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Product description'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'minimum_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '0',
                'placeholder': 'Minimum stock level for alerts'
            }),
            'reorder_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '0',
                'placeholder': 'Suggested reorder quantity'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '0',
                'step': '0.01',
                'placeholder': 'Unit price'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StockTransactionForm(forms.ModelForm):
    """Stock transaction form."""
    class Meta:
        model = StockTransaction
        fields = ['product', 'transaction_type', 'quantity', 'reason', 'reference_no', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '1',
                'placeholder': 'Enter quantity'
            }),
            'reason': forms.Select(attrs={'class': 'form-select'}),
            'reference_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Invoice/PO number (optional)'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes (optional)'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        
        if quantity and quantity <= 0:
            self.add_error('quantity', 'Quantity must be greater than 0.')
        
        return cleaned_data


class ProductFilterForm(forms.Form):
    """Filter products form."""
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="All Categories"
    )
    status = forms.ChoiceField(
        choices=[
            ('', 'All Stock Status'),
            ('in_stock', 'In Stock'),
            ('low_stock', 'Low Stock'),
            ('out_of_stock', 'Out of Stock'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name or SKU...'
        })
    )


class TransactionFilterForm(forms.Form):
    """Filter transactions form."""
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="All Products"
    )
    transaction_type = forms.ChoiceField(
        choices=[('', 'All Types'), ('IN', 'Stock In'), ('OUT', 'Stock Out')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
