import django.db
import django.http
import django.shortcuts
import django.utils
import django.utils.translation as translation
import django.views.generic

import catalog.models
import rating.forms
import rating.models as rating_models


class RatingMixin:
    def get_rating_info(self, item):
        ratings_query = rating_models.Rating.objects.filter(item=item)

        ratings_query_annotated = ratings_query.annotate(
            avg_rating=django.db.models.Avg("value"),
            total_ratings=django.db.models.Count("value"),
        )

        ratings = ratings_query_annotated.first()

        if self.request.user.is_authenticated:
            user_rating = rating_models.Rating.objects.filter(
                item=item,
                user=self.request.user,
            ).first()

        if ratings:
            return (
                ratings.avg_rating,
                ratings.total_ratings,
                user_rating,
            )

        return None, 0, None


class ItemList(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"

    def get_queryset(self):
        return catalog.models.Item.objects.published()


class NewItems(django.views.generic.ListView):
    template_name = "catalog/item_filter_date.html"
    context_object_name = "items"
    extra_context = {"view_type": "new_items"}

    def get_queryset(self):
        return catalog.models.Item.objects.new_items()


class FridayItems(django.views.generic.ListView):
    template_name = "catalog/item_filter_date.html"
    context_object_name = "items"
    extra_context = {"view_type": "friday_items"}

    def get_queryset(self):
        return catalog.models.Item.objects.friday_items()


class UnverifiedItems(django.views.generic.ListView):
    tempalte_name = "catalog/item_filter_date.html"
    extra_context = {"view_type": "unverified_items"}
    context_object_name = "items"

    def get_queryset(self):
        return catalog.models.Item.objects.unverified_items()


class ItemDetail(RatingMixin, django.views.generic.DetailView):
    template_name = "catalog/item.html"
    context_object_name = "item"
    form_class = rating.forms.RatingForm

    def get_queryset(self):
        return catalog.models.Item.objects.gallery_images()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object

        average_rating, total_ratings, user_rating = self.get_rating_info(item)
        context["average_rating"] = average_rating
        context["total_ratings"] = total_ratings
        context["user_rating"] = user_rating
        context["rating_form"] = self.form_class(initial={"item": item})

        return context

    def post(self, request, *args, **kwargs):
        item = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            user_rating, created = rating_models.Rating.objects.get_or_create(
                user=request.user,
                item=item,
                defaults={"value": form.cleaned_data["value"]},
            )
            if not created:
                user_rating.value = form.cleaned_data["value"]
                user_rating.save()

            django.contrib.messages.success(
                request,
                translation.gettext_lazy("Вы поставили оценку"),
            )

            return django.shortcuts.redirect("catalog:item-detail", pk=item.pk)

        return super().post(request, *args, **kwargs)


class RatingDeleteView(django.views.View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get("item_id")
        user = request.user

        ratings = rating_models.Rating.objects.get(item_id=item_id, user=user)
        ratings.delete()
        django.contrib.messages.success(
            request,
            translation.gettext_lazy("Оценка удалена"),
        )
        return django.shortcuts.redirect("catalog:item-detail", pk=item_id)


__all__ = []
