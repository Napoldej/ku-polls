from django.shortcuts import get_object_or_404,render,redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages



# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by("-pub_date")[:5]
    
    
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    def get(self,request, *args, **kwargs):
        try:
            self.object = get_object_or_404(Question, pk = kwargs['pk'])
        except Http404:
            messages.error(request,f"Poll number with ID {kwargs['pk']} is not available")
            return redirect("polls:index")
        
        
        if(not self.object.can_vote()):
            messages.error(request, f"Poll number {self.object.pk} has ended, which is not allow for voting.")
            return redirect("polls:index")
        
        if(not self.object.is_published()):
            messages.error(request, f"Polls number {self.object.pk} is not available")
            return redirect("polls: index")

        return render(request,"polls/detail.html",{"question": self.object})
    
       
            
            

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if(not question.can_vote()):
        messages.error(request, "Poll number {question.id} is not available to vote")
        HttpResponseRedirect(reverse('polls:index'))
        
    else:
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            messages.error(request,"You didn't select the choice.")
            return render(request, 'polls/detail.html', {
                'question': question,
            })
        else:
            selected_choice.vote += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        
        