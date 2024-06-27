from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
import requests
from datetime import date, datetime
import time
import calendar

# Create your models here.

#General functions

def convert_to_array(data):
    array = []
    for record in data:
        for item in record:
            array.append(list(item.values()))
    return array

def get_header(data):
    if data is not None:
        header = [list(data[0].keys())]
    else:
        header = []
    return header

def status_desc(status):
    status_map = {
        0: 'Mới',
        17: 'Chờ xác nhận',
        11: 'Chờ hàng',
        12: 'Chờ in',
        13: 'Đã in',
        20: 'Đã đặt hàng',
        1: 'Đã xác nhận',
        8: 'Đang đóng hàng',
        9: 'Chờ chuyển hàng',
        2: 'Đã gửi hàng',
        3: 'Đã nhận',
        16: 'Đã thu tiền',
        4: 'Đang trả hàng',
        15: 'Hoàn 1 phần',
        5: 'Đã hoàn',
        6: 'Đã hủy',
        7: 'Đã xóa',
        10: 'Đơn Webcake',
        21: 'Đơn Storecake'
    }
    return status_map.get(status, None)

#End general functions


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(_("tên nhóm trang"),blank=False,max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,limit_choices_to={'is_staff': True},)

    class Meta:
        verbose_name = _("Nhóm trang")
        verbose_name_plural = _("Nhóm trang")
    def __str__(self) -> str:
        return self.name

