from app.db.models import User  # misol uchun
import math
import aiohttp

from sqlalchemy import func
from sqlalchemy import select
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


from app.db.crud import get_user
from app.db.models import SalesReport
from app.db.session import async_session
from app.services.uzum_report import UzumAPIService


async def get_shops(token: str):
    url = 'https://api-seller.uzum.uz/api/seller-openapi/v1/shops'
    headers = {'Authorization': token, 'accept': '*/*'}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                return False


async def update_reports(user_id, status):
    user = await get_user(user_id)
    last_recorded_date = await get_latest_sale_date(user_id)
    now = datetime.now(ZoneInfo(user.timezone))

    if not last_recorded_date:
        from_date = datetime(2000, 1, 1)
        last_recorded_date = from_date
    else:
        from_date = last_recorded_date-timedelta(days=5)

    sales_period = {
        "from": date_to_ms(from_date),
        "to": date_to_ms(now)
    }

    async with UzumAPIService(status, sales_period, user) as service:
        return await service.update_data(last_recorded_date)


async def get_latest_sale_date(user_id: int):
    async with async_session() as session:
        stmt = select(func.max(SalesReport.date)).where(
            SalesReport.user_id == user_id)
        result = await session.execute(stmt)
        date = result.scalar()
        return date


def date_to_ms(date_input) -> int:
    if isinstance(date_input, str):
        try:
            dt = datetime.strptime(date_input.strip(), "%d.%m.%Y %H:%M:%S")
        except ValueError:
            dt = datetime.strptime(date_input.strip(), "%d.%m.%Y %H:%M")
    elif isinstance(date_input, datetime):
        dt = date_input
    else:
        raise ValueError("date_input should be str or datetime")
    return int(dt.timestamp() * 1000)


def ms_to_date(ms):
    return datetime.fromtimestamp(ms / 1000)


def format_date(date_input):
    if isinstance(date_input, str):
        dt = datetime.strptime(date_input.strip(), "%d.%m.%Y %H:%M")
    elif isinstance(date_input, datetime):
        dt = date_input
    else:
        raise ValueError("date_input should be str or datetime")
    return dt.strftime("%d.%m.%Y %H:%M")


def format_analytics_msg(report):
    res = report["metrics"]
    inv = report["inventory"]

    def format_val(val: dict, suffix="UZS", is_percent=False):
        if not val or "now" not in val:
            return "0 UZS ✅ 0%"

        now = val.get("now", 0)
        diff = val.get("diff", 0)
        percent = val.get("percent", 0)

        if now is None or math.isnan(now) if isinstance(now, float) else False:
            now = 0
        if diff is None or math.isnan(diff) if isinstance(diff, float) else False:
            diff = 0
        if percent is None or math.isnan(percent) if isinstance(percent, float) else False:
            percent = 0

        arrow = "✅" if diff >= 0 else "❗"

        if is_percent:
            symbol = f"{now:.1f}%"
        else:
            symbol = f"{now:,.0f}" if abs(now) >= 1 else f"{now:.1f}"

        percent_str = f"{percent:+.1f}%" if percent != 0 else "0%"

        return f"{symbol} {suffix if not is_percent else ''} {arrow} {percent_str}"

    def format_date(d: str) -> str:
        try:
            return datetime.strptime(d, "%d.%m.%Y %H:%M:%S").strftime("%d.%m %H:%M")
        except:
            return d

    def safe_number(value, decimal_places=0):
        if value is None:
            return 0
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return 0

        if decimal_places == 0:
            return int(value)
        else:
            return round(float(value), decimal_places)

    # Hisobot matnini yaratish
    msg = "*📊 Ежемесячный отчет*\n\n"

    # Finanslar bo'limi
    msg += "💰 *Финансы*\n"
    msg += f"• Выручка: {format_val(res.get('revenue', {}))}\n"
    msg += f"• Себестоимость: {format_val(res.get('cost_price', {}))}\n"
    msg += f"• Комиссия: {format_val(res.get('commission', {}))}\n"
    msg += f"• Логистика: {format_val(res.get('logistic_fee', 0))}\n"
    msg += f"• Чистая прибыль: {format_val(res.get('net_profit', {}))}\n"
    msg += f"• Рентабельность: {format_val(res.get('profitability', {}), suffix='%', is_percent=True)}\n\n"

    # Buyurtmalar bo'limi
    msg += "📦 *Заказы*\n"
    msg += f"• Кол-во прод. тов.: {format_val(res.get('quantity', {}), suffix='шт')}\n"
    msg += f"• Кол-во заказов: {format_val(res.get('order_count', {}), suffix='шт')}\n"
    msg += f"• Ср. чек: {format_val(res.get('avg_check', {}))}\n"
    msg += f"• Кол-во отказов: {format_val(res.get('cancelled_orders', {}), suffix='шт')}\n\n"

    # Inventar bo'limi
    msg += "📈 *Инвентарь*\n"
    msg += f"• Ср. цена: {safe_number(inv.get('avg_price', 0)):,.0f} UZS\n"
    msg += f"• Остаток: {safe_number(inv.get('total_stock', 0)):,} шт\n"
    msg += f"• Склад: {safe_number(inv.get('sklad', 0)):,.0f} UZS\n"
    msg += f"• Сумма остатков: {safe_number(inv.get('total_sell', 0)):,.0f} UZS\n"
    msg += f"• Продажи / Склад: {safe_number(inv.get('sales_to_stock_ratio', 0), 2)}\n"
    msg += f"• Прибыль: {safe_number(inv.get('total_profit', 0)):,.0f} UZS\n\n"

    # Vaqt oralig'i
    msg += "🕒 *Период*\n"
    msg += f"• Текущий: {format_date(report['current_period']['date_from'])} — {format_date(report['current_period']['date_to'])}\n"
    msg += f"• Предыдущий: {format_date(report['previous_period']['date_from'])} — {format_date(report['previous_period']['date_to'])}\n"

    try:
        year = datetime.strptime(
            report['current_period']['from'], '%d.%m.%Y %H:%M:%S').year
        msg += f"Данные за {year} год"
    except:
        msg += "Данные за текущий период"

    return msg


def user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "uzum_login": user.uzum_login,
        "uzum_password": user.uzum_password,
        "uzum_api_key": user.uzum_api_key,
        "timezone": user.timezone,
        "is_invalid_key": user.is_invalid_key,
        "is_verified": user.is_verified
    }
