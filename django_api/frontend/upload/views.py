from django.shortcuts import render                                                                                                                                                  

from django.http import HttpResponse

# Create your views here.
def load_file(request):
    if request.method == "POST":
        File = request.FILES.get("files", None)
        if File is None:
            return HttpResponse("no file")

        if '.csv' in File.name:
            with open("./csv_files/mdbd.csv", 'wb+') as  f:  
                for chunk in File.chunks():
                    f.write(chunk)
                    result = File.name + ' upload Succeed'
            return render(request, "upload_file.html", {'result':result})

        if '.pdf' in File.name:
            with open("./pdf_files/"+File.name, 'wb+') as  f:  
                for chunk in File.chunks():
                    f.write(chunk)
                    result = File.name + ' upload Succeed'
            return render(request, "upload_file.html", {'result':result})

        else:
            return HttpResponse("unavailable file type")
    else:
        return render(request, "upload_file.html")
