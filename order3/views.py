from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.core.exceptions import *
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from account.views import serializeUser
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from comment.models import *

# Create your views here.

userSerializer = serializeUser()


def orderStatusUpdate():
    for order_obj in order3.objects.all():
        if order_obj.expireDateTime < timezone.now():
            order_obj.order_status = order3.expired
            order_obj.save()


def search(request):
    # 不验证是否登录
    # search也不一定需要 搜索的关键字可以是快递商种类，地址
    # 每次返回10个订单
    orderStatusUpdate()  # 更新数据库状态
    search = request.GET.get("search", "")
    goods_category=request.GET.get("goods_category","")
    print("search:" + search)
    page = request.GET.get("page", "")
    try:
        page = int(page)
    except ValueError as e:
        print(e)
        return JsonResponse({"msg": "page字段有问题"}, status=404)

    results = order3.objects.filter(order_status=order3.uncompleted, free_lancer=None,goods_category=goods_category).values(
        *["orderid", "createTime", "money", "received_pos",  "campus", "expireDateTime",
          "goods_introduction", "goods_category", "goods_img"])
    print(len(results))
    results = [_ for _ in results if search in _["received_pos"] ]

    orderByTime = request.GET.get("orderByTime", '')
    orderByPrice = request.GET.get("orderByPrice", '')

    if orderByTime:
        results.sort(key=lambda x: x['createTime'], reverse=True)
    if orderByTime == "-1":  # 时间最长的订单
        results.reverse()
    print(orderByTime)
    print(orderByPrice)
    if orderByPrice:
        results.sort(key=lambda x: x['money'], reverse=True)

    if orderByPrice == "-1":  # 价钱最小的订单
        results.reverse()

    if page < 1:
        page = 1
    results = results[10 * page - 10:10 * page]

    return JsonResponse({'results': results}, safe=False)


def getOrder(request):  # 获得某个订单的具体信息
    # 还有一种是已经登录，并且是自己的订单
    openid = request.session.get("openid", "")
    user_exists = True
    try:
        cur_user = user.objects.get(openid=openid)
    except user.DoesNotExist as e:
        user_exists = False

    orderid = request.GET.get("orderid")
    if not orderid:
        return JsonResponse({"msg": "orderid字段不存在"}, status=404)

    ret_order = ""
    try:
        ret_order = order3.objects.get(orderid=orderid)
    except order3.DoesNotExist:
        ret_order = ""

    if not ret_order:
        return JsonResponse({"msg": "orderid" + orderid + "用户不存在"})
    ret_keys = ["orderid","createTime", "expireDateTime", "order_owner", "money",
                "order_status", "goods_introduction", "goods_category","goods_weight","pos" ]
    if user_exists and (ret_order.free_lancer == cur_user or ret_order.order_owner == cur_user):
        ret_keys.append(["hidden_info", "free_lancer", "recieved_pos"])

    ret_values = {}

    fields = ("wx_name", "openid", "head_img")
    for key in ret_keys:
        value = getattr(ret_order, key)
        if type(value) == type(user()):
            serializedValue = userSerializer.default(value, *fields)
            # print("serializedValue:",serializedValue)
            ret_values[key] = serializedValue
        else:
            ret_values[key] = value
    print(ret_values)
    return JsonResponse({"order3": ret_values}, safe=False)


@csrf_exempt
def sendOrder(request):
    if request.method == 'POST':
        openid = request.session.get("openid")
        print("openid", openid)
        cur_user = get_object_or_404(user, openid=openid)
        #hidden_info = request.POST.get("hidden_info", "")
        orderid = request.POST.get('orderid', "")
        expireTime = request.POST.get("expireTime", "")
        money = request.POST.get('money', "")
        #kuaidi = request.POST.get("kuaidi", "")
        goods_introduction=request.POST.get("goods_introduction", "")
        #goods_img=request.POST.get("goods_img", "")
        goods_category=request.POST.get("goods_category", "")
        campus=request.POST.get("xiaoqu", "")
        received_pos = request.POST.get('received_pos', "")
        goods_weight = request.POST.get('goods_weight', "")
        #goods_img=request.POST.get('goods_img', "")
        try:
            expireTime = int(expireTime)
            # money = float(expireTime)
        except ValueError as e:
            print(e)
            print("expireTime", expireTime)
            return JsonResponse({"msg": "字段有错误"}, status=404)
        try:
            cur_order = order3.objects.get(orderid=orderid)
            return JsonResponse({"msg": "订单id重复"}, status=404)
        except:
            pass
        if not cur_user or not goods_introduction or not goods_weight or not money or not received_pos :
            return JsonResponse({"msg": "字段不全"}, status=404)
            #or not expireTime  or not kuaidi
        else:
            if cur_user.sended_order_count <= 0:
                return JsonResponse({"msg": "你已有10个订单，到达额度"}, status=404)

            cur_user.sended_order_count -= 1

            newOrder = order3()
            #print(orderid, order.uncompleted, cur_user, hidden_info, timezone.now() + timedelta(hours=expireTime),
             #   money, kuaidi, received_pos)
            newOrder.order_status = order3.uncompleted
            newOrder.order_owner = cur_user
            newOrder.goods_introduction = goods_introduction
            newOrder.expireDateTime = timezone.now() + timedelta(hours=expireTime)
            newOrder.money = money
            #newOrder.kuaidi = kuaidi
            newOrder.received_pos = received_pos
            newOrder.campus=campus
            newOrder.goods_category=goods_category
            # newOrder.goods_introduction=goods_introduction
            # newOrder.goods_img=goods_img
            newOrder.goods_weight = goods_weight
            newOrder.save()
            cur_user.save()
            return JsonResponse({"msg": "创建订单成功"})
    else:
        return JsonResponse({"msg": "请使用post"}, status=406)  # not acceptable


