from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ResumeTemplate, ResumeOrder, Resume,Contact
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
import io
import base64
import os
from django.contrib import messages
from django.conf import settings
from django.utils.html import escape
from xhtml2pdf import pisa
from django.template.loader import get_template
from .forms import CustomUserCreationForm,ContactForm
from weasyprint import HTML,CSS
from django.template.loader import get_template
from django.core.files.base import ContentFile
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    templates = ResumeTemplate.objects.filter(id__in=[1, 3, 6])
    return render(request, 'resume/home.html', {'templates': templates})

def about(request):
    return render(request,'resume/about.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')  # Redirect to a success page
    else:
        form = ContactForm()
    
    return render(request, 'resume/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'resume/contact_success.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'resume/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    form = AuthenticationForm()
    return render(request, 'resume/login.html', {'form': form})

def select_template(request):
    templates = ResumeTemplate.objects.filter(id__in=[1, 2,3,4,5,6])
    return render(request, 'resume/course.html', {'templates': templates})


@login_required
def edit_resume(request, template_id):
    """ User edits their resume details and saves progress. """
    template = get_object_or_404(ResumeTemplate, id=template_id)
    resume, created = Resume.objects.get_or_create(user=request.user, template=template)
    

    if request.method == 'POST':
        
        project_names = request.POST.getlist("project_name[]")
        project_descriptions = request.POST.getlist("project_description[]")
        project_technologies = request.POST.getlist("technologies[]")
        
        print("DEBUG: Project Names:", project_names)  # Debugging
        print("DEBUG: Project Descriptions:", project_descriptions)  # Debugging
        print("DEBUG: Project Technologies:", project_technologies) 
        
        projects = []
        for i in range(len(project_names)):
            if project_names[i]:  # Ensure the project has a name
                projects.append({
                    "name": project_names[i],
                    "description": project_descriptions[i] if i < len(project_descriptions) else "",
                    "technologies": project_technologies[i] if i < len(project_technologies) else "",
                })

        degrees = request.POST.getlist("degree[]")
        colleges = request.POST.getlist("college[]")
        years = request.POST.getlist("year[]")

        # Handling multiple education entries
        education_entries = []
        for i in range(len(degrees)):
            if degrees[i]:  # Ensure there is a degree name
                education_entries.append({
                    "degree": degrees[i],
                    "college": colleges[i] if i < len(colleges) else "",
                    "year": years[i] if i < len(years) else "",
                })
        
        if 'profile_photo' in request.FILES:
            profile_photo = request.FILES['profile_photo']
            resume.profile_photo = profile_photo
            resume.save()
        
        updated_data = {
            "full_name": request.POST.get("full_name", ""),
            "professional_summary":request.POST.get("professional_summary", ""),
            "email": request.POST.get("email", ""),
            "phone": request.POST.get("phone", ""),
            "linkedin": request.POST.get("linkedin", ""),
            "degree": request.POST.get("degree", ""),
            "college": request.POST.get("college", ""),
            "year": request.POST.get("year", ""),
            "font_family": request.POST.get("font_family", ""),
            "font_size": request.POST.get("font_size", ""),
            "font_weight": request.POST.get("font_weight", ""),
            "font_color": request.POST.get("font_color", ""),
            "background_color": request.POST.get("background_color", ""),
            "font_style": request.POST.get("font_style", ""),
            "border_style": request.POST.get("border_style", ""),
            "section_spacing": request.POST.get("section_spacing", ""),
            "section_alignment": request.POST.get("section_alignment", ""),
            "header": request.POST.get("header", ""),
            "experience": request.POST.get("experience", ""),
            "skills": request.POST.get("skills", ""),
            "contact": request.POST.get("contact", ""),
            "company_name": request.POST.get("company_name", ""),
            "role": request.POST.get("role", ""),
            "duration": request.POST.get("duration", ""),
            
            "skills": request.POST.get("skills", ""),
            "certifications": request.POST.get("certifications", ""),
            "languages": request.POST.get("languages", ""),
            "interest": request.POST.get("interest", ""),
            
            "projects": projects,
            "education": education_entries
        }

        resume.data = updated_data
        resume.save()
        return redirect('preview_resume', resume_id=resume.id)

    template_filename = f'resume/edit_resume_{template_id}.html'
    return render(request, template_filename, {'template': template, 'resume': resume})


@login_required
def preview_resume(request, resume_id):
    """ User previews the resume before placing an order. """
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    allowed_template_ids = {1, 2,3 ,4,5,6}
    template_id = resume.template.id if resume.template.id in allowed_template_ids else 1  # Default to template_1

    print(f"DEBUG: Selected Template ID: {template_id}")
    
    profile_photo_url = resume.profile_photo.url if resume.profile_photo else None
    
    template_filename = f"resume/preview_template_{template_id}.html"
    
    return render(request, template_filename, {"resume": resume,"profile_photo": profile_photo_url})

def get_base64_image(image_path):
    """Convert image to base64 encoding for PDF rendering."""
    try:
        with open(image_path, "rb") as img_file:
            return f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
    except FileNotFoundError:
        return None  # Return None if file is not found

def generate_pdf(order):
    """ Generate a PDF from the resume order using xhtml2pdf (pisa). """
    try:
        resume = Resume.objects.get(user=order.user, template=order.template)
        
        profile_photo_url = None
        if resume.profile_photo:
            profile_photo_path = os.path.join(settings.MEDIA_ROOT, resume.profile_photo.name)
            profile_photo_url = get_base64_image(profile_photo_path)

        context = {
            'user': order.user,
            'professional_summary' : order.professional_summary,
            'template': order.template,
            'font_family': order.font_family or "Arial",
            'font_size': order.font_size or "12px",
            'font_weight': order.font_weight or "normal",
            'font_color': order.font_color or "#000000",
            'background_color': order.background_color,
            'font_style': order.font_style,
            'border_style': order.border_style,
            'section_spacing': order.section_spacing or "10px",
            'section_alignment': order.section_alignment or "left",
            'header': resume.data.get('header', 'Default Header'),
            'full_name': resume.data.get('full_name'),
            'email': resume.data.get('email'),
            'phone': resume.data.get('phone'),
            'linkedin': resume.data.get('linkedin'),
            
            # Handle multiple education entries
            'education': resume.data.get('education', []),
            
            'skills': resume.data.get('skills'),
            'certifications': resume.data.get('certifications'),
            'languages': resume.data.get('languages'),
            'interest': resume.data.get('interest'),
            
            'experience': resume.data.get('experience', 'No experience available'),
            'skills': resume.data.get('skills', 'No skills available'),
            'contact': resume.data.get('contact', 'No contact information available'),
            'company_name': resume.data.get('company_name'),
            'role': resume.data.get('role'),
            'duration': resume.data.get('duration'),
            'projects': resume.data.get('projects', []),
            'profile_photo': profile_photo_url,
        }

        template_id = resume.template.id if resume.template.id in {1, 2, 3, 4,5,6} else 1
        template_filename = f"resume/resume_template_{template_id}.html"

        template = get_template(template_filename)
        html_content = template.render(context)

        if not html_content.strip():
            raise ValueError("Generated HTML is empty. Check template rendering.")

        pdf_file = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.StringIO(html_content), dest=pdf_file)

        if pisa_status.err:
            raise ValueError("PDF generation failed due to pisa error.")

        return ContentFile(pdf_file.getvalue(), name=f"resumes/{order.user.username}_resume.pdf")

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None  # Handle failure gracefully


