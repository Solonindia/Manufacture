from django.shortcuts import render, redirect
from .models import MainProcess, SubProcess
from .forms import MainProcessForm, SubProcessForm

def production_table(request):
    # Fetch all main processes and their related sub-processes
    main_processes = MainProcess.objects.prefetch_related('subprocesses').all()

    context = {
        'main_processes': main_processes,
    }
    return render(request, 'production_table.html', context)

def add_data(request):
    # Handling POST request to add new data
    if request.method == 'POST':
        main_form = MainProcessForm(request.POST)
        sub_form = SubProcessForm(request.POST)

        if main_form.is_valid():
            new_main_process = main_form.save()  # Save new main process
        if sub_form.is_valid():
            sub_process = sub_form.save(commit=False)
            # Assign the main process to the sub process
            sub_process.main_process = new_main_process
            sub_process.save()  # Save sub process

        # Redirect to the production table page to display newly added data
        return redirect('production_table')

    # Initialize empty forms
    main_form = MainProcessForm()
    sub_form = SubProcessForm()

    context = {
        'main_form': main_form,
        'sub_form': sub_form,
    }
    return render(request, 'add_data.html', context)
