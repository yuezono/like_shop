import csv
import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Shops

class Command(BaseCommand):
    help = 'Backup Shops data'

    def handle(self, *args, **options):
      #実行時のYYYYMMDDを取得
      date = datetime.date.today().strftime("%Y%m%d")

      #保存用ファイルの相対パス
      file_path = settings.BACKUP_PATH + 'shops_' + date + '.csv'

      #保存ディレクトリが存在しなければ作成
      os.makedirs(settings.BACKUP_PATH, exist_ok=True)

      #バックアップファイルの作成
      with open(file_path, 'w')as file:
        writer = csv.writer(file)

        #ヘッダーの書き込み
        header = [field.name for field in Shops._meta.fields]
        writer.writerow(header)

        #Shopsテーブルの全データを取得
        shopper = Shops.objects.all()

        #データ部分の書き込み
        for shops in shopper:
          writer.writerow([str(shops.user),
                        shops.title,
                        shops.content,
                        str(shops.photo1),
                        str(shops.photo2),
                        str(shops.photo3),
                        str(shops.created_at),
                        str(shops.updated_at)])

        #保存ディレクトリのファイルリストを取得
        files = os.listdir(settings.BACKUP_PATH)
        #ファイルが設定数以上あったら一番古いファイルを削除
        if len(files) >= settings.NUM_SAVED_BACKUP:
          files.sort()
          os.remove(settings.BACKUP_PATH + files[0])


