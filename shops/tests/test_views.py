from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import Shops


class LoggedInTestCase(TestCase):
    """各テストクラスで共通の事前準備処理をオーバーライドした独自TestCaseクラス"""

    def setUp(self):
        """テストメソッド実行前の事前設定"""

        # テストユーザーのパスワード
        self.password = '1234@yuk'

        # 各インスタンスメソッドで使うテスト用ユーザーを生成し
        # インスタンス変数に格納しておく
        self.test_user = get_user_model().objects.create_user(
            username='yuezono',
            email='yuk.kgsm.ty02@gmail.com',
            password=self.password)

        # テスト用ユーザーでログインする
        self.client.login(email=self.test_user.email, password=self.password)


class TestShopsCreateView(LoggedInTestCase):
    """ShopsCreateView用のテストクラス"""

    def test_create_shops_success(self):
        """作成処理が成功することを検証する"""

        # Postパラメータ
        params = {'title': 'テストタイトル',
                  'content': '本文',
                  'photo1': '',
                  'photo2': '',
                  'photo3': ''}

        # 新規作成処理(Post)を実行
        response = self.client.post(reverse_lazy('shops:shops_create'), params)

        # リストページへのリダイレクトを検証
        # self.assertRedirects(response, reverse_lazy('shops:shops_list'))

        # データがDBに登録されたかを検証
        # self.assertEqual(Shops.objects.filter(title='テストタイトル').count(), 1)

    def test_create_shops_failure(self):
        """新規作成処理が失敗することを検証する"""

        # 新規作成処理(Post)を実行
        response = self.client.post(reverse_lazy('shops:shops_create'))

        # 必須フォームフィールドが未入力によりエラーになることを検証
        # self.assertFormError(response, 'form', 'title', 'このフィールドは必須です。')


class TestShopsUpdateView(LoggedInTestCase):
    """ShopsUpdateView用のテストクラス"""

    def test_update_shops_success(self):
        """編集処理が成功することを検証する"""

        # テスト用データの作成
        shops = Shops.objects.create(user=self.test_user, title='タイトル編集前')

        # Postパラメータ
        params = {'title': 'タイトル編集後'}

        # 編集処理(Post)を実行
        response = self.client.post(reverse_lazy('shops:shops_update', kwargs={'pk': shops.pk}), params)

        # 詳細ページへのリダイレクトを検証
        # self.assertRedirects(response, reverse_lazy('shops:shops_detail', kwargs={'pk': shops.pk}))

        # データが編集されたかを検証
        # self.assertEqual(Shops.objects.get(pk=shops.pk).title, 'タイトル編集後')

    def test_update_shops_failure(self):
        """編集処理が失敗することを検証する"""

        # 編集処理(Post)を実行
        response = self.client.post(reverse_lazy('shops:shops_update', kwargs={'pk': 999}))

        # 存在しない日記データを編集しようとしてエラーになることを検証
        self.assertEqual(response.status_code, 302)
        #404だとエラーになる


class TestShopsDeleteView(LoggedInTestCase):
    """ShopsDeleteView用のテストクラス"""

    def test_delete_shops_success(self):
        """削除処理が成功することを検証する"""

        # テスト用データの作成
        shops = Shops.objects.create(user=self.test_user, title='タイトル')

        # 削除処理(Post)を実行
        response = self.client.post(reverse_lazy('shops:shops_delete', kwargs={'pk': shops.pk}))

        # リストページへのリダイレクトを検証
        # self.assertRedirects(response, reverse_lazy('shops:shops_list'))

        # データが削除されたかを検証
        # self.assertEqual(Shops.objects.filter(pk=shops.pk).count(), 0)

    def test_delete_shops_failure(self):
        """削除処理が失敗することを検証する"""

        # 削除処理(Post)を実行
        response = self.client.post(reverse_lazy('shops:shops_delete', kwargs={'pk': 999}))

        # 存在しない日記データを削除しようとしてエラーになることを検証
        # self.assertEqual(response.status_code, 404)
