# pokemon/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import PokemonForm
from .util import *
from .pokemonUtil import *
from django.core.exceptions import ValidationError
import os
import PyPDF2

def send_email_with_pdf(pdf_filename, recipients):
    msg = MIMEMultipart()
    msg['From'] = 'atakanuk98@gmail.com'
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = 'Pokemon Abilities'

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(pdf_filename, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % pdf_filename)
    msg.attach(part)

    server = SMTP_SSL('smtp.gmail.com', 465)
    server.login("atakanuk98@gmail.com", "pboi mjsa uhom gmut")
    server.sendmail("atakanuk98@gmail.com", recipients, msg.as_string())
    server.quit()

def email_pokemon(request):
    if request.method == 'POST':
        form = PokemonForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            email_addresses = email.split()
            temp = form.cleaned_data['pokemon_name']
            pokemon_names = temp.split()

            success_messages = []
            failure_messages = []
            pdf_filenames = []  # To store generated PDF file names

            for pokemon_name in pokemon_names:
                data = retrieve_pokemon_data(pokemon_name)

                if data:
                    abilities = get_pokemon_abilities(data)
                    pdf_filename = create_pdf(pokemon_name, abilities)
                    pdf_filenames.append(pdf_filename)

                    success_messages.append(f"Abilities for {pokemon_name} are ready.")
                else:
                    failure_messages.append(f"Failed to retrieve data for {pokemon_name}")

            # Merge multiple PDFs into one
            merged_pdf_filename = merge_pdfs(pdf_filenames)

            # Send the merged PDF to the provided email addresses
            send_email_with_pdf(merged_pdf_filename, email_addresses)

            # Clean up temporary PDF files
            for pdf_filename in pdf_filenames:
                os.remove(pdf_filename)

            # Clean up the merged PDF file
            os.remove(merged_pdf_filename)

            return JsonResponse({'message': 'Email sent successfully', 'success': True})
        else:
            return JsonResponse({'message': 'Form data is invalid', 'success': False}, status=400)
    else:
        form = PokemonForm()
        return render(request, 'pokemon/email_pokemon.html', {'form': form})
    
def merge_pdfs(pdf_filenames):    
    if not pdf_filenames:
        return None
    # Create a PdfFileMerger object
    pdf_merger = PyPDF2.PdfMerger()
    try:
        # Append each PDF to the merger
        for pdf_filename in pdf_filenames:
            pdf_merger.append(pdf_filename)
        # Define the filename for the merged PDF
        merged_pdf_filename = 'merged.pdf'
        # Write the merged PDF to the output file
        pdf_merger.write(merged_pdf_filename)
        return merged_pdf_filename
    except Exception as e:
        print(f"Failed to merge PDFs: {str(e)}")
        return None
    finally:
        # Close the PdfFileMerger object
        pdf_merger.close()
