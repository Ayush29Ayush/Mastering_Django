from django.forms import ValidationError
from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy, reverse

from firstapp.forms import ContactUsForm


# Create your views here.
# def index(request):
#     age = 20
#     arr = ["ayush", "hey", "world", "dragon"]
#     dic = {"a": "one", "b": "two"}

#     context = {
#         "age": age,
#         "array": arr,
#         "dic": dic

#     }
#     return render(
#         request,
#         "firstapp/index.html",
#         context=context
#     )
#     # return HttpResponse("<h1>Hello</h1>")


class Index(TemplateView):
    template_name = "firstapp/index.html"

    def get_context_data(self, **kwargs):
        age = 10
        arr = ["ayush", "hey", "world", "dragon"]
        dic = {"a": "one", "b": "two"}
        context_old = super().get_context_data(**kwargs)
        context = {"age": age, "array": arr, "dic": dic, "context_old": context_old}
        return context


def contactus(request):
    if request.method == "POST":
        print(request.POST)
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST["phone"]
        if len(phone) < 10 or len(phone) > 10:
            raise ValidationError("Phone number length is not right")
        query = request.POST["query"]

        print(name + " " + email + " " + phone + " " + query)

    return render(request, "firstapp/contactus.html")


#! Functional based approach
def contactus2(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)

        if form.is_valid():  #! cleaned_data is created by is_valid()
            if len(form.cleaned_data.get("query")) > 10:
                form.add_error("query", "Query length is not right")  #! Approach 1 -> This one is better
                return render(request, "firstapp/contactus2.html", {"form": form})
            form.save()
            return HttpResponse("Thank You")
        else:
            if len(form.cleaned_data.get("query")) > 10:
                # form.add_error("query", "Query length is not right")
                form.errors["__all__"] = ("Query length is not right. It should be in 10 digits.")  #! Approach 2
            return render(request, "firstapp/contactus2.html", {"form": form})

    return render(request, "firstapp/contactus2.html", {"form": ContactUsForm})

#! Class based approach
class ContactUs(FormView):
    form_class = ContactUsForm
    template_name = 'firstapp/contactus2.html'
    #success_url = '/'   #hardcoded url
    success_url = reverse_lazy('index')
    def form_valid(self, form):
        if len(form.cleaned_data.get('query'))>10:
            form.add_error('query', 'Query length is not right')
            return render(self.request, 'firstapp/contactus2.html', {'form':form})
        form.save()
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        if len(form.cleaned_data.get('query'))>10:
            form.add_error('query', 'Query length is not right')
            #form.errors['__all__'] = 'Query length is not right. It should be in 10 digits.'
        response = super().form_invalid(form)
        return response