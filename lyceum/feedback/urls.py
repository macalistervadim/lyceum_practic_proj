import django.urls

import feedback.views

app_name = "feedback"

urlpatterns = [
    django.urls.path(
        "",
        feedback.views.FeedbackView.as_view(),
        name="feedback",
    ),
]
