from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import AdminLoginForm, PartnerForm
from django.contrib.auth.decorators import login_required
from .models import Partner
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid login credentials')
    else:
        form = AdminLoginForm()
    return render(request, 'admin_login.html', {'form': form})


@login_required()
def dashboard(request):
    total_partners = Partner.objects.count()
    recent_partners = Partner.objects.order_by('-created_at')[:5]
    return render(request, 'dashboard.html', {'total_partners': total_partners, 'recent_partners': recent_partners})

@login_required
def partner_list(request):
    partners = Partner.objects.all()
    query = request.GET.get('q')
    if query:
        partners = partners.filter(name__icontains=query)
    return render(request, 'partner_list.html', {'partners': partners})

@login_required
def add_partner(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile_no = request.POST['mobile_no']
        address = request.POST['address']
        partner = Partner.objects.filter(email=email)
        if partner is None:
            partner = Partner.objects.create(name=name, email=email, mobile_no=mobile_no, address=address)
            partner.save()
            return redirect('partner_list')
        else:
            messages.error(request, 'Partner already exist.')
            return redirect('add_partner')
    return render(request, 'add_partner.html')

@login_required
def partner_detail(request, pk):
    partner = Partner.objects.get(pk=pk)
    return render(request, 'partner_details.html', {'partner': partner})

@login_required
def edit_partner(request, pk):
    partner = Partner.objects.get(pk=pk)
    if request.method == 'POST':
        form = PartnerForm(request.POST, instance=partner)
        if form.is_valid():
            form.save()
            return redirect('partner_detail', pk=partner.pk)
    else:
        form = PartnerForm(instance=partner)
    return render(request, 'edit_partner.html', {'form': form, 'partner': partner})

@login_required
def Logout(request):
    logout(request)
    return redirect('dashboard')