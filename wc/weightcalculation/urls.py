"""
 * Version : 1.0
 * Project: Calendar Automation
 * Copyright : Indxx Capital Management
 * Author: Pavan Rajput
 * Created Date: 08-04-2019
 * Modified Date: dd-mm-yyyy
 * Licensed under : Self
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import (handler400, handler403, handler404, handler500)
from django.views.generic.base import TemplateView
from weightcalculation import views

urlpatterns = [
	path('', views.home, name = 'home'),
	path('equalweight', views.equal_weight, name = 'equalweight'),
	path('equalweightpost', views.eq_weight_post, name='equalweightpost'),
	#path('ulcapweight', views.ul_cap_weight, name = 'ulcapweight'),
	#path('ulcapweightpost', views.ul_cap_weight_post, name='ulcapweightpost'),
	path('ulcapagweight', views.ul_cap_ag_weight, name = 'ulcapagweight'),
	path('ulcapagweightpost', views.ul_cap_ag_weight_post, name = 'ulcapagweightpost'),
	path('uprcapweight', views.upr_cap_weight, name = 'uprcapweight'),
	path('uprcapweightpost', views.upr_cap_weight_post, name = 'uprcapweightpost'),
	#path('ultopremainsecu', views.ul_top_remain_secu_weight, name = 'ultopremainsecu'),
	#path('ultopremainsecupost', views.ul_top_remain_secu_weight_post, name = 'ultopremainsecupost'),
	path('mlp', views.mlp, name = 'mlp'),
	path('mlppost', views.mlp_post, name = 'mlppost'),
	path('mlpsector', views.mlp_sector, name = 'mlpsector'),
	path('mlpsectorpost', views.mlp_sector_post, name = 'mlpsectorpost'),
	path('ussharing', views.us_sharing, name = 'ussharing'),
	path('ussharingpost', views.us_sharing_post, name = 'ussharingpost'),
	path('globalspace', views.global_space, name = 'globalspace'),
	path('globalspacepost', views.global_space_post, name = 'globalspacepost'),
	path('privatecredit', views.private_credit, name = 'privatecredit'),
	path('privatecreditpost', views.private_credit_post, name = 'privatecreditpost'),
	path('g5nextg', views.g5_nextg, name = 'g5nextg'),
	path('g5nextgpost', views.g5_nextg_post, name = 'g5nextgpost'),
	path('aibigdata', views.ai_big_data, name = 'aibigdata'),
	path('aibigdatapost', views.ai_big_data_post, name = 'aibigdatapost'),
	path('blockchain', views.blockchain, name = 'blockchain'),
	path('blockchainpost', views.blockchain_post, name = 'blockchainpost'),
	path('globalaerospace', views.global_aerospace, name = 'globalaerospace'),
	path('globalaerospacepost', views.global_aerospace_post, name = 'globalaerospacepost'),
	path('globalcloudcomputing', views.global_cloud_computing, name = 'globalcloudcomputing'),
	path('globalcloudcomputingpost', views.global_cloud_computing_post, name = 'globalcloudcomputingpost'),
	path('globalecomm', views.global_ecomm, name = 'globalecomm'),
	path('globalecommpost', views.global_ecomm_post, name = 'globalecommpost'),
	#----------------------------- New Indices--------------------------------------------------------------------------------------------------
	path('globaliot', views.global_iot, name = 'globaliot'),
	path('globaliotpost', views.global_iot_post, name = 'globaliotpost'),
	path('foodtech', views.food_tech, name = 'foodtech'),
	path('foodtechpost', views.food_tech_post, name = 'foodtechpost'),
	path('oldagenursing', views.old_age_nursing, name = 'oldagenursing'),
	path('oldagenursingpost', views.old_age_nursing_post, name = 'oldagenursingpost'),
	path('climatechange', views.climate_change, name = 'climatechange'),
	path('climatechangepost', views.climate_change_post, name = 'climatechangepost'),
	path('globalwearablesiot', views.global_wearables_iot, name = 'globalwearablesiot'),
	path('globalwearablesiotpost', views.global_wearables_iot_post, name = 'globalwearablesiotpost'),
	path('northamericancannabis',views.north_american_cannabis,name='northamericancannabis'),
	path('northamericancannabispost',views.north_american_cannabis_post,name='northamericancannabispost'),
	path('healthcareinnovation',views.healthcare_innovation,name='healthcareinnovation'),
	path('healthcareinnovationpost',views.healthcare_innovation_post,name='healthcareinnovationpost'),
	path('usindustrialrealestatelogistics',views.us_industrial_real_estate_logistics,name='usindustrialrealestatelogistics'),
	path('usindustrialrealestatelogisticspost',views.us_industrial_real_estate_logistics_post,name='usindustrialrealestatelogisticspost'),
	path('usjuniorcloudcomputingexpo',views.us_junior_cloud_computing_expo,name='usjuniorcloudcomputingexpo'),
	path('usjuniorcloudcomputingexpopost',views.us_junior_cloud_computing_expo_post,name='usjuniorcloudcomputingexpopost'),
	path('globaljuniorcloudcomputing',views.global_junior_cloud_computing,name='globaljuniorcloudcomputing'),
	path('globaljuniorcloudcomputingpost',views.global_junior_cloud_computing_post,name='globaljuniorcloudcomputingpost'),
	path('usecomm', views.us_ecomm, name = 'usecomm'),
	path('usecommpost', views.us_ecomm_post, name = 'usecommpost'),
	path('ecomm', views.ecomm, name = 'ecomm'),
	path('ecommpost', views.ecomm_post, name = 'ecommpost'),
	path('hylvpreferred',views.hylv_preferred,name='hylvpreferred'),
	path('hylvpreferredpost',views.hylv_preferred_post,name='hylvpreferredpost'),
	path('superdividendprimary',views.super_dividend_primary,name='superdividendprimary'),
	path('superdividendprimarypost',views.super_dividend_primary_post,name='superdividendprimarypost'),
	path('superdividendsecondary',views.super_dividend_secondary,name='superdividendsecondary'),
	path('superdividendsecondarypost',views.super_dividend_secondary_post,name='superdividendsecondarypost'),
	path('globalyieldco',views.global_yieldco,name='globalyieldco'),
	path('globalyieldcopost',views.global_yieldco_post,name='globalyieldcopost'),
	path('yieldcorenewable',views.yieldco_renewable,name='yieldcorenewable'),
	path('yieldcorenewablepost',views.yieldco_renewable_post,name='yieldcorenewablepost'),
	path('qualitygoldminers',views.quality_gold_miners,name='qualitygoldminers'),
	path('qualitygoldminerspost',views.quality_gold_miners_post,name='qualitygoldminerspost'),
	path('reitmaster',views.reit_master,name='reitmaster'),
	path('reitmasterpost',views.reit_master_post,name='reitmasterpost'),
	path('reitpreferred',views.reit_preferred,name='reitpreferred'),
	path('reitpreferredpost',views.reit_preferred_post,name='reitpreferredpost'),
	path('ushighbetalow',views.us_high_beta_low,name='ushighbetalow'),
	path('ushighbetalowpost',views.us_high_beta_low_post,name='ushighbetalowpost'),
	path('uspoliwogg',views.us_poliwogg,name='uspoliwogg'),
	path('uspoliwoggpost',views.us_poliwogg_post,name='uspoliwoggpost'),
#-------------------------------------------------------------------------------------------------------------------
	path('back/', views.back, name = 'back'),
    #path('weightcal/', views.weightcal, name='weightcal'),
	path('signin', views.sign_in, name='signin'),
	path('callback', views.callback, name='callback'),
	path('signout', views.sign_out, name='signout'),
	path('gettoken/', views.gettoken, name='gettoken'),
	path('downloadcsv/', views.download_csv, name='downloadcsv'),
	path('downloadcsv1/',views.download_csv1,name='downloadcsv1'),


]
