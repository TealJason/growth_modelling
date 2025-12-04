from django.shortcuts import render
from . utils import run_model

def index(request): 
    if request.method == "POST":
        ininital_density = request.POST.get("i_density","").
        platau_density =  request.POST.get("p_density","")
        growth_rate =  request.POST.get("g_rate","")
        species = request.POST.get("species","")
        
        if not ininital_density or not platau_density or not growth_rate:
            return render(request, "index.html", {"result": None, "seatched":False})
        
        growth_df = run_model(ininital_density,platau_density,growth_rate)
        
        growth_html_string = growth_df.to_html(header=True, table_id="growth_table")
        
        return render(request, "index.html", {"result": growth_html_string, "searched": True})
    
    return render(request, "index.html")

