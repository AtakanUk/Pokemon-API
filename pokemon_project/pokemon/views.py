from django.shortcuts import render
from django.http import JsonResponse
from .forms import PokemonForm
from .util import *
from .pokemonUtil import *
from django.core.exceptions import ValidationError
import os

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
            pdf_filenames = []

            for email_address in email_addresses:
                if not is_valid_email(email_address):
                    failure_messages.append(f"Invalid email address: {email_address}")
                    continue

            if failure_messages:
                return JsonResponse({'message': '\n'.join(failure_messages), 'success': False}, status=400)

            for pokemon_name in pokemon_names:
                data = retrieve_pokemon_data(pokemon_name)

                if data:
                    abilities = get_pokemon_abilities(data)
                    pdf_filename = create_pdf(pokemon_name, abilities)
                    pdf_filenames.append(pdf_filename)
                    success_messages.append(f"Abilities for {pokemon_name} are ready.")
                else:
                    failure_messages.append(f"Failed to retrieve data for {pokemon_name}")
            
            if failure_messages:        
                return JsonResponse({'message': '\n'.join(failure_messages), 'success': False}, status=400)
            merged_pdf_filename = merge_pdfs(pdf_filenames)

            if not merged_pdf_filename:
                return JsonResponse({'message': 'Failed to merge PDF files', 'success': False}, status=400)
            
            if len(pokemon_names) == 1:
                send_email_with_pdfs(pdf_filenames, email_addresses)
            else:
                send_email_with_pdfs(pdf_filenames + [merged_pdf_filename], email_addresses)

            for pdf_filename in pdf_filenames:
                os.remove(pdf_filename)

            os.remove(merged_pdf_filename)

            return JsonResponse({'message': 'Email sent successfully', 'success': True})
        else:
            return JsonResponse({'message': 'Form data is invalid', 'success': False}, status=400)
    else:
        form = PokemonForm()
        return render(request, 'pokemon/email_pokemon.html', {'form': form})
