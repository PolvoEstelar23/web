# core/views.py
import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View


API_BASE_URL = "http://127.0.0.1:8001/api/v1/banks"
REQUEST_TIMEOUT = 5


def _api_url(path=""):
    return f"{API_BASE_URL}/{path}".rstrip("/") + "/"


def _api_error(response):
    try:
        details = response.json()
    except ValueError:
        details = response.text.strip()
    return f"La API respondió con un error ({response.status_code}): {details}"


def _bank_form_data(request):
    return {
        "name": request.POST.get("name", "").strip(),
        "address": request.POST.get("address", "").strip(),
        "status": request.POST.get("status") == "on",
    }


class ListBank(View):
    template_name = "core/list_bank.html"

    def get(self, request):
        try:
            response = requests.get(_api_url("list"), timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            banks = response.json()
        except (requests.RequestException, ValueError) as exc:
            error = _api_error(response) if "response" in locals() else str(exc)
            return render(request, self.template_name, {"banks": [], "error": error}, status=502)

        return render(request, self.template_name, {"banks": banks})


class CreateBank(View):
    template_name = "core/bank_form.html"

    def get(self, request):
        return render(request, self.template_name, {"title": "Crear banco"})

    def post(self, request):
        data = _bank_form_data(request)
        if not data["name"] or not data["address"]:
            return render(
                request,
                self.template_name,
                {"title": "Crear banco", "data": data, "error": "El nombre y la dirección son obligatorios."},
                status=400,
            )

        try:
            response = requests.post(_api_url("create"), json=data, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as exc:
            error = _api_error(response) if "response" in locals() else str(exc)
            return render(request, self.template_name, {"title": "Crear banco", "data": data, "error": error}, status=502)

        messages.success(request, "Banco creado correctamente.")
        return redirect("core:listbank")


class DetailBank(View):
    template_name = "core/bank_detail.html"

    def get(self, request, pk):
        try:
            response = requests.get(_api_url(f"detail/{pk}"), timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            bank = response.json()
        except (requests.RequestException, ValueError) as exc:
            error = _api_error(response) if "response" in locals() else str(exc)
            return render(request, "core/error.html", {"error": error}, status=502)

        return render(request, self.template_name, {"bank": bank})


class UpdateBank(View):
    template_name = "core/bank_form.html"

    def get(self, request, pk):
        try:
            response = requests.get(_api_url(f"detail/{pk}"), timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            bank = response.json()
        except (requests.RequestException, ValueError) as exc:
            error = _api_error(response) if "response" in locals() else str(exc)
            return render(request, "core/error.html", {"error": error}, status=502)

        return render(request, self.template_name, {"title": "Editar banco", "bank": bank})

    def post(self, request, pk):
        data = _bank_form_data(request)
        if not data["name"] or not data["address"]:
            data["id"] = pk
            return render(
                request,
                self.template_name,
                {"title": "Editar banco", "data": data, "error": "El nombre y la dirección son obligatorios."},
                status=400,
            )

        try:
            response = requests.put(_api_url(f"update/{pk}"), json=data, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as exc:
            error = _api_error(response) if "response" in locals() else str(exc)
            data["id"] = pk
            return render(request, self.template_name, {"title": "Editar banco", "data": data, "error": error}, status=502)

        messages.success(request, "Banco actualizado correctamente.")
        return redirect("core:detail_bank", pk=pk)


class DeleteBank(View):
    template_name = "core/bank_confirm_delete.html"

    def get(self, request, pk):
        try:
            response = requests.get(_api_url(f"detail/{pk}"), timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            bank = response.json()
        except (requests.RequestException, ValueError) as exc:
            error = _api_error(response) if "response" in locals() else str(exc)
            return render(request, "core/error.html", {"error": error}, status=502)

        return render(request, self.template_name, {"bank": bank})

    def post(self, request, pk):
        try:
            response = requests.delete(_api_url(f"delete/{pk}"), timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as exc:
            error = _api_error(response) if "response" in locals() else str(exc)
            return render(request, "core/error.html", {"error": error}, status=502)

        messages.success(request, "Banco eliminado correctamente.")
        return redirect("core:listbank")
