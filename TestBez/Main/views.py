from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import hashlib



def koko(request):
    hashn = ''
    status = {}
    if request.is_ajax():
        if 'webgl unmasked vendor' and 'webgl unmasked renderer' not in request.POST.keys():
            return JsonResponse({'result':'tor'})
        for i,a in request.POST.items():
            if i == 'csrfmiddlewaretoken':
                continue
            if i == 'screenResolution[]':
                hashn += str(request.POST.getlist('screenResolution[]'))
            if i == 'webgl unmasked renderer':
                if len(a.split(',')) <= 1:
                    hashn += 'unnamed'
                else:
                    hashn += str(a.split(',')[-1][0:-1])
            else:
                hashn += str(a)
        
        ip = request.META.get('HTTP_X_REAL_IP')
        hashn = hashlib.sha224(bytes(hashn,'utf-8')).hexdigest()
#        ipbd = MainData.objects.filter(num = ip)
#        hashnbd = MainData.objects.filter(hash = hashn)
        try :
            MainData.objects.get(num = ip)
            status['result'] = 'okay'
            status['ip'] = ip
            status['hash'] = str(hashn)
            status['vpn'] = 'Не используется'
            status['tor'] = 'Не используется'
            
        except:
            try:
                MainData.objects.get(hashn = hashn)
                a = MainData.objects.get(hashn = hashn)
                status['result'] = 'vpn/proxy'
                status['ip'] = MainData.objects.get(hashn = hashn).num
                status['hash'] = a.hashn
                status['vpn'] = 'Используется'
                status['tor'] = 'Не используется'                
            except:
                sa = MainData.objects.create(num = str(ip),hashn = str(hashn))
                sa.save()
                status['result'] = 'new'
                status['ip'] = ip
                status['hash'] = str(hashn)
                status['vpn'] = 'Не используется'
                status['tor'] = 'Не используется'                
        
        #return JsonResponse({'hashn':(hashlib.sha224(bytes(hashn,'utf-8')).hexdigest()),'meta':str(request.META.get('HTTP_X_REAL_IP'))})
        return JsonResponse(status)
        # print(hashlib.sha224(bytes(hashn,'utf-8')).hexdigest())
        # for i in range (27):
        #     if request.POST.get('components['+ str(i) +'][key]') in params_list:
        #         print(request.POST.get('components[' + str(i) + '][key]'))
        #         if request.POST.get('components[' + str(i) + '][value]') == None:
        #             for g in request.POST.getlist('components[' + str(i) + '][value][]'):
        #                 if g.split(':')[0] not in params_list:
        #                     if len(g.split(':')) == 1:
        #                         hashnum += g
        #                     print(g.split(':'))
        #         else:
        #             hashnum += request.POST.get('components[' + str(i) + '][value]')
        #             print(request.POST.get('components[' + str(i) + '][value]'))
        # print(hashnum)



        # for i,a in request.POST.keys():
        #     print(i,a)
        # print(request.POST.getlist('components[6][value][]'))
        # print(request.POST.getlist('components[9][value]'))
        # # print(request.POST.getlist('components[19][value][]'))
        # a = str(request.POST.getlist('components[19][value][]')).split(',')
        # print(request.POST)
        # for i in a[3:]:
        #     print(i.split(':'))
        # print(request.POST['components[6][value][]'])
        # print(request.POST['components[6][value][]'])
        # print(request.POST['components[6][value][]'])
        # print(request.POST['components[6][value][]'])
        # print(request.POST['components[6][value][]'])

        # return HttpResponse('koko')
    return render(request,'main.html')
# Create your views here.