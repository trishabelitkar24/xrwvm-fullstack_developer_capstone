urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # Home page
    path('', TemplateView.as_view(template_name="Home.html")),

    # About and Contact pages
    path('about', TemplateView.as_view(template_name="About.html")),
    path('contact', TemplateView.as_view(template_name="Contact.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
