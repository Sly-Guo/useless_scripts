## 根据图片的exif信息来推测所在位置
# 需要图片的exif信息中携带GPS信息


import requests
import exifread
 
class GetPhotoInfo:
    def __init__(self, photo):
        self.photo = photo
        # 百度地图ak  请替换为自己申请的ak
        self.ak = 'rv3yloWmcsvjuzzGt60haql8xIVpyZGM'
        self.location = self.get_photo_info()
 
    def get_photo_info(self, ):
        with open(self.photo, 'rb') as f:
            tags = exifread.process_file(f)
        try:
            # 打印照片其中一些信息
            print('拍摄时间：', tags['EXIF DateTimeOriginal'])
            print('照相机制造商：', tags['Image Make'])
            print('照相机型号：', tags['Image Model'])
            print('照片尺寸：', tags['EXIF ExifImageWidth'], tags['EXIF ExifImageLength'])
            # 纬度
            lat_ref = tags["GPS GPSLatitudeRef"].printable
            lat = tags["GPS GPSLatitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            lat = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / float(lat[3]) / 3600
            if lat_ref != "N":
                lat = lat * (-1)
            # 经度
            lon_ref = tags["GPS GPSLongitudeRef"].printable
            lon = tags["GPS GPSLongitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            lon = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / float(lon[3]) / 3600
            if lon_ref != "E":
                lon = lon * (-1)
        except KeyError:
            return "ERROR:请确保照片包含经纬度等EXIF信息。"
        else:
            print("经纬度：", lat, lon)
            return lat, lon
 
    def get_location(self):
        url = 'http://api.map.baidu.com/reverse_geocoding/v3/?ak={}&output=json' \
              '&coordtype=wgs84ll&location={},{}'.format(self.ak, *self.location)
        response = requests.get(url).json()
        status = response['status']
#         print(response)
        if status == 0:
            address = response['result']['formatted_address']
            print('详细地址：', address)
        else:
            print('baidu_map error')
 
 
if __name__ == '__main__':
    Main = GetPhotoInfo('D:/all_band/3/IMG_210323_061609_0051_RGB.JPG')
    Main.get_location()
