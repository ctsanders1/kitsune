# Ported from mozilla/django-badger
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_http_methods
from django.views.generic.list import ListView

from kitsune.kbadge import BADGER_BADGE_PAGE_SIZE, BADGER_MAX_RECENT, BADGER_TEMPLATE_BASE
from kitsune.kbadge.forms import BadgeAwardForm
from kitsune.kbadge.models import Award, Badge


class BadgesListView(ListView):
    """Badges list page"""
    model = Badge
    template_name = '%s/badges_list.html' % BADGER_TEMPLATE_BASE
    template_object_name = 'badge'
    paginate_by = BADGER_BADGE_PAGE_SIZE

    def get_queryset(self):
        qs = Badge.objects.order_by('-modified')
        query_string = self.request.GET.get('q', None)

        if query_string is not None:
            sort_order = self.request.GET.get('sort', 'created')
            qs = Badge.objects.search(query_string, sort_order)

        return qs

    def get_context_data(self, **kwargs):
        context = super(BadgesListView, self).get_context_data(**kwargs)
        context['award_list'] = None
        context['tag_name'] = self.kwargs.get('tag_name', None)
        context['query_string'] = kwargs.get('q', None)
        if context['query_string'] is not None:
            # TODO: Is this the most efficient query?
            context['award_list'] = (Award.objects.filter(badge__in=self.get_queryset()))
        return context


badges_list = BadgesListView.as_view()


@require_http_methods(['HEAD', 'GET', 'POST'])
def detail(request, slug, format="html"):
    """Badge detail view"""
    badge = get_object_or_404(Badge, slug=slug)
    if not badge.allows_detail_by(request.user):
        return HttpResponseForbidden('Detail forbidden')

    awards = (Award.objects.filter(badge=badge)
                           .order_by('-created'))[:BADGER_MAX_RECENT]

    # FIXME: This is awkward. It used to collect sections as responses to a
    # signal sent out to badger_multiplayer and hypothetical future expansions
    # to badger
    sections = dict()
    sections['award'] = dict(form=BadgeAwardForm())

    if request.method == "POST":
        url = reverse('kbadge.views.detail', kwargs=dict(slug=slug))
        return HttpResponseRedirect(url)

    return render(request, '%s/badge_detail.html' % BADGER_TEMPLATE_BASE, dict(
        badge=badge, award_list=awards, sections=sections
    ))


class AwardsListView(ListView):
    model = Award
    template_name = '%s/awards_list.html' % BADGER_TEMPLATE_BASE
    template_object_name = 'award'
    paginate_by = BADGER_BADGE_PAGE_SIZE

    def get_badge(self):
        if not hasattr(self, 'badge'):
            self._badge = get_object_or_404(Badge, slug=self.kwargs.get('slug', None))
        return self._badge

    def get_queryset(self):
        qs = Award.objects.order_by('-modified')
        if self.kwargs.get('slug', None) is not None:
            qs = qs.filter(badge=self.get_badge())
        return qs

    def get_context_data(self, **kwargs):
        context = super(AwardsListView, self).get_context_data(**kwargs)
        if self.kwargs.get('slug', None) is None:
            context['badge'] = None
        else:
            context['badge'] = self.get_badge()
        return context


awards_list = AwardsListView.as_view()


@require_http_methods(['HEAD', 'GET'])
def award_detail(request, slug, id, format="html"):
    """Award detail view"""
    badge = get_object_or_404(Badge, slug=slug)
    award = get_object_or_404(Award, badge=badge, pk=id)

    if not award.allows_detail_by(request.user):
        return HttpResponseForbidden('Award detail forbidden')

    return render(request, '%s/award_detail.html' % BADGER_TEMPLATE_BASE, dict(
        badge=badge, award=award,
    ))


@require_GET
def awards_by_user(request, username):
    """Badge awards by user"""
    user = get_object_or_404(User, username=username)
    awards = Award.objects.filter(user=user)
    return render(request, '%s/awards_by_user.html' % BADGER_TEMPLATE_BASE, dict(
        user=user, award_list=awards,
    ))


@require_GET
def awards_by_badge(request, slug):
    """Badge awards by badge"""
    badge = get_object_or_404(Badge, slug=slug)
    awards = Award.objects.filter(badge=badge)
    return render(request, '%s/awards_by_badge.html' % BADGER_TEMPLATE_BASE, dict(
        badge=badge, awards=awards,
    ))


@require_GET
def badges_by_user(request, username):
    """Badges created by user"""
    user = get_object_or_404(User, username=username)
    badges = Badge.objects.filter(creator=user)
    return render(request, '%s/badges_by_user.html' % BADGER_TEMPLATE_BASE, dict(
        user=user, badge_list=badges,
    ))