class Page(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(_("tên ngắn page (tự đặt)"),blank=False,editable=True, max_length=10)
    pancake_id = models.CharField(verbose_name=_("id trang theo Pancake"),max_length=20,blank=False,editable=True)
    facebook_id = models.CharField(verbose_name=_("id trang Facebook"),max_length=20,blank=True,editable=True)
    name = models.CharField(_("tên trang"),blank=True,max_length=200)
    url = models.CharField(_("địa chỉ trang"),blank=True,max_length=200)
    owner = models.CharField(_("tên người sở hữu trang"),blank=True,max_length=200)
    group = models.ForeignKey(Group,on_delete=models.SET_NULL,verbose_name=_("thuộc nhóm"),blank=True,null=True)
    access_token = models.CharField(_("access token của page"),blank=True,max_length=200)

    class Meta:
        verbose_name = _("Trang")
        verbose_name_plural = _("Trang")

    def __str__(self) -> str:
        return self.name
    
    def customer_engagements_bydate_raw(self,date):
        BASE_URL = 'https://pages.fm/api/public_api/v1/pages/'
        pancake_engage_url = f"{BASE_URL}{self.pancake_id}/statistics/customer_engagements"
        params = {
            'page_access_token': self.access_token,
            'date_range': f"{date} 00:00:00 - {date} 23:59:59"
        }
        print(self.access_token)
        r = requests.get(pancake_engage_url, params=params)
        try:
            print(r.url)
            return r.json()
        except Exception as e:
            print(f"Lỗi khi lấy data engagements by date raw: {e}")
            return {}
        
    def customer_engagements_by_date_range_raw(self,fromdate,todate):
        BASE_URL = 'https://pages.fm/api/public_api/v1/pages/'
        pancake_engage_url = f"{BASE_URL}{self.pancake_id}/statistics/customer_engagements"
        params = {
            'page_access_token': self.access_token,
            'date_range': f"{fromdate} 00:00:00 - {todate} 23:59:59"
        }
        print(self.access_token)
        r = requests.get(pancake_engage_url, params=params)
        try:
            print(r.url)
            return r.json()
        except Exception as e:
            print(f"Lỗi khi lấy data engagements by date range raw: {e}")
            return {}
        
    def customer_engagements_bydate(self,date,header=1):
        BASE_URL = 'https://pages.fm/api/public_api/v1/pages/'
        pancake_engage_url = f"{BASE_URL}{self.pancake_id}/statistics/customer_engagements"
        params = {
            'page_access_token': self.access_token,
            'date_range': f"{date} 00:00:00 - {date} 23:59:59"
        }
        try:
            r = requests.get(pancake_engage_url, params=params)
            time.sleep(1.1)
            engage = r.json().get("users_engagements",[])
            if not engage:
                return []
        except Exception as e:
            print(f"Error at {date} - detail as {e}")
            return []
        result = []
        #print(result)
        if engage is not None:
            for item in engage:
                try:
                    row = [{
                        'Năm': int(date.split('/')[2]),
                        'Tháng': int(date.split('/')[1]),
                        'Ngày': date,
                        'Page ID': self.id,
                        'Tên trang': self.name,
                        'Sales': item.get('name'),
                        'Đơn khách cũ': item.get('old_order_count'),
                        'Đơn khách mới': item.get('order_count') - item.get('old_order_count') if item.get('order_count') > 0 else 0,
                        'Tổng đơn': item.get('order_count'),
                        'Comment': item.get('comment_count',0),
                        #'customer_engagement_new_inbox': item.get('customer_engagement_new_inbox',0),
                        #'inbox_count': item.get('inbox_count',0),
                        'TT cũ': item.get('total_engagement',0) - item.get('new_customer_replied_count',0), #TT cũ
                        'TT mới': item.get('new_customer_replied_count',0), #TT mới
                        'Tương tác': item.get('total_engagement',0),
                        'TLC': f"{(item.get('order_count') / item.get('new_customer_replied_count',0)):.0%}" if item.get('new_customer_replied_count',0) > 0 else 0,
                        'TLC chung': f"{(item.get('order_count') / item.get('total_engagement',0)):.0%}" if item.get('total_engagement',0) > 0 else 0,
                        'TLC khách cũ': f"{(item.get('old_order_count') / (item.get('total_engagement',0) - item.get('new_customer_replied_count',0))):.0%}" if item.get('total_engagement',0) - item.get('new_customer_replied_count',0) > 0 else 0,
                        'TLC khách mới': (item.get('order_count') - item.get('old_order_count') if item.get('order_count') > 0 else 0) / item.get('new_customer_replied_count',0) if item.get('new_customer_replied_count',0) > 0 else 0
                    }]
                #row = [engage[header] for header in headers]
                    result.append(row)
                except Exception as e:
                    print(f"Error: {e}")
        array = []
        if result:
            array = [list(result[0][0].keys()) if header else []]
            array.extend([list(item[0].values()) for item in result])
        else:
            array = []
        return array
        #print(result)
        #print(array)
    def customer_engagements_bymonth(self,year,month):
        result = []
        header_ok = 0
        for day in range(1,calendar._monthlen(year,month)+1):
            date = f"{day:02}/{month:02}/{year}"
            try:
                engage_by_date = self.customer_engagements_bydate(date)
                if engage_by_date:
                    if not header_ok:
                        result.append(engage_by_date[0])
                        header_ok = 1
                    result.extend(engage_by_date[1:])
            except Exception as e:
                print(f"Error at {date} - detail: {e}")
        return result
    

    def customer_engagements_by_date_range(self,fromdate,todate,header=1):
        BASE_URL = 'https://pages.fm/api/public_api/v1/pages/'
        pancake_engage_url = f"{BASE_URL}{self.pancake_id}/statistics/customer_engagements"
        params = {
            'page_access_token': self.access_token,
            'date_range': f"{fromdate} 00:00:00 - {todate} 23:59:59"
        }
        try:
            r = requests.get(pancake_engage_url, params=params)
            time.sleep(1.1)
            engage = r.json().get("users_engagements",[])
            if not engage:
                return []
        except Exception as e:
            print(f"Error at date range: {fromdate} - {todate} - detail as {e}")
            return []
        result = []
        #print(result)
        if engage is not None:
            for item in engage:
                try:
                    
                    row = [{
                        'Năm': int(date.split('/')[2]),
                        'Tháng': int(date.split('/')[1]),
                        'Ngày': date,
                        'Page ID': self.id,
                        'Tên trang': self.name,
                        'Sales': item.get('name'),
                        'Đơn khách cũ': item.get('old_order_count'),
                        'Đơn khách mới': item.get('order_count') - item.get('old_order_count') if item.get('order_count') > 0 else 0,
                        'Tổng đơn': item.get('order_count'),
                        'Comment': item.get('comment_count',0),
                        #'customer_engagement_new_inbox': item.get('customer_engagement_new_inbox',0),
                        #'inbox_count': item.get('inbox_count',0),
                        'TT cũ': item.get('total_engagement',0) - item.get('new_customer_replied_count',0), #TT cũ
                        'TT mới': item.get('new_customer_replied_count',0), #TT mới
                        'Tương tác': item.get('total_engagement',0),
                        'TLC': f"{(item.get('order_count') / item.get('new_customer_replied_count',0)):.0%}" if item.get('new_customer_replied_count',0) > 0 else 0,
                        'TLC chung': f"{(item.get('order_count') / item.get('total_engagement',0)):.0%}" if item.get('total_engagement',0) > 0 else 0,
                        'TLC khách cũ': f"{(item.get('old_order_count') / (item.get('total_engagement',0) - item.get('new_customer_replied_count',0))):.0%}" if item.get('total_engagement',0) - item.get('new_customer_replied_count',0) > 0 else 0,
                        'TLC khách mới': (item.get('order_count') - item.get('old_order_count') if item.get('order_count') > 0 else 0) / item.get('new_customer_replied_count',0) if item.get('new_customer_replied_count',0) > 0 else 0
                    }]
                #row = [engage[header] for header in headers]
                    result.append(row)
                except Exception as e:
                    print(f"Error: {e}")
        array = []
        if result:
            array = [list(result[0][0].keys()) if header else []]
            array.extend([list(item[0].values()) for item in result])
        else:
            array = []
        return array
    

    



    

