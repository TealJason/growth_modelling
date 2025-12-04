from django.shortcuts import render
from .utils import run_model
from django.utils.timezone import now

def index(request):
    growth_html_string = None  # initialize to prevent reference errors

    if request.method == "POST":
        ininital_density = request.POST.get("i_density", "")
        platau_density = request.POST.get("p_density", "")
        growth_rate = request.POST.get("g_rate", "")
        species = request.POST.get("species", "")
        temperature = request.POST.get("temperature", "")
        number_of_time_steps = request.POST.get("time_steps")

        if not ininital_density or not platau_density or not growth_rate:
            context = {"result": None, "searched": False}
        else:
            growth_df = run_model(ininital_density, platau_density, growth_rate,
                                  temperature, species, number_of_time_steps)
            growth_html_string = growth_df.to_html(header=True, table_id="growth_table")
            context = {"result": growth_html_string,"searched": True, "timestamp": now().timestamp()}

        # Check for AJAX request
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(request, "partials/result.html", context)

        return render(request, "index.html", context)

    return render(request, "index.html")