@login_required
def place_order(request, resume_id):
    """ User places an order, and the PDF is generated using xhtml2pdf. """
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    profile_photo_url = resume.profile_photo.url if resume.profile_photo else None


    order = ResumeOrder.objects.create(
        user=request.user,
        professional_summary = request.professional_summary,
        full_name=resume.data.get('full_name'),
        email=resume.data.get('email'),
        phone=resume.data.get('phone'),
        linkedin=resume.data.get('linkedin'),
        education=resume.data.get('education', []),
        company_name=resume.data.get('company_name'),
        role=resume.data.get('role'),
        duration=resume.data.get('duration'),
        skills = resume.data.get('skills'),
        certifications= resume.data.get('certifications'),
        languages = resume.data.get('languages'),
        interest = resume.data.get('interest'),
        template=resume.template,
        font_family=resume.data.get('font_family', "Arial"),
        font_size=resume.data.get('font_size', "12"),
        font_weight=resume.data.get('font_weight', "normal"),
        font_style=resume.data.get('font_style'),
        border_style=resume.data.get('border_style'),
        font_color=resume.data.get('font_color', "#000000"),
        background_color=resume.data.get('background_color'),
        section_spacing=resume.data.get('section_spacing', "10"),
        section_alignment=resume.data.get('section_alignment', "center"),
        projects=resume.data.get('projects', []),  # ✅ Add projects to ResumeOrder
        profile_photo=profile_photo_url,
    )
    order.save()
    
    print(f"DEBUG: Order ID = {order.id}")

    # ✅ Generate and Save PDF
    pdf_file = generate_pdf(order)
    if pdf_file:
        order.pdf_file.save(f"{order.user.username}_resume.pdf", pdf_file, save=True)
    else:
        return HttpResponse("PDF generation failed. Please try again later.", status=500)

    return redirect('checkout_page', order_id=order.id)


