from datetime import date

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from ..models import WinEntry
from ..serializers import WinEntrySerializer


class WinEntryList(APIView):
    """
    List all target entries or create a new target entry
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, date_request, format=None):
        """
        List all target entries or filter by date
        """
        return self._handle_target_list_action(request, date_request)

    def post(self, request, date_request, format=None):
        """
        Create a new target entry
        """
        return self._handle_target_list_action(request, date_request)

    def _handle_target_list_action(self, request, date_request):
        """
        Private helper method to handle both GET and POST requests

        Check if request is allowed based on the date and either
        lists all target entries or creates a new target entry
        """
        if request.method == "GET":
            if date_request is not None:
                try:
                    requested_date = date.fromisoformat(date_request)
                except ValueError:
                    return Response(
                        {
                            "error":
                            "Invalid date format. Please user YYYY-MM-DD."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                target_entries = WinEntry.objects.filter(
                    created_on__date=requested_date)
            else:
                target_entries = WinEntry.objects.all()

            serializer = WinEntrySerializer(
                target_entries, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            current_date = date.today().strftime("%Y-%m-%d")
            if date_request != current_date:
                return Response(
                    {
                        "error":
                        "You are not allowed to change targets \
                            for past or future dates."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = WinEntrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        raise MethodNotAllowed(request.method)


class WinEntryDetail(APIView):
    """
    Retrieve, update or delete an target entry
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get an target entry object from the database
        or raise a 404 error
        """
        try:
            return WinEntry.objects.get(pk=pk)
        except WinEntry.DoesNotExist:
            raise Http404

    def get(self, request, date_request, pk, format=None):
        """
        Retrieve an target entry
        """
        return self._handle_target_detail_action(request, date_request, pk)

    def put(self, request, date_request, pk, format=None):
        """
        Update an target entry
        """
        return self._handle_target_detail_action(request, date_request, pk)

    def delete(self, request, date_request, pk, format=None):
        """
        Delete an target entry
        """
        return self._handle_target_detail_action(request, date_request, pk)

    def _handle_target_detail_action(self, request, date_request, pk):
        """
        Private helper method to handle GET, PUT and DELETE requests

        Check if request is allowed based on date and
        either retrieve, update or delete an target entry
        """
        current_date = date.today().strftime("%Y-%m-%d")
        if date_request != current_date:
            return Response(
                {
                    "error":
                    "You are not allowed to change targets \
                        for past or future dates."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if pk is not None:
            try:
                target_id = isinstance(pk, int)
                target_entry = self.get_object(pk)
            except (ValueError, Http404):
                if isinstance(pk, str):
                    return Response(
                        {"error": "Invalid target ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(status=status.HTTP_404_NOT_FOUND)

            if request.method == "GET":
                serializer = WinEntrySerializer(target_entry)
                return Response(serializer.data)

            elif request.method == "PUT":
                serializer = WinEntrySerializer(
                    target_entry, data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response(serializer.data)
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            elif request.method == "DELETE":
                target_entry.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
