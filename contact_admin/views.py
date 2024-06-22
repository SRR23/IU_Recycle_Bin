from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail  # Import for sending email notifications
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_user')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save form data to database (if using the model)
            form.save()

            # # Send email notification to admin (optional)
            # send_mail(
            #     subject='New Contact Form Submission',
            #     message=f'Name: {form.cleaned_data["name"]}\nEmail: {form.cleaned_data["email"]}\n\nMessage:\n{form.cleaned_data["message"]}',
            #     from_email='your_email@example.com',  # Replace with your email
            #     recipient_list=['admin_email@example.com'],  # Replace with admin email
            # )
            
            messages.success(request, "Your message has been sent to the admin")
            return redirect('contact')  # Redirect to success page (optional)
    else:
        form = ContactForm()

    return render(request, 'contact_form.html', {'form': form})