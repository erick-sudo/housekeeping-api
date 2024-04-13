from django.contrib import admin

class SparkleAdminSite(admin.AdminSite):
    site_header = 'SparkleSync'
    site_title = 'SparkleSync'
    
sparkle_admin_site = SparkleAdminSite(name="sparkle-sync")