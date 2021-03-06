"""
Tests for registry admin module
"""
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.test import TestCase

from ..admin import MonitoringLocationAdmin, MonitoringLocationAdminForm
from ..models import AgencyLookup, MonitoringLocation


class TestRegistryFormAdmin(TestCase):

    def setUp(self):
        self.form_data = {
            'display_flag': False,
            'agency': 'USGS',
            'site_no': '1234567',
            'site_name': 'My test site',
            'wl_sn_flag': False,
            'wl_baseline_flag': False,
            'qw_sn_flag': False,
            'qw_baseline_flag': False
        }

    def test_valid_when_display_flag_false(self):
        form = MonitoringLocationAdminForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_when_site_name_blank(self):
        self.form_data['site_name'] = ''
        form = MonitoringLocationAdminForm(self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data['site_name'] = '     '
        form = MonitoringLocationAdminForm(self.form_data)
        self.assertFalse(form.is_valid())

    def test_valid_when_display_flag_true_sn_flags_false(self):
        self.form_data['display_flag'] = True
        form = MonitoringLocationAdminForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_valid_when_display_flag_true_and_wl_sn_flags_true(self):
        self.form_data['display_flag'] = True
        self.form_data['wl_sn_flag'] = True
        self.form_data['wl_well_purpose'] = 'Other'
        self.form_data['wl_well_type'] = 'Trend'
        self.form_data['wl_baseline_flag'] = True
        form = MonitoringLocationAdminForm(self.form_data)

        self.assertTrue(form.is_valid())

    def test_invalid_when_display_flag_true_and_wl_sn_flag_true(self):
        self.form_data['display_flag'] = True
        self.form_data['wl_sn_flag'] = True
        form = MonitoringLocationAdminForm(self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data['wl_well_purpose'] = 'Other'
        self.form_data['wl_well_type'] = 'Trend'
        self.form_data['wl_baseline_flag'] = False
        form = MonitoringLocationAdminForm(self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data['wl_well_purpose'] = ''
        self.form_data['wl_well_type'] = 'Trend'
        self.form_data['wl_baseline_flag'] = True
        form = MonitoringLocationAdminForm(self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data['wl_well_purpose'] = 'Other'
        self.form_data['wl_well_type'] = ''
        self.form_data['wl_baseline_flag'] = True
        form = MonitoringLocationAdminForm(self.form_data)
        self.assertFalse(form.is_valid())


class TestRegistryAdmin(TestCase):
    fixtures = ['test_monitoring_location.json', 'test_user.json']

    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser('my_superuser')
        self.adwr_group = Group.objects.get(name='adwr')
        self.adwr_user = get_user_model().objects.create_user('adwr_user')
        self.adwr_user.groups.add(self.adwr_group)
        self.adwr_user.save()

        self.site = AdminSite()
        self.admin = MonitoringLocationAdmin(MonitoringLocation, self.site)

    def test_site_id(self):
        reg_entry = MonitoringLocation.objects.get(site_no='44445555',
                                                   agency='ADWR')
        site_id = MonitoringLocationAdmin.site_id(reg_entry)

        self.assertEqual(site_id, "ADWR:44445555")

    def test_save_model_new_registry_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.adwr_user
        registry = MonitoringLocation.objects.create(site_no='11111111')
        self.admin.save_model(request, registry, None, None)

        saved_registry = MonitoringLocation.objects.get(site_no='11111111')
        self.assertEqual(saved_registry.insert_user, self.adwr_user)
        self.assertEqual(saved_registry.update_user, self.adwr_user)
        self.assertEqual(saved_registry.agency, AgencyLookup.objects.get(agency_cd='ADWR'))

    def test_save_model_new_registry_with_super_user(self):
        request = HttpRequest()
        request.user = self.superuser
        registry = MonitoringLocation.objects.create(site_no='11111111',
                                                     agency=AgencyLookup.objects.get(agency_cd='ADWR'))
        self.admin.save_model(request, registry, None, None)

        saved_registry = MonitoringLocation.objects.get(site_no='11111111')
        self.assertEqual(saved_registry.insert_user, self.superuser)
        self.assertEqual(saved_registry.update_user, self.superuser)
        self.assertEqual(saved_registry.agency, AgencyLookup.objects.get(agency_cd='ADWR'))

    def test_save_model_existing_registry_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.superuser
        registry = MonitoringLocation.objects.create(site_no='11111111',
                                                     agency=AgencyLookup.objects.get(agency_cd='ADWR'))
        self.admin.save_model(request, registry, None, None)

        saved_registry = MonitoringLocation.objects.get(site_no='11111111')
        saved_registry.site_name = 'A site'
        request.user = self.adwr_user
        self.admin.save_model(request, saved_registry, None, None)
        saved_registry = MonitoringLocation.objects.get(site_no='11111111')

        self.assertEqual(saved_registry.insert_user, self.superuser)
        self.assertEqual(saved_registry.update_user, self.adwr_user)
        self.assertEqual(saved_registry.agency, AgencyLookup.objects.get(agency_cd='ADWR'))

    def test_get_queryset_with_superuser(self):
        request = HttpRequest()
        request.user = self.superuser
        qs = self.admin.get_queryset(request)

        self.assertEqual(qs.count(), 3)

    def test_get_queryset_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.adwr_user
        qs = self.admin.get_queryset(request)

        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.filter(agency='ADWR').count(), 1)

    def test_has_view_permission_with_superuser(self):
        request = HttpRequest()
        request.user = self.superuser

        self.assertTrue(self.admin.has_view_permission(request))
        self.assertTrue(self.admin.has_view_permission(request, MonitoringLocation.objects.get(site_no='12345678')))

    def test_has_view_permission_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.adwr_user

        self.assertTrue(self.admin.has_view_permission(request))
        self.assertTrue(self.admin.has_view_permission(request, MonitoringLocation.objects.get(site_no='44445555')))
        self.assertFalse(self.admin.has_view_permission(request, MonitoringLocation.objects.get(site_no='12345678')))

    def test_has_add_permission_with_superuser(self):
        request = HttpRequest()
        request.user = self.superuser

        self.assertTrue(self.admin.has_add_permission(request))

    def test_has_add_permission_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.adwr_user

        self.assertTrue(self.admin.has_add_permission(request))

    def test_has_change_permission_with_superuser(self):
        request = HttpRequest()
        request.user = self.superuser

        self.assertTrue(self.admin.has_change_permission(request))
        self.assertTrue(self.admin.has_change_permission(request, MonitoringLocation.objects.get(site_no='12345678')))

    def test_has_change_permission_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.adwr_user

        self.assertTrue(self.admin.has_change_permission(request))
        self.assertTrue(self.admin.has_change_permission(request, MonitoringLocation.objects.get(site_no='44445555')))
        self.assertFalse(self.admin.has_change_permission(request, MonitoringLocation.objects.get(site_no='12345678')))

    def test_has_delete_permission_with_superuser(self):
        request = HttpRequest()
        request.user = self.superuser

        self.assertTrue(self.admin.has_delete_permission(request))
        self.assertTrue(self.admin.has_delete_permission(request, MonitoringLocation.objects.get(site_no='12345678')))

    def test_has_delete_permission_with_adwr_user(self):
        request = HttpRequest()
        request.user = self.adwr_user

        self.assertTrue(self.admin.has_delete_permission(request))
        self.assertTrue(self.admin.has_delete_permission(request, MonitoringLocation.objects.get(site_no='44445555')))
        self.assertFalse(self.admin.has_delete_permission(request, MonitoringLocation.objects.get(site_no='12345678')))
