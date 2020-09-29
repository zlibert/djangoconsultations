from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from datetime import datetime
from django.db import transaction, IntegrityError

from django.contrib.auth.models import User
from django.contrib import messages
from .models import Consultation, UploadedFile, Message
from .forms import ConsultationForm

from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['requesters', 'agents', 'supervisors'])
def index(request):
    # Show consultations created by authenticated requester or all of them for the agents and supervisors
    if request.user.groups.filter(name='requesters').exists():
        print(request.user.username)
        consultations = Consultation.objects.filter(requester_id=request.user.id)
    else:
        consultations = Consultation.objects.all()
    open_consultations = consultations.filter(status='Open')
    pending_consultations = consultations.filter(status='Pending')
    waiting_for_patient_consultations = consultations.filter(status='Waiting for Patient')
    waiting_for_payment_consultations = consultations.filter(status='Waiting for Payment')
    closed_consultations = consultations.filter(status='Closed')
    resolved_consultations = consultations.filter(status='Resolved')
    rejected_consultations = consultations.filter(status='Rejected')
    context = {'consultations' : consultations, 'open_consultations' : open_consultations,\
        'pending_consultations': pending_consultations,
        'waiting_for_patient_consultations': waiting_for_patient_consultations, 'waiting_for_payment_consultations': waiting_for_payment_consultations,\
        'closed_consultations' : closed_consultations, 'resolved_consultations' : resolved_consultations, 'rejected_consultations': rejected_consultations
    }

    return render(request, 'index.html', context)

@login_required(login_url='accounts:login')
def detail(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    if request.user.id==consultation.requester_id or request.user.groups.filter(name='supervisors').exists() or request.user.groups.filter(name='agents').exists():
        requester = get_object_or_404(User, id=consultation.requester_id)
        uploadedfiles = UploadedFile.objects.filter(consultation=consultation_id)
        chat = Message.objects.filter(consultation_id=consultation_id)

        context = {
            'consultation': consultation,
            'requester': requester,
            'uploadedfiles': uploadedfiles,
            'chat': chat
        }
        # if the authenticated user is a requester 
        if request.user.groups.filter(name='requesters').exists():
            context['UserIsStaff'] = False
        else: # if the authenticated user is a supervisor or agent
            if request.user.groups.filter(name='supervisors').exists() or request.user.groups.filter(name='agents').exists():
                context['UserIsStaff'] = True

        if request.method == 'POST':
            if request.POST.get("send-message") == "send":
                if request.POST.get("chat-message"): 
                    if  len(request.POST.get("chat-message"))>0:
                        newMessage= Message(consultation_id=consultation_id, sender_id=request.user.id, text=request.POST.get("chat-message"))
                        newMessage.save()
                        messages.success(request, "Message sent")
                else:
                    messages.error(request, "Chat Messages can't be empty")
                    
            else:
                if request.POST.get("assignConsultation"):
                    consultation.assigned_to = request.user
                    consultation.save()
                    messages.success(request, "Consultation is assigned to you. Please make sure to respond within 48 Hours")
                if request.POST.get("price") and consultation.price != int(request.POST.get("price")) and int(request.POST.get("price"))>=0:
                    consultation.price = int(request.POST.get("price"))
                    consultation.save()
                    messages.success(request, "Price was set. Send the payment information to the \
                        user, when payment is confirmed, add this to payment information and save it")
                if  request.POST.get("paymentInfo") and consultation.paymentinfo!=request.POST.get("paymentInfo"):
                    consultation.paymentinfo = request.POST.get("paymentInfo")
                    consultation.save()
                    messages.success(request, "Payment info submitted. Wait for a payment hash or tx number to verify it.")
                if consultation.status != request.POST.get("status") and request.POST.get("status") != None:
                    consultation.status = request.POST.get("status")
                    consultation.save()
                    messages.success(request, "Status changed")

            return render(request, 'detail.html', context)

        else: # request.method not POST
            return render(request, 'detail.html', context)
    else:
        return HttpResponseForbidden('<h1>403 Forbidden</h1><p>You have no access to this site</p>', content_type='text/html')

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['requesters', 'supervisors'])
def add(request):
    form = ConsultationForm(request.POST or None)
    UploadedFileFormset = modelformset_factory(UploadedFile , exclude=('consultation',), extra=5, max_num=5)
    formset = UploadedFileFormset(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    consultation = form.save(commit=False)
                    consultation.requester_id = request.user.id
                    consultation.save()
                    for upload in formset:
                        if upload.cleaned_data != {}: # prevent saving empty forms as uploads
                            data = upload.save(commit=False)
                            data.consultation = consultation
                            data.save()
            except IntegrityError:
                messages.success(request, "Error found while saving form. Check your information or contact web admin")

            messages.success(request, 'Your consultation is created and an advisor will write you back soon')
            return redirect('consultations:index')
        else:
            messages.error(request, "There are errors in your consultation form. Check your information")

            context = {
                'form' : form,
                'formset' : formset
            }
            return render(request, 'add.html', context)
    else:
        formset = UploadedFileFormset(queryset=UploadedFile.objects.none())
        context = {
            'form' : form,
            'formset' : formset
        }
        return render(request, 'add.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['requesters', 'supervisors'])
def change(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    if request.user.id==consultation.requester_id:
        if request.method == 'POST':
            form = ConsultationForm(request.POST, instance=consultation)
            UploadedFileFormset = modelformset_factory(UploadedFile , exclude=('consultation',), extra=5, max_num=5)
            formset = UploadedFileFormset(request.POST or None, request.FILES or None)
            if form.is_valid() and formset.is_valid():
                try:
                    with transaction.atomic():
                        consultation = form.save(commit=False)
                        consultation.requester_id = request.user.id
                        consultation.save()
                        for upload in formset:
                            if upload.cleaned_data != {}: # prevent saving empty forms as uploads
                                data = upload.save(commit=False)
                                data.consultation = consultation
                                data.save()
                except IntegrityError:
                    messages.success(request, "Error found while saving form. Check your information or contact web admin")

                messages.success(request, "Your consultation was saved and an advisor will write you back soon")
                return redirect('consultations:index')
            else:
                messages.error(request, "There are errors in your consultation form. Check your information")

                context = {
                    'form' : form,
                    'formset' : formset
                }
                return render(request, 'add.html', context)
        else:
            UploadedFileFormset = modelformset_factory(UploadedFile , exclude=('consultation',), extra=5, max_num=5)
            form = ConsultationForm(instance=consultation)
            formset = UploadedFileFormset(queryset=UploadedFile.objects.filter(consultation=consultation_id))
            context = {
                'form': form,
                'formset': formset
            }
            return render(request, 'change.html', context)
    else:
        return HttpResponseForbidden('<h1>403 Forbidden</h1><p>You have no access to this site</p>', content_type='text/html')

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['requesters', 'supervisors'])
def delete(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    if request.user.id==consultation.requester_id:
        consultation.delete()
        messages.success(request, "Consultation deleted")
        return redirect('consultations:index')
    else:
        return HttpResponseForbidden('<h1>403 Forbidden</h1><p>You have no access to this site</p>', content_type='text/html')

def pricing(request):
    context = {}
    return render(request, 'pricing.html', context)

def faq(request):
    context = {}
    return render(request, 'faq.html', context)

def terms(request):
    context = {}
    return render(request, 'terms.html', context)

def contact(request):
    context = {}
    return render(request, 'contact.html', context)