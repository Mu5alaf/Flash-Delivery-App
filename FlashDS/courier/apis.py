from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from FlashDS.models import *
# ----------------------------------------------------------------


@csrf_exempt
@login_required(login_url="courier/sign-in/")
def available_task_api(request):
    # gating value inside list
    tasks = list(Request.objects.filter(
        status=Request.PROCESSING_STATUS).values())
    return JsonResponse({
        "tasks": tasks,
        "success": True,
    })
# ----------------------------------------------------------------
@csrf_exempt
@login_required(login_url="courier/sign-in/")
def current_task_update_api(request, id):
    try:
        # Ensure the request method is POST
        if request.method == 'POST':
            task = Request.objects.filter(
                id=id,
                courier=request.user.courier,
                status__in=[
                    Request.PICKING_STATUS,
                    Request.DELIVERING_STATUS,
                ]
            ).last()

            if task and task.status == Request.PICKING_STATUS:
                task.pickup_picture = request.FILES['pickup_picture']
                task.pickup_Time = timezone.now()
                task.status = Request.DELIVERING_STATUS
                task.save()
                return JsonResponse({"success": True})
            elif task and task.status == Request.DELIVERING_STATUS:
                task.delivery_picture = request.FILES['delivery_picture']
                task.delivered_Time = timezone.now()
                task.status = Request.COMPLETED_STATUS
                task.save()
                return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

    # Return a generic failure response if no other condition is met
    return JsonResponse({"success": False, "error": "Invalid request"})
# ----------------------------------------------------------------
@csrf_exempt
@login_required(login_url="courier/sign-in/")
def fcm_token_upgrade_api(request):
    request.user.courier.fcm_token = request.GET.get('fcm_token')
    request.user.courier.save()
    return JsonResponse({
        "success":True
    })