@login_required
def checkout_page(request, resume_id):
    """Creates an order if missing, then shows checkout details"""
    
    # Fetch resume & associated template
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    profile_photo_url = resume.profile_photo.url if resume.profile_photo else None
    
    # Create or update order
    order, created = ResumeOrder.objects.update_or_create(
        user=request.user,
        template=resume.template,
        defaults={
            "full_name": resume.data.get("full_name", ""),
            "professional_summary":resume.data.get("professional_summary",""),
            "email": resume.data.get("email", ""),
            "phone": resume.data.get("phone", ""),
            "linkedin": resume.data.get("linkedin", ""),
            'education': resume.data.get('education', []),
            "company_name": resume.data.get("company_name", ""),
            "role": resume.data.get("role", ""),
            "duration": resume.data.get("duration", ""),
            "skills": resume.data.get("skills", ""),
            "certifications": resume.data.get("certifications", ""),
            "languages": resume.data.get("languages", ""),
            "interest": resume.data.get("interest", ""),
            "font_family": resume.data.get("font_family", "Arial"),
            "font_size": resume.data.get("font_size", "12"),
            "font_weight": resume.data.get("font_weight", "normal"),
            "font_style": resume.data.get("font_style", ""),
            "border_style": resume.data.get("border_style", ""),
            "font_color": resume.data.get("font_color", "#000000"),
            "background_color": resume.data.get("background_color", ""),
            "section_spacing": resume.data.get("section_spacing", "10"),
            "section_alignment": resume.data.get("section_alignment", "center"),
            "projects": resume.data.get("projects", []),
            "qr_payment": None,  # Default to None before upload
            "payment_status": "pending",  # Set order as pending until payment proof is uploaded
            "profile_photo": profile_photo_url,
        }
    )

    print(f"DEBUG: Order ID = {order.id}")

    # ✅ Generate and Save PDF
    pdf_file = generate_pdf(order)
    if pdf_file:
        order.pdf_file.save(f"{order.user.username}_resume.pdf", pdf_file, save=True)
    else:
        return HttpResponse("PDF generation failed. Please try again later.", status=500)

    print(f"DEBUG: Before handling payment upload")

    # ✅ Handle Payment Upload (POST Request)
    if request.method == "POST":
        qr_payment = request.FILES.get("qr_payment")

        if qr_payment:
            print(f"DEBUG: ✅ Received QR Payment file: {qr_payment.name}")
            order.qr_payment = qr_payment  # ✅ Save the file correctly
            order.payment_status = "pending"
            order.save()
            print(f"DEBUG: ✅ Saved QR Payment to order {order.id}")
            return redirect("thank_you")

        print("DEBUG: ❌ No payment file uploaded!")

    return render(request, "resume/checkout_page.html", {"order": order})


def initiate_checkout(request, resume_id):
    """ Confirm order details before proceeding to checkout. """
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    # Check if the user already has a pending order for this resume
    existing_order = ResumeOrder.objects.filter(user=request.user, resume=resume, payment_status="pending").first()
    if existing_order:
        return redirect('checkout_page', order_id=existing_order.id)

    return render(request, "resume/initiate_checkout.html", {"resume": resume})

def thank_you(request):
    """ Thank You Page after checkout """
    return render(request, "resume/thank_you.html")

def my_account(request):
    """ Show user's orders if payment is approved, else show a message. """
    orders = ResumeOrder.objects.filter(user=request.user, payment_status="approved")

    return render(request, "resume/my_account.html", {"orders": orders})

def download_resume(request, order_id):
    """ User downloads the ordered PDF resume. """
    order = get_object_or_404(ResumeOrder, id=order_id, user=request.user)
    pdf_file = order.pdf_file

    print(f"PDF file path: {pdf_file.path}")
        
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={order.pdf_file.name}'
    return response

