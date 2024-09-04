from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect
from .models import Question, Choice, Vote
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages


# Create your views here.
class IndexView(generic.ListView):
    """
    View to display the list of the most recent questions.
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Returns the last five published questions (excluding future questions).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()) \
                               .order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """
    Display the contents of a specific question and allow voting.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to display the details of a specific question.

        Args:
            request (HttpRequest): The request object.
            *args: Variable length argument list.
            **kwargs: Keyword arguments
            ,including the primary key of the question.

        Returns:
            HttpResponse: The rendered response with question details.
        """
        try:
            self.object = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            messages.error(
                request,
                f"Poll number with ID {kwargs['pk']} is not available"
            )
            return redirect("polls:index")

        if not self.object.can_vote():
            messages.error(
                request,
                f"Poll number {self.object.pk} has ended, which is not allowed for voting."
            )
            return redirect("polls:index")

        if not self.object.is_published():
            messages.error(
                request,
                f"Poll number {self.object.pk} is not available"
            )
            return redirect("polls:index")

        return render(request, "polls/detail.html", {"question": self.object})


class ResultsView(generic.DetailView):
    """
    View to display the results of a specific question.
    """
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """
    Handles voting for a specific question.

    Args:
        request (HttpRequest): The request object.
        question_id (int): The ID of the question being voted on.

    Returns:
        HttpResponse: Redirect to the results page 
        or re-render voting form with an error message.
    """
    question = get_object_or_404(Question, pk=question_id)

    if not question.can_vote():
        messages.error(
            request,
            f"Poll number {question.id} is not available to vote"
        )
        return HttpResponseRedirect(reverse('polls:index'))

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't select a choice.")
        return render(request, 'polls/detail.html', {
            'question': question,
        })
    # Reference to the current user.
    this_user = request.user
    try:
        vote = this_user.vote_set.get(user= this_user, choice=selected_choice)
        vote.choice = selected_choice
        vote.save()
        messages.success(request,f"Your vote for {selected_choice} has been recorded.")
    except Vote.DoesNotExist:
        vote = Vote.objects.create(user=this_user, choice=selected_choice)
        vote.save()
        messages.success(request,f"Your vote for {selected_choice} has been recorded.")

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
