
from django.conf import settings
from django.core.management.commands.runserver import Command as Runserver
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.views.static import serve


class MezzStaticFilesHandler(StaticFilesHandler):

    def get_response(self, request):
        if request.path.startswith(settings.MEDIA_URL):
            path = self.file_path(request.path)
            return serve(request, path, document_root=settings.STATIC_ROOT)
        return super(MezzStaticFilesHandler, self).get_response(request)


class Command(Runserver):
    """
    Overrides runserver so that we can serve uploaded files
    during development, and not require every single developer on
    every single one of their projects to have to set up multiple
    web server aliases for serving static content.
    See https://code.djangoproject.com/ticket/15199
    """

    def get_handler(self, *args, **options):
        handler = super(Command, self).get_handler(*args, **options)
        if settings.DEBUG:
            return MezzStaticFilesHandler(handler)
        return handler
