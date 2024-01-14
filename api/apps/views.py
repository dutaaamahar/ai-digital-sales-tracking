from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.functions.features import tracking_per_sales_staff

def build_result(result):
    # Build a standard result dictionary for success
    result = {
        "status": 200,
        "message": "success",
        "result": result
    }

    # Return the result dictionary
    return result

class TrackingPerSalesStaff(APIView):
    def post(self, request):
        try:
            # Call the tracking_per_sales_staff function with the data from the request
            result = tracking_per_sales_staff(request.data)

            # Build the response using the build_result function (assuming it's defined)
            response_data = build_result(result)

            # Return the response with a 200 status code
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            # If an exception occurs, capture the error message and return a 400 status code
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
