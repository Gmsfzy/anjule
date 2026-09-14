# 模拟第三方支付接口
def mock_payment_api(house_id, amount, payment_type):
    """
    模拟支付接口返回结果
    :param house_id: 房屋ID
    :param amount: 支付金额
    :param payment_type: 支付类型
    :return: 模拟返回字典
    """
    return {
        "code": 200,
        "msg": "支付成功",
        "data": {
            "order_id": f"PAY{house_id}{int(amount*100)}",
            "house_id": house_id,
            "amount": amount,
            "payment_type": payment_type,
            "status": "success",
            "timestamp": "2025-12-17 15:00:00"
        }
    }

# 模拟第三方门禁接口
def mock_access_api(house_id, user_id):
    """
    模拟门禁接口返回结果
    :param house_id: 房屋ID
    :param user_id: 用户ID
    :return: 模拟返回字典
    """
    return {
        "code": 200,
        "msg": "门禁授权成功",
        "data": {
            "access_id": f"ACC{house_id}{user_id}",
            "house_id": house_id,
            "user_id": user_id,
            "status": "authorized",
            "expire_time": "2025-12-31 23:59:59"
        }
    }