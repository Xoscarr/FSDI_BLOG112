from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post 
from django.urls import reverse


class PostModelTests(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com', 
            password='secret'
        )
        self.post = Post.objects.create(
            title="A title",
            body="A body",
            author=self.user 
        )

    def test_post_list_view(self):
        response = self.clientget("/posts/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("post.list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A Title")
        self.assertContains(response, "A Body")
        self.assertContains(response, "A Title")
        self.assertContains(response, "A Body")
        self.assertTemplateUsed(response, "blog/list.html")
        self.assertTemplateUsed(response, "base.html")

    def post_detail_view(self):
        response = self.client.get("/posts/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A Title")
        self.assertTemplateUsed(response, "blog/detail.html")

    def test_post_create_view(self):
        response= self.client.post(reverse("post_new"), {
            "title":"New title",
            "body":"New body",
            "author":self.user
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "New title")
        self.assertEqual(Post.objects.last().title, "New body")
        self.assertTemplateUsed(response, "blog/new.html")

    def test_post_update_view(self):
        response = self.client.post(reverse("post_edit", args=[1]), {
            "title":"Updated title",
            "body": "updated body",

        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "Updated title")
    
    def test_post_delete_view(self):
        response = self.client.post(reverse("post_delete", args=[1]))
        self.assertEqual(response.status_code, 302)
        # # if we wantted to validate:
        # response = self.client.get(reverse("post_detail", args=[1]))
        # self.assertEqual(response2.status_code, 404)
        
    def test_body_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f"{post.body}"
        self.assertEqual(expected_object_name, "test")

    def test_post_string_representation(self):
        post = Post.objects.get(id=1)
        str_repr = str(post)
        self.assertEqual(str_repr, "A test")


    # class PostViewTest(TestCase): 
    
    # # def setUp(self):
    # #     Post.objects.create(title="Another test", body="Test2")

    # def test_listview_url_exists_at_proper_location(self):
    #     resp = self.client.get("/posts/")
    #     self.assertEqual(resp.status_code, 200)
    
    # def test_listview_url_by_name(self):
    #     resp = self.client.get(reverse("posts_list"))
    #     self.assertEqual(resp.status_code, 200)

    # def test_listview_uses_correct_template(self):
    #     resp = self.client.get("/posts/")
    #     self.assertTemplateUsed(resp, "post_list.html")

    # def test_listview_contains_content(self):
    #     resp = self.client.get(reverse("post_list"))
    #     self.assertContains(resp, "Another test")
    
    # def test_detailview_exists_at_proper_location(self):
    #     resp = self.client.get("/posts/1/")
    #     self.assertEqual(resp.status_code, 200)

    # def test_detailview_uses_correct_template(self):
    #     resp = self.client.get(reverse("post_detail", args=[1]))
    #     self.assertTemplateUsed(resp, "post_detail.html")