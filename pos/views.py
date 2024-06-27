from django.shortcuts import render
from .forms import *
from .models import *
from django.http import HttpResponse
from datetime import datetime
from django.http import JsonResponse

# Create your views here.

def pos(request):
    return render(request, 'pos/pos.html')



def engagements(request):
    group_form = GroupSelectionForm()
    page_form = PageSelectionForm()
    data = []
    
    if request.method == 'POST':
        group_form = GroupSelectionForm(request.POST)
        page_form = PageSelectionForm(request.POST)
        if group_form.is_valid() and page_form.is_valid():
            selected_group = group_form.cleaned_data['group']
            selected_page = page_form.cleaned_data['page']
            # Process the selected group and page as needed

            print(type(selected_page))
            print(type(selected_group))
            #print(selected_page.customer_engagements_by_date_range_raw('20/05/2024','25/05/2024'))
            print("--------------------")
            #print(selected_page.customer_engagements_bydate_raw('20/05/2024'))
            print("--------------------")
            #data = selected_page.customer_engagements_by_date_range_raw('20/05/2024','22/05/2024')
            data = [["cont","cont2"],[1,2]]
            print(data)

        print("OK")
    context = {
        'group_form': group_form,
        'page_form': page_form,
        'data': data,
    }
    return render(request, 'pos/engagement.html', context)


def date_range_view(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        # Use these dates to filter your data or perform other operations
        
        # Your data fetching logic here
        data = [["conte1","conte23"],[1,2],[2,6]]
        
        context = {
            'data': data,
            'start_date': start_date,
            'end_date': end_date,
        }
        print(f"Request header detail: {request.headers.get('X-Requested-With')}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # If it's an AJAX request, return only the results partial
            print(data)
            
            return render(request, 'pos/load_result.html', context)
            #return JsonResponse(data)
        else:
            # For a full page load, render the entire template
            return render(request, 'pos/load_result.html', context)
    
    # If no dates provided, just render the initial page
    return render(request, 'pos/load_result.html')