import json
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.contrib import messages
from mycrm.forms import SignUpForm, AddRecordForm
from mycrm.models import Record


# Create your views here.


@login_required(login_url="/login")
def home(request):
    customer_record = Record.objects.all()
    customer_record_count = customer_record.count()
    context = {
        "customer_record_count": customer_record_count,
    }
    print(customer_record_count)
    return render(request, "home.html", context)


def logout_user(request):
    logout(request)
    messages.add_message(
        request, messages.SUCCESS, "You have been logged out successfully."
    )
    return redirect("home")


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        name = request.POST.get("name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            # messages.error(request, 'Password does not match')
            print("pwd error    ")
            return JsonResponse(
                {"status": "error", "message": "Password does not match"}
            )
        else:
            if form.is_valid():
                form.save()
                # Return a success response
                # messages.success(request, 'User registered successfully!')
                print("done user")
                return JsonResponse(
                    {"status": "success", "message": "User registered successfully!"}
                )

        return JsonResponse(
            {"status": "error", "message": "Invalid request method"}, status=400
        )

    context = {
        "form": form,
    }
    return render(request, "sign-up.html", context)


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, "customer.html", {"customer_record": customer_record})
    else:
        messages.error(request, "Something went wrong.")
        return redirect("home")


def delete_record(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required."}, status=403)

    delete_record = get_object_or_404(Record, id=pk)

    if request.method == "POST":
            delete_record.delete()
            return JsonResponse({"status": "success", "message": "Record deleted."})
    else:
            return JsonResponse(
                {"status": "error", "message": "You don't have permission to delete"}
            )

    return JsonResponse({"error": "Invalid request method."}, status=400)


def add_record_view(request):
    if request.method == "POST":
        form = AddRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"status": "success", "message": "Record added successfully!"}
            )

        else:
            field_errors = {
                field: [str(error) for error in errors]
                for field, errors in form.errors.items()
            }
            return JsonResponse(
                {
                    "status": "error",
                    "message": field_errors,
                    "errors": field_errors,
                },
                status=400,
            )
    else:
        form = AddRecordForm()
    return render(request, "add_record.html", {"form": form})


def update_record(request, pk):
    if not request.user.is_authenticated:
        return render(
            request, "update_record.html", {"error": "Authentication required."}
        )

    update_record = get_object_or_404(Record, id=pk)

    if request.method == "POST":
        forms = AddRecordForm(request.POST or None, instance=update_record)
        if forms.is_valid():
            forms.save()
            return JsonResponse({"status": "success", "message": "Record updated."})
        else:
            errors = forms.errors.as_json()
            return JsonResponse({"status": "error", "errors": errors}, status=400)

    forms = AddRecordForm(instance=update_record)
    data = {
        "id": update_record.id,
        "first_name": update_record.first_name,
        "last_name": update_record.last_name,
        "email": update_record.email,
        "phone": update_record.phone,
        "city": update_record.city,
        "state": update_record.state,
        "created_at": update_record.created_at.strftime("%d/%m/%Y %I:%M:%S %p"),
    }
    update_record_url = reverse("update_record", args=[update_record.id])
    record_url = reverse("record", args=[update_record.id])
    return render(
        request,
        "update_record.html",
        {
            "data": data,
            "forms": forms,
            "update_record_url": update_record_url,
            "record_url": record_url,
        },
    )


def record_list_view(request):
    return render(request, "record_list.html")


def fetch_data(request):
    data = Record.objects.all().values()  # Fetch data from your model
    if data is not None:
        return JsonResponse(list(data), safe=False)


def customer_record_ajax(request, pk):
    if request.user.is_authenticated:
        try:
            customer_record = get_object_or_404(Record, pk=pk)
            data = {
                "id": customer_record.id,
                "first_name": customer_record.first_name,
                "last_name": customer_record.last_name,
                "email": customer_record.email,
                "phone": customer_record.phone,
                "city": customer_record.city,
                "state": customer_record.state,
                "created_at": customer_record.created_at.strftime(
                    "%d/%m/%Y %I:%M:%S %p"
                ),
            }
            print(data)
            return JsonResponse(data)
        except Record.DoesNotExist:
            print("no data")
            return JsonResponse({"error": "Customer record not found."}, status=404)
    else:
        return JsonResponse({"error": "Authentication required."}, status=403)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"status": "success", "message": "Logout successful"})
    else:
        return JsonResponse(
            {"status": "error", "message": "User not authenticated"}, status=403
        )


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            session_duration = timedelta(minutes=3)
            session_expiry_time = datetime.now() + session_duration

            # Store the session expiry time in the session
            request.session["session_expiry_time"] = session_expiry_time.timestamp()
            return JsonResponse(
                {"status": "success", "message": "You are logged in successfully!."}
            )

        else:
            return JsonResponse(
                {"status": "error", "message": "Invalid username or password."}
            )
    return render(request, "sign-in.html")
