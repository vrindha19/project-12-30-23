from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from .forms import ProductQuantityForm
from django.shortcuts import render, get_object_or_404
from .models import Product 

def fruits(request, data):
    return render(request,'fruits.product.html')
def home(request, data=None):
    return render(request,'index.html')
def vegitables(request, data):
    return render(request,'vegitables.html')
def contact(request):
    return render(request,'contact.html')
def add_product(request):
    return render(request,'add_product.html')
def forgot_password(request):
    return render(request,'forgot_password.html')
def about(request):
    return render(request,'about.html')
def orderpage(request):
    return render(request,'orderpage.html')
def logout(request):
    return render(request,'logout.html')
def logout_action(request):
    return render(request,'logout-action.html')
def orderpage(request):
    return render(request,'orderpage.html')
def payment(request):
    return render(request,'view_payment.html')

def shopping_cart(request):
    return render(request,'shopping cart.html')
def register(request):
    return render(request,'register.html')
def login(request):
    return render(request,'login.html')
def allproduct(request):
    return render(request,'all product.html')


def product_view(request):
    form = ProductQuantityForm()
    
    context = {
        'form': form,
        # Add other context variables as needed
    }
    
    return render(request, 'product.html', context)



class ProductView(View):
	def get(self, request):
		totalitem = 0
		Fruits = Product.objects.filter(category='F')
		vegitables = Product.objects.filter(category='V')
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		return render(request, 'index.html',
				 { 'Fruits':Fruits, 'vegitables':vegitables, 'totalitem':totalitem})

class ProductDetailView(View):
	def get(self, request, pk):
		totalitem = 0
		product = Product.objects.first() 
		print(product.id)
		item_already_in_cart=False
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
			item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
		return render(request, 'productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})
######
#############PRODUCT DETALIS#############
# def productdetail(request):

# 	return render(request,'productdetail.html')
		
# @login_required()
# def add_to_cart(request):
#     user = request.user
#     product_id = request.GET.get('prod_id')
    
#     try:
#         product = get_object_or_404(Product, id=product_id)
        
#         item_already_in_cart = Cart.objects.filter(Q(product=product) & Q(user=user)).exists()
        
#         if not item_already_in_cart:
#             Cart(user=user, product=product).save()
#             messages.success(request, 'Product Added to Cart Successfully!')
#         else:
#             messages.info(request, 'Product is already in the cart.')
            
#     except Product.DoesNotExist:
#         messages.error(request, 'Product does not exist!')
#         return render(request, 'addtocart.html')  # Rendering the template here since product doesn't exist
    
#     return redirect('cart')
  # Below Code is used to return to same page
  # return redirect(request.META['HTTP_REFERER'])

@login_required
def show_cart(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0.0
		shipping_amount = 70.0
		totalamount=0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		print(cart_product)
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity * p.product.discounted_price)
				amount += tempamount
			totalamount = amount+shipping_amount
			return render(request, 'addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem})
		else:
			return render(request, 'emptycart.html', {'totalitem':totalitem})
	else:
		return render(request, 'emptycart.html', {'totalitem':totalitem})

def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

@login_required
def checkout(request):
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_items = Cart.objects.filter(user=request.user)
	amount = 0.0
	shipping_amount = 70.0
	totalamount=0.0
	cart_product = [p for p in Cart.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		totalamount = amount+shipping_amount
	return render(request, 'checkout.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount})

@login_required
def payment_done(request):
	custid = request.GET.get('custid')
	print("Customer ID", custid)
	user = request.user
	cartid = Cart.objects.filter(user = user)
	customer = Customer.objects.get(id=custid)
	print(customer)
	for cid in cartid:
		OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
		print("Order Saved")
		cid.delete()
		print("Cart Item Deleted")
	return redirect("orders")

def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

@login_required
def address(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	add = Customer.objects.filter(user=request.user)
	return render(request, 'address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})

@login_required
def orders(request):
	op = OrderPlaced.objects.filter(user=request.user)
	return render(request, 'orders.html', {'order_placed':op})





class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'register.html', {'form':form})
  
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully.')
   form.save()
  return render(request, 'register.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm()
		return render(request, 'profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
		
	def post(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name  = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated Successfully.')
		return render(request, 'profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})

from django.shortcuts import render

from django.shortcuts import render, get_object_or_404

def product_detail(request, product_slug):
    # Define product data in a list of dictionaries or a database model
    products = {
        'capsicum': {'id': 1, 'title': 'Capsicum', 'selling_price': 15, 'product_image': 'productimg/product-1.jpg'},
        'tomato': {'id': 2, 'title': 'Tomato', 'selling_price': 30, 'product_image': 'productimg/product-5.jpg'},
        'apple': {'id': 3, 'title': 'Apple', 'selling_price': 25, 'product_image': 'productimg/product_01.jpg'},
        'orange': {'id': 4, 'title': 'Orange', 'selling_price': 45, 'product_image': 'productimg/orange.jpg'},
    }
    
    # Try to fetch the product using the product_slug
    product = products.get(product_slug)
    
    # If product doesn't exist, return a 404 page
    if not product:
        return render(request, '404.html')
    
    # Create a context dictionary to pass to the template
    context = {
        'product': product,
    }
    
    return render(request, 'productdetail.html', context)


    return render(request, 'productdetail.html', {'product': product, 'product_image': product_image})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages



####CART VIEWS###########
@login_required
# def addcart(request, product_id):
#     user = request.user
#     product = get_object_or_404(Product, id=product_id)
    
#     # Get or create the cart for the user
#     cart, created = Cart.objects.get_or_create(user=user)
    
#     # Create or get the cart item for the product
#     cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
#     if not cart_item_created:
#         cart_item.quantity += 1
#         cart_item.save()
#         messages.success(request, 'Quantity updated in your cart.')
#     else:
#         messages.success(request, 'Product added to cart.')
    
#     return redirect('cart:cart_detail') 





# Assuming Product model is imported correctly

def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    
    # Assuming quantity is sent via POST request, adjust as needed
    if request.method == 'POST':
        quantity = request.POST.get('quantity')  # Adjust 'quantity' based on your form field name
    else:
        quantity = None  # Handle accordingly if quantity is not provided
    
    context = {
        'product': product,
        'user': user,
        'quantity': quantity,
        # ... any other data you want to pass to the template
    }
    
    return render(request, 'addtocart.html', context)

 

