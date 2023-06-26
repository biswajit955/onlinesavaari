from django.urls import path,include
from . import views
from .views import *
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('base', views.base, name="base"),
	path('', views.admin_login, name="admin_login"),
    path('direct_cancel/', views.direct_cancel, name="direct_cancel"),
	path('admin_logout', views.admin_logout, name="admin_logout"),
	path("agent_list", views.agent_list, name='agent_list'),
    path("agent_list", views.agent_list, name='agent_list'),
    path("tds_detail", views.tds_detail, name='tds_detail'),
    path("find_ticket", views.find_ticket, name='find_ticket'),
    path("hold_booking", views.hold_booking, name='hold_booking'),
    path('distribution_list', views.distribution_list, name="distribution_list"),
    path('commission', views.commission, name="commission"),
    path('customer_list', views.customer_list, name="customer_list"),
    path('corporation_list', views.corporation_list, name="corporation_list"),
    path('view_agent_profile/<int:id>/', views.view_agent_profile, name="view_agent_profile"),
    path('update_credit/<int:id>/', views.update_credit, name="update_credit"),
    path('view_cust_profile/<int:id>/', views.view_cust_profile, name="view_cust_profile"),
    path('view_corp_profile/<int:id>/', views.view_corp_profile, name="view_corp_profile"),
    path('update_credit/<int:id>/', views.update_credit, name="update_credit"),
    path('updaterecord/<int:id>/', views.updaterecord, name="updaterecord"),
    path('update_hold/<int:id>/', views.update_hold, name="update_hold"),
    path('update_agent/<int:id>/', views.update_agent, name="update_agent"),
    path('update_corp/<int:id>/', views.update_corp, name="update_corp"),
    path('updatedoc/<int:id>/', views.updatedoc, name="updatedoc"),
    path('update_refund/<int:id>/', views.update_refund, name="update_refund"),
    path('update_deposit/<int:id>/', views.update_deposit, name="update_deposit"),
    path('delete_markup/<int:id>/', views.delete_markup, name="delete_markup"),
    path('delete_user/<int:id>/', views.delete_user, name="delete_user"),
    path('delete_serialmarkup/<int:id>/', views.delete_serialmarkup, name="delete_serialmarkup"),
    path('updatepromocode/<int:id>/', views.updatepromocode, name="updatepromocode"),
    path('updateseriesrecord/<int:id>/', views.updateseriesrecord, name="updateseriesrecord"),
    path('markup', views.markup, name="markup"),
    path('refund',views.refund,name="refund"),
    path('reschedule',views.reschedule,name="reschedule"),
    path('reschedule_pay_request',views.reschedule_pay_request,name="reschedule_pay_request"),
    path('update_reschedule/<int:id>/',views.update_reschedule,name="update_reschedule"),
    path('serialmarkup', views.serialmarkup, name="serialmarkup"),
    path('promocode', views.promocode, name="promocode"),
    path('flightbooking', views.flightbooking, name="flightbooking"),
    path('hotelbooking', views.hotelbooking, name="hotelbooking"),
    path('updateflightboking/<int:id>/', views.updateflightboking, name="updateflightboking"),
    path('updatehotelboking/<int:id>/',
          views.updatehotelboking, name="updatehotelboking"),
    
    path('agentlogin', views.agent_login, name="agent_login"),
    path('banner', views.banner, name="banner"),
    path('deposit_request', views.deposit_request, name="deposit_request"),
    path('staff', views.staff, name="staff"),
    path('apibalance', views.apibalance, name="apibalance"),
    path('notification', views.notification, name="notification"),
    path('RegisterAdmin/', RegisterAdmin.as_view(), name='RegisterAdmin'),
    # path('designation',views.designation, name='designation'),

    path('addpermitions/', CreateGroup.as_view(), name='AddPermitions'),
    path('agentcredit/', AgentCredits.as_view(), name='AgentCredit'),

    path('mailbox/', views.mailbox, name='mailbox'),
    path('manual_ticket/', views.manual_ticket, name='manual_ticket'),
    
    path('card_list/', views.card_list, name='card_list'),
    path('update_card/<int:id>', views.update_card, name='update_card'),
    path('delete_card/<int:id>', views.delete_card, name='delete_card'),
    path('pcc_list/', views.pcc_list, name='pcc_list'),
    path('update_pcc/<int:id>', views.update_pcc, name='update_pcc'),
    path('delete_pcc/<int:id>', views.delete_pcc, name='delete_pcc'),
    path('deduct_wallet/', views.deduct_wallet, name='deduct_wallet'),
    path('agent_recharge_wallet/<int:id>', views.agent_recharge_wallet, name='agent_recharge_wallet'),
    path('hotel_markup', views.hotel_markup, name="hotel_markup"),
    path('update_hotel_markup/<int:id>', views.update_hotel_markup, name="update_hotel_markup"),
    path('delete_hotel_markup/<int:id>', views.delete_hotel_markup, name="delete_hotel_markup"),
    path('agent_transaction_excel', views.agent_transaction_excel, name="agent_transaction_excel"),
    path('flight_booking_excel', views.flight_booking_excel, name="flight_booking_excel"),
    path('insurance_booking_list', views.insurance_booking_list, name="insurance_booking_list"),
	path('update_insurance_booking/<int:id>', views.update_insurance_booking, name="update_insurance_booking"),
 

    path('corporate_manager_excel', views.corporate_manager_excel, name="corporate_manager_excel"),
    path('customer_manager_excel', views.customer_manager_excel, name="customer_manager_excel"),
    path('hotel_booking_excel', views.hotel_booking_excel, name="hotel_booking_excel"),
    path('insurance_booking_excel', views.insurance_booking_excel, name="insurance_booking_excel"),
    path('refund_excel', views.refund_excel, name="refund_excel"),
    path('reschedule_excel', views.reschedule_excel, name="reschedule_excel"),
    path('deposit_excel', views.deposit_excel, name="deposit_excel"),

    #by biswajit
    path('zoho-invoice/<int:ids>/',views.zoho_invoice, name="zoho_invoice"),
    path('groups/<int:pk>/update/', GroupUpdateView.as_view(), name='group_update'),

    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)