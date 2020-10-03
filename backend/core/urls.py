from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, re_path

app_name = 'core'


# urlpatterns = [
# 	path("search/", views.SearchSubscriptionsView.as_view()),
# ]
#
# router = DefaultRouter()
# router.register('users', views.UserViewSet, basename='users')
# router.register('team-members', views.TeamMemberViewSet, basename='team-members')
# router.register('team-form', views.TeamFormViewSet, basename='team-form')
# router.register('contact-us', views.ContactUsViewSet, basename='contactus')
# router.register('feedbacks', views.FeedbackViewSet, basename='feedback')
# router.register('faqs', views.FAQViewSet, basename='faqs')
# router.register('articles', views.ArticleViewSet, basename='articles')
# router.register('news', views.NewsViewSet, basename='news')
# router.register('newsletter', views.NewsletterViewSet, basename='newsletter')
#
# router.register('categories', views.CategoryViewSet, basename='category')
# router.register('sub-categories', views.SubCategoryViewSet, basename='sub-category')
# router.register('pdfs', views.PDFSerializer, basename='pdf')
# router.register('mcqs', views.MCQSerializer, basename='mcq')
# router.register('summaries', views.SummarySerializer, basename='summary')
# router.register('sessions', views.SessionSerializer, basename='session')
# router.register('user-subscriptions', views.UserSubscriptionsSerializer, basename='user-subscription')






# urlpatterns += router.urls
