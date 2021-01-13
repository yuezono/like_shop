import logging
from django.urls import reverse_lazy
from django.views import generic
from .forms import InquiryForm, ShopsCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from .models import Shops

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
  template_name = 'index.html'

class InquiryView(generic.FormView):
  template_name = 'inquiry.html'
  form_class = InquiryForm
  success_url = reverse_lazy('shops:inquiry')

  def form_valid(self,form):
    form.send_email()
    messages.success(self.request,'メッセージを送信しました。')
    logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
    return super().form_valid(form)

class ShopsListView(LoginRequiredMixin,generic.ListView):
  model = Shops
  template_name = 'shops_list.html'
  paginate_by = 2

  def get_queryset(self):
    shopper = Shops.objects.filter(user=self.request.user).order_by('-created_at')
    return shopper

class ShopsDetailView(LoginRequiredMixin,generic.DetailView):
  model = Shops
  template_name = 'shops_detail.html'

class ShopsCreateView(LoginRequiredMixin,generic.CreateView):
  model =Shops
  template_name = 'shops_create.html'
  form_class = ShopsCreateForm
  success_url = reverse_lazy('shops:shops_list')

  def form_valid(self,form):
    shops = form.save(commit=False)
    shops.user =self.request.user
    shops.save()
    messages.success(self.request,'お気に入りのお店を追加しました。')
    return super().form_valid(form)

  def form_invalid(self,form):
    messages.error(self.request,'お店の追加に失敗しました。')
    return super().form_invalid(form)

class ShopsUpdateView(LoginRequiredMixin,generic.UpdateView):
  model = Shops
  template_name = 'shops_update.html'
  form_class = ShopsCreateForm

  def get_success_url(self):
    return reverse_lazy('shops:shops_detail',kwargs={'pk':self.kwargs['pk']})

  def form_valid(self,form):
    messages.success(self.request,'更新しました。')
    return super().form_valid(form)

  def form_invalid(self,form):
    messages.error(self.request,'更新に失敗しました。')
    return super().form_invalid(form)

class ShopsDeleteView(LoginRequiredMixin,generic.DeleteView):
  model = Shops
  template_name ='shops_delete.html'
  success_url = reverse_lazy('shops:shops_list')

  def delete(self,request,*args,**kwargs):
    messages.success(self.request,"削除しました。")
    return super().delete(request,*args,**kwargs)