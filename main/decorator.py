from django.shortcuts import redirect

def user_chief(fun):
    def wrapper(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            if request.user.user.chief == True:
                return fun(self,request,*args,**kwargs)
            return redirect('main:home')
        else:
            return redirect('main:login')
        return redirect('main:home')
    return wrapper


def user_educator(fun):
    def wrapper(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            if request.user.user.chief == False:
                return fun(self,request,*args,**kwargs)
            else:
                return redirect('main:home_admin')
            return redirect('main:home')
        else:
            return redirect('main:login')
        return redirect('main:home')
    return wrapper

def user_chief_fun(fun):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            if request.user.user.chief == True:
                return fun(request,*args,**kwargs)
            return redirect('main:home')
        else:
            return redirect('main:login')
        return redirect('main:home')
    return wrapper