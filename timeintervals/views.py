from django.shortcuts import render, redirect, get_object_or_404
from .models import Process,ProcessInterval
from .forms import ProcessForm, ProcessIntervalFormSet,ProcessIntervalForm
from datetime import datetime, timedelta
from itertools import groupby
from django.utils import timezone
from .models import ProcessInterval1
from .forms import SignUpForm,LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def button_page(request):
    if request.method == 'POST':
        if 'admin' in request.POST:
            return redirect('login')
        elif 'user' in request.POST:
            return redirect('loginu')
    return render(request, 'button_page.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('admin')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user')  # Redirect to your desired page
            else:
                # Return an 'invalid login' error message.
                return render(request, 'loginu.html', {'form': form, 'error_message': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'loginu.html', {'form': form})

VALID_USERNAME = 'admin'
VALID_PASSWORD = 'res@123'

def login1_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                # Redirect to the main page or a protected page
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

from collections import defaultdict
def process_list(request):
    # Fetch all processes with prefetching related intervals
    processes = Process.objects.prefetch_related('intervals').all().order_by('created_at')

    # Group processes by main_process and sub_process using defaultdict
    grouped_processes = defaultdict(list)

    for process in processes:
        key = (process.main_process, process.sub_process)
        grouped_processes[key].append(process)

    # Prepare time intervals (10-minute intervals between 08:30 and 00:00)
    time_intervals = []
    start_time = datetime.strptime('08:30', '%H:%M')
    end_time = datetime.strptime('00:00', '%H:%M') + timedelta(days=1)

    while start_time < end_time:
        next_time = start_time + timedelta(minutes=10)
        time_intervals.append(f"{start_time.strftime('%H:%M')}-{next_time.strftime('%H:%M')}")
        start_time = next_time

    # Process each group to add interval information
    process_details = []  # Temporary list to store process and interval data

    for group in grouped_processes.values():
        for process in group:
            start_infos = []
            end_infos = []
            startend_infos = []

            add_info = process.add_info  # Add any process-specific info (no changes here)

            def generate_interval_info(interval_field, time_type):
                interval_infos = []
                # Iterate over the related 'intervals' for the given process
                for interval in process.intervals.all():
                    if getattr(interval, time_type):  # Check if the time_type field is set
                        time_obj = getattr(interval, time_type)  # Get the time object (start_time, end_time, or startend_time)
                        formatted_time = time_obj.strftime('%H:%M')
                        next_time = (datetime.combine(datetime.today(), time_obj) + timedelta(minutes=10)).strftime('%H:%M')
                        time_range = f"{formatted_time}-{next_time}"
                        
                        # Map the correct info field based on the time_type
                        if time_type == 'start_time':
                            info = interval.start_info
                        elif time_type == 'end_time':
                            info = interval.end_info
                        else:  # for startend_time
                            info = interval.startend_info
                        
                        interval_infos.append({'time_range': time_range, 'info': info})
                
                return interval_infos

            # Generate the interval information
            start_infos = generate_interval_info('start_infos', 'start_time')
            end_infos = generate_interval_info('end_infos', 'end_time')

            # Store the process with its generated interval information in a dictionary
            process_details.append({
                'process': process,
                'start_infos': start_infos,
                'end_infos': end_infos,
                'add_info': add_info,
            })

    return render(request, 'process_list.html', {
        'process_details': process_details,
        'time_intervals': time_intervals,
    })
def process_add(request):
    if request.method == 'POST':
        main_process = request.POST.get('main_process')
        sub_process = request.POST.get('sub_process')
        add_info = request.POST.get('add_info')

        # Check if the main process already exists
        existing_main_process = Process.objects.filter(main_process=main_process).first()

        if existing_main_process:
            # If the main process exists, create a new sub-process under it
            Process.objects.create(
                main_process=existing_main_process,
                sub_process=sub_process,
                add_info=add_info
            )
        else:
            # If the main process doesn't exist, create a new main process and sub-process
            Process.objects.create(
                main_process=main_process,
                sub_process=sub_process,
                add_info=add_info
            )

        return redirect('process_list')  # Redirect back to the process list view (or wherever)

    return render(request, 'process_add.html')

def process_edit(request, process_id):
    process = get_object_or_404(Process, pk=process_id)  # Fetch the process object

    # Initialize the main form and the formset
    if request.method == 'POST':
        form = ProcessForm(request.POST, instance=process)  # Edit the existing process
        formset = ProcessIntervalFormSet(request.POST, instance=process)  # Edit the existing intervals
        
        if form.is_valid() and formset.is_valid():  # Check both forms for validity
            form.save()  # Save the main process form
            formset.save()  # Save the intervals formset
            return redirect('process_list')  # Redirect to the process list after saving
    else:
        form = ProcessForm(instance=process)  # If GET request, just load the existing process
        formset = ProcessIntervalFormSet(instance=process)  # Load the existing intervals

    return render(request, 'process_edit.html', {
        'form': form,  # Pass the main form to the template
        'formset': formset,  # Pass the formset to the template
        'process': process,  # Optionally pass the process object to the template if needed
    })

def add_process_interval(request, process_id):
    process = get_object_or_404(Process, pk=process_id)

    if request.method == 'POST':
        form = ProcessIntervalForm(request.POST)
        if form.is_valid():
            interval = form.save(commit=False)  # Do not save yet
            interval.process = process  # Associate with the correct process
            interval.save()  # Now save it
            return redirect('process_edit', process_id=process.id)  # Use process_id instead of pk
    else:
        form = ProcessIntervalForm()

    return render(request, 'add_process_interval.html', {
        'form': form,
        'process': process,
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import ProcessInterval1
from .forms import ProcessForm1, ProcessIntervalFormSet1
from datetime import datetime, timedelta
from itertools import groupby
from django.utils import timezone
import pandas as pd
import pytz

def Home(request):
    return render(request, 'Home.html')

def process_list1(request):
    processes = Process.objects.prefetch_related('intervals1').all().order_by('created_at')
    
    # Group processes by main_process and sub_process
    grouped_processes = [
        list(group) for key, group in groupby(processes, key=lambda p: (p.main_process, p.sub_process))
    ]

    # Get the current time in the server's timezone and convert to the local timezone if needed
    local_timezone = pytz.timezone('Asia/Kolkata')  # Replace with your timezone if different
    now = timezone.now().astimezone(local_timezone)
    start_time = now.replace(second=0, microsecond=0, minute=(now.minute // 10) * 10)  # Round down to the nearest 10 minutes
    end_time = start_time + timedelta(hours=6)  # End 6 hours from the current time

    # Generate 10-minute intervals from start_time to end_time
    time_intervals = []
    while start_time < end_time:
        next_time = start_time + timedelta(minutes=10)
        time_range = f"{start_time.strftime('%H:%M')}-{next_time.strftime('%H:%M')}"
        time_intervals.append(time_range)
        start_time = next_time

    # Process each grouped process
    for group in grouped_processes:
        for process in group:
            start_infos = []
            end_infos = []
            startend_infos = []
            add_info = process.add_info  

            # Iterate over the intervals1 related to this process
            for interval in process.intervals1.all():
                # Start Time Range
                if interval.start_time:
                    formatted_start_time = interval.start_time.strftime('%H:%M')
                    next_start_time = (datetime.combine(datetime.today(), interval.start_time) + timedelta(minutes=10)).strftime('%H:%M')
                    start_infos.append({'time_range': f"{formatted_start_time}-{next_start_time}", 'info': interval.start_info})

                # End Time Range
                if interval.end_time:
                    formatted_end_time = interval.end_time.strftime('%H:%M')
                    next_end_time = (datetime.combine(datetime.today(), interval.end_time) + timedelta(minutes=10)).strftime('%H:%M')
                    end_infos.append({'time_range': f"{formatted_end_time}-{next_end_time}", 'info': interval.end_info})

                # Start-End Time Range
                if interval.startend_time:
                    formatted_startend_time = interval.startend_time.strftime('%H:%M')
                    next_startend_time = (datetime.combine(datetime.today(), interval.startend_time) + timedelta(minutes=10)).strftime('%H:%M')
                    startend_infos.append({'time_range': f"{formatted_startend_time}-{next_startend_time}", 'info': interval.start_info})

            # Attach information to the process
            process.start_infos = start_infos
            process.end_infos = end_infos
            process.startend_infos = startend_infos
            process.add_info = add_info

    return render(request, 'process_list1.html', {
        'grouped_processes': grouped_processes,
        'time_intervals': time_intervals,
    })

def process_full(request):
    processes = Process.objects.prefetch_related('intervals1').all().order_by('created_at')
    
    grouped_processes = []
    
    # Group by main_process and sub_process
    for key, group in groupby(processes, key=lambda p: (p.main_process, p.sub_process)):
        grouped_processes.append(list(group))

    time_intervals = []
    start_time = datetime.strptime('08:30', '%H:%M')
    end_time = datetime.strptime('00:00', '%H:%M') + timedelta(days=1)

    while start_time < end_time:
        next_time = start_time + timedelta(minutes=10)
        time_intervals.append(f"{start_time.strftime('%H:%M')}-{next_time.strftime('%H:%M')}")
        start_time = next_time

    for group in grouped_processes:
        for process in group:
            start_infos = []
            end_infos = []
            startend_infos = []            
            add_info = process.add_info  

            for interval in process.intervals1.all():  # Use intervals1 only
                if interval.start_time:
                    formatted_start_time = interval.start_time.strftime('%H:%M')
                    next_start_time = (datetime.combine(datetime.today(), interval.start_time) + timedelta(minutes=10)).strftime('%H:%M')
                    time_range = f"{formatted_start_time}-{next_start_time}"
                    start_infos.append({'time_range': time_range, 'info': interval.start_info})

                if interval.end_time:
                    formatted_end_time = interval.end_time.strftime('%H:%M')
                    next_end_time = (datetime.combine(datetime.today(), interval.end_time) + timedelta(minutes=10)).strftime('%H:%M')
                    time_range = f"{formatted_end_time}-{next_end_time}"
                    end_infos.append({'time_range': time_range, 'info': interval.end_info})

                if interval.startend_time:
                    formatted_startend_time = interval.startend_time.strftime('%H:%M')
                    next_startend_time = (datetime.combine(datetime.today(), interval.startend_time) + timedelta(minutes=10)).strftime('%H:%M')
                    time_range = f"{formatted_startend_time}-{next_startend_time}"
                    startend_infos.append({'time_range': time_range, 'info': interval.start_info})

            # Attach start, end, and startend information to the process
            process.start_infos = start_infos
            process.end_infos = end_infos
            process.startend_infos = startend_infos
            process.add_info = add_info  # Store additional info

    return render(request, 'process_list1.html', {
        'grouped_processes': grouped_processes,
        'time_intervals': time_intervals,
    })

def process_add1(request):
    if request.method == 'POST':
        form = ProcessForm1(request.POST)
        if form.is_valid():  # Ensure the form is valid
            form.save()  # Save the Process instance
            return redirect('process_list1')  # Redirect to the process list after saving
    else:
        form = ProcessForm1()  # Initialize an empty form on GET request

    return render(request, 'process_add1.html', {'form': form})


def process_edit2(request,pk):
    process = get_object_or_404(Process, pk=pk)
    if request.method == 'POST':
        formset = ProcessIntervalFormSet1(request.POST, instance=process)

        if formset.is_valid():
            intervals = formset.save(commit=False)  # Do not commit yet

            for interval in intervals:
                interval.process = process  # Associate the interval with the process

                # Ensure that start_time and end_time are valid
                if interval.start_time and interval.end_time:
                    start_dt = datetime.combine(timezone.now().date(), interval.start_time)
                    end_dt = datetime.combine(timezone.now().date(), interval.end_time)

                    # Check if end_time is later than start_time
                    if end_dt <= start_dt:
                        formset.errors.append("End time must be later than start time.")
                        return render(request, 'process_edit2.html', {'formset': formset})

                    # Calculate midpoint for startend_time
                    interval.startend_time = (start_dt + (end_dt - start_dt) / 2).time()

                interval.save()  # Now save the interval

            return redirect('process_list1')  # Redirect to the process list after saving

    else:
        formset = ProcessIntervalFormSet1(queryset=ProcessInterval1.objects.none())  # Ensures empty formset on GET

    return render(request, 'process_edit2.html', {'formset': formset})





