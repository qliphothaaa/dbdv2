from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.
def load_file(request):
    if request.method == "POST":
        File = request.FILES.get("files", None)
        if File is None:
            return HttpResponse("no file")
        if not '.csv' in File.name:
            return HttpResponse("unavailable file type")
        else:
            with open("./csv_files/mdbd.csv", 'wb+') as  f:
                for chunk in File.chunks():
                    f.write(chunk)
            return render(request, "upload_file.html", {'result':'ok'})
    else:
        return render(request, "upload_file.html")