def receiveOrder(request):
    # 需要登录
    """
    :param request:
    :param orderid:
    :return:
    """
    openid = request.session.get("openid")
    orderid = request.GET.get("orderid")
    cur_user = get_object_or_404(user, openid=openid)
    cur_order = get_object_or_404(order3, orderid=orderid)
    # if not cur_user.phone:
    #     return JsonResponse({"msg":"请绑定手机号"},status=404)
    if cur_user.received_order_count <= 0:
        return JsonResponse({"msg": "你已有10个订单"}, status=404)
    elif cur_user.status == user.banned:
        return JsonResponse({"msg": "被禁止用户"}, status=404)
    elif not cur_user.studentId or not cur_user.stuIdPwd:
        return JsonResponse({"msg": "未绑定学号"}, status=404)
    elif cur_order.free_lancer:
        return JsonResponse({"msg": "该订单已经有人领单"}, status=404)
    else:
        cur_order.order_status = order3.completing
        cur_order.free_lancer = cur_user
        cur_user.received_order_count -= 1
        cur_order.save()
        cur_user.save()
        return JsonResponse({"msg": "领取订单成功"})


def cancelOrder(request):
    openid = request.session.get("openid", "")
    orderid = request.GET.get("orderid", "")
    cur_user = get_object_or_404(user, openid=openid)
    cur_order = get_object_or_404(order3, orderid=orderid)
    if cur_order.order_owner == cur_user:
        if cur_order.order_status == order3.canceled:
            return JsonResponse({"msg": "订单早已取消"}, status=404)
        elif cur_order.order_status != order3.uncompleted|order3.completing:
            return JsonResponse({"msg": "订单已完成或过期不能取消"}, status=404)
        cur_order.order_status = order3.canceled
        cur_user.sended_order_count += 1
        lancer_user = cur_order.free_lancer
        if lancer_user:
            lancer_user.received_order_count += 1
            lancer_user.save()
        cur_user.save()
        cur_order.save()
        return JsonResponse({"msg": "取消成功请重新发起订单"})
    if cur_order.free_lancer == cur_user:
        return JsonResponse({"msg": "请联系订单主人协商后由主人取消"}, status=404)

    return JsonResponse({"msg": "你无权取消"}, status=404)


def calRate(cur_user: user):
    owner_orders = order3.objects.filter(order_owner=cur_user)
    lancer_orders = order3.objects.filter(free_lancer=cur_user)
    orders_count = len(owner_orders) + len(lancer_orders)

    rateSum = 0
    count = 0
    for orderObj in owner_orders:
        try:
            commentObj = comment.objects.get(order3=orderObj)
            if commentObj.lancer_commented:
                rateSum += commentObj.lancer_star
                count += 1
        except ObjectDoesNotExist:
            continue
    for orderObj in lancer_orders:
        try:
            commentObj = comment.objects.get(order=orderObj)
            if commentObj.owner_commented:
                rateSum += commentObj.owner_star
                count += 1
        except ObjectDoesNotExist:
            continue
    try:
        rate = rateSum / count
    except ZeroDivisionError:
        rate = 5.0
    cur_user.rate = rate
    cur_user.save()
    return rate


def orderComplete(request):
    openid = request.session.get("openid", "")
    orderid = request.GET.get("orderid", "")
    cur_user = get_object_or_404(user, openid=openid)
    cur_order = get_object_or_404(order3, orderid=orderid)
    if cur_order.order_owner == cur_user:
        if cur_order.order_status == order3.completed:
            return JsonResponse({"msg": "订单早已完成"}, status=404)
        elif cur_order.order_status != order3.completing:
            return JsonResponse({"msg": "订单已取消或过期不能完成"}, status=404)
        cur_order.order_status = order3.uncommented
        cur_order.save()
        cur_user.sended_order_count += 1
        lancer_user = cur_order.free_lancer
        lancer_user.received_order_count += 1

        cur_user.save()
        lancer_user.save()
        return JsonResponse({"msg": "完成订单确认成功"})
    if cur_order.free_lancer == cur_user:
        return JsonResponse({"msg": "请联系订单主人后由主人确认"}, status=404)

    return JsonResponse({"msg": "你无权确认完成订单"}, status=404)

