from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Category
# Create your tests here.


class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


class IndexViewTests(TestCase):
    def test_index_view_with_no_category(self):
        response = self.client.get(reverse('rango:rango_default'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "There are no categories present.")
        # self.assertQuerySetEqual(response.context['categories'], [])

    # def test_index_view_with_category(self):
    #     add_cat('test1', 1, 1)
    #     add_cat('test2', 2, 2)
    #     add_cat('test3', 3, 3)
    #     add_cat('test4', 4, 4)
    #     response = self.client.get(reverse('rango:rango_default'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "test")        

