import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.signals import (user_logged_in,
                                         user_logged_out, user_login_failed)
from django.dispatch import receiver
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Question, Choice, Vote


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    return ip_address


@receiver(user_login_failed)
def log_user_login_failed(request, credentials, **kwargs):
    """
    Get the signal, when user failed login.
    """
    logger = logging.getLogger("polls")
    ip = get_client_ip(request)
    username = credentials.get('username', None)
    logger.warning(f"Failed login for {username} from {ip}")


@receiver(user_logged_in)
def log_user_login(request, user, **kwargs):
    """
    Get the signal, when user logged in.
    """
    logger = logging.getLogger("polls")
    ip_address = get_client_ip(request)
    logger.info(f'User "{user.username}" logged in from IP {ip_address}.')


@receiver(user_logged_out)
def log_user_logout(request, user, **kwargs):
    """
    Get the signal, when user logged out.
    """
    logger = logging.getLogger("polls")
    ip_address = get_client_ip(request)
    logger.info(f'User "{user.username}" logged out from IP {ip_address}.')


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

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.
        """
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        vote = None
        if self.request.user.is_authenticated:
            try:
                vote = Vote.objects.get(user=self.request.user,
                                        choice__question=self.object)
            except Vote.DoesNotExist:
                vote = None
        context["vote"] = vote
        return context

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to display the details of a specific question.

        Args:
            request (HttpRequest): The request object.
            *args: Variable length argument list.
            **kwargs: Keyword arguments including,
            the primary key of the question.

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
            logging.error(f"This question {self.object.pk} does not exist")
            return redirect("polls:index")

        if not self.object.can_vote():
            messages.error(
                request,
                f"Poll number {self.object.pk} has ended, "
                f"which is not allowed for voting."
            )
            return redirect("polls:index")

        if not self.object.is_published():
            messages.error(
                request,
                f"Poll number {self.object.pk} is not available"
            )
            return redirect("polls:index")

        if self.request.user.is_authenticated:
            context = self.get_context_data()
            return render(request, "polls/detail.html", context=context)

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
    this_user = request.user
    logger = logging.getLogger(__name__)
    ip_address = get_client_ip(request)
    logger.info(f"{this_user} log in from {ip_address}")

    # The question has ended already
    if not question.can_vote():
        messages.error(
            request,
            f"Poll number {question.id} is not available to vote"
        )
        logger.warning("This question is not yet voted")
        return HttpResponseRedirect(reverse('polls:index'))

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't select a choice.")
        logger.warning(f"{this_user} didn't select a choice "
                       f"from {ip_address}.")
        return render(request, 'polls/detail.html', {
            'question': question,
        })

    vote_for_poll(request, question.id, logger, selected_choice, this_user)
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def vote_for_poll(request, question_id, logger, selected_choice, this_user):
    """
    Handles voting for a specific question.
    """
    choice_id = request.POST['choice']
    question = get_object_or_404(Question, pk=question_id)
    if not choice_id:
        # no choice_id was set
        messages.error(request, "You didn't make a choice")
        return redirect('polls:detail', question_id)
    try:
        vote = this_user.vote_set.get(user=this_user,
                                      choice__question=question)
        vote.choice = selected_choice
        vote.save()
        messages.success(request, f"Your vote for {selected_choice} "
                                  f"has been recorded.")
        logger.info(f"{this_user.username} has voted for {question.id} "
                    f"with {choice_id}")
    except Vote.DoesNotExist:
        vote = Vote.objects.create(user=this_user, choice=selected_choice)
        vote.save()
        messages.success(request, f"Your vote for {selected_choice} "
                                  f"has been recorded.")
        logger.info(f"{this_user.username} has voted for {question.id} "
                    f"with {choice_id}")
    return redirect('polls:results', question_id)
