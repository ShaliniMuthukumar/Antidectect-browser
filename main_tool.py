import os
import json
import zipfile
import random
import psutil
import shutil
import time
import re
import pandas as pd
import uuid
from faker import Faker
import requests
import subprocess
from gologin import getRandomPort
import concurrent.futures

class IntegratedDataGenerator():
    def __init__(self,profile_name=None):
        self.platform_type = random.choice(["win32","linux armv81","iphone","macintel","android"])
        self.result_set = self.UserProfileGenerator(
        useragent_path=os.path.join(os.getcwd(), f'parquet_files/{self.platform_type}/useragent.parquet'),
        hardware_path=os.path.join(os.getcwd(), f'parquet_files/{self.platform_type}/hardwareConcurrency.parquet'),
        maxtouchpoints_path=os.path.join(os.getcwd(), f'parquet_files/{self.platform_type}/maxtouchpoints.parquet'),
        devicememory_path=os.path.join(os.getcwd(), f'parquet_files/{self.platform_type}/devicememory.parquet'),
        language_path=os.path.join(os.getcwd(), f'parquet_files/{self.platform_type}/language.parquet'),
        webgl_path=os.path.join(os.getcwd(), f'parquet_files/{self.platform_type}/webgl.parquet'),
        mediadevice_path=os.path.join(os.getcwd(), f'parquet_files/{self.platform_type}/mediadevice.parquet'),
        os_path=os.path.join(os.getcwd(), f'parquet_files/{self.platform_type}/os.parquet'),
        resolution_path=os.path.join(os.getcwd(), f'parquet_files/{self.platform_type}/resolution.parquet'),
        devicepixel_path=os.path.join(os.getcwd(), f'parquet_files/{self.platform_type}/devicepixelratio.parquet')
    )        
        
        self.profile_name = profile_name
        self.flag=1
        
        # Set the default path for the profile_data directory
        self.main_path = os.path.join(os.getcwd(), 'profile_data')

        # If a profile_number is provided, create a profile with the specified number
        if profile_name is not None:
            self.main_path = os.path.join(self.main_path, f'{profile_name}')
            os.makedirs(self.main_path, exist_ok=True)  # Create the profile directory

            # Extract contents from main.zip to the profile directory
            zip_path = os.path.join(os.getcwd(), 'main.zip')
            if '.zip' in zip_path:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(self.main_path)
        
    def create_profile(self):
        dev = self.result_set['navigator']['deviceMemory']
        if dev == '4':
            deviceMemory = 4096
        elif dev == '2':
            deviceMemory = 2048
        elif dev == '8':
            deviceMemory = 8192
        elif dev == '16':
            deviceMemory = 16384
        else:
            deviceMemory = 4096

        main_data = {
            'name': self.profile_name,
            'id': self.result_set['id'],
            'notes': '',
            'browserType': self.result_set['browserType'],
            'os': self.result_set['os'],
            'bookmarks': self.result_set['bookmarks'],
            'profile_id': self.result_set['profile_id'],
            'deviceMemory': deviceMemory,
            'userAgent': self.result_set['userAgent'],
            'navigator': {
                'userAgent' : self.result_set['navigator']['userAgent'],
                'hardwareConcurrency': self.result_set['hardwareConcurrency'],
                'deviceMemory': deviceMemory,
                'language': self.result_set['navigator']['language'],
                'max_touch_points' : int(self.result_set['navigator']['maxTouchPoints']),
                'platform': self.result_set['navigator']['platform'],
                'resolution': self.result_set['navigator']['resolution'],
                'doNotTrack': random.choice([True, False])
            },
            'screenWidth': int(self.result_set['screenWidth']),
            'screenHeight': int(self.result_set['screenHeight']),
            'timezone': {
                'id' : self.tz.get('timezone')
            },
            'fonts': {
                'enableMasking': self.result_set['fonts']['enableMasking'],
                'enableDomRect': self.result_set['fonts']['enableDomRect'],
                'families': self.result_set['fonts']['families']
            },
            'audioContext': {
                'enable': self.result_set['audioContext']['enable'],
                'noiseValue': self.result_set['audioContext']['noiseValue']
            },
            'canvas': {
                'mode': self.result_set['canvas']['mode'],
                'noise': self.result_set['canvas']['noise']
            },
            's3Date': self.result_set['s3Date'],
            's3Path': self.result_set['s3Path'],
            'devicePixelRatio': int(self.result_set['devicePixelRatio']),
            'owner': self.result_set['owner'],
            'autoProxyPassword': '',
            'autoProxyServer': '',
            'autoProxyUsername': '',
            'canBeRunning': True,
            'checkCookies': False,
            'debugMode': False,
            'dns': '',
            'extensions': {
                'enabled': self.result_set['extensions']['enabled'],
                'preloadCustom': self.result_set['extensions']['preloadCustom'],
                'names': self.result_set['extensions']['names']
            },
            'languages': self.tz.get('languages'),
            'lockEnabled': False,
            'isBookmarksSynced': self.result_set['isBookmarksSynced'],
             "webgl":{
                "metadata":{
                    "mode":True,
                    "renderer" : self.result_set['webgl']['metadata']['renderer'],
                    "vendor" : self.result_set['webgl']['metadata']['vendor']
                    }
                },
            'webGlParamsValues' : self.result_set['webGlParamsValues'],
            "clientRects":{
                "mode":"noise",
                "noise": round(random.uniform(0, 1), 8),
            },
            'canvasMode': self.result_set['canvasMode'],
            'client_rects_noise_enable': self.result_set['client_rects_noise_enable'],
            'audioContextMode': self.result_set['audioContextMode'],
            'autoLang': True,
            'chromeExtensions': self.result_set['chromeExtensions'],
            'hardwareConcurrency': self.result_set['hardwareConcurrency'],
            'proxy': {
                'id': '',
                'mode': 'http',
                'host': '',
                'port': '',
                'autoProxyRegion': '',
                'torProxyRegion': '',
                'username': '',
                'password': '',
                'changeIpUrl': ''
            },
            'proxyEnabled': False,
            'startUrl': self.result_set['startUrl'],
            'userAgent': self.result_set['userAgent'],
            'userChromeExtensions': self.result_set['userChromeExtensions'],
            'googleServicesEnabled': self.result_set['googleServicesEnabled']
        }
        if self.result_set['navigator']['platform'] == 'Android':
            print("mobile used")
            main_data["mobile"]={
                "device_scale_factor": random.uniform(2.10, 4.99),
                "enable":True,
                "height":int(self.result_set['screenHeight']),
                "width":int(self.result_set['screenWidth'])
            }
            main_data['permissions']={
                'transferProfile': self.result_set['permissions']['transferProfile'],
                'transferToMyWorkspace': self.result_set['permissions']['transferToMyWorkspace'],
                'shareProfile': self.result_set['permissions']['shareProfile'],
                'manageFolders': self.result_set['permissions']['manageFolders'],
                'editProfile': self.result_set['permissions']['editProfile'],
                'deleteProfile': self.result_set['permissions']['deleteProfile'],
                'cloneProfile': self.result_set['permissions']['cloneProfile'],
                'exportProfile': self.result_set['permissions']['exportProfile'],
                'updateUA': self.result_set['permissions']['updateUA'],
                'addVpnUfoProxy': self.result_set['permissions']['addVpnUfoProxy'],
                'runProfile': self.result_set['permissions']['runProfile'],
                'viewProfile': self.result_set['permissions']['viewProfile'],
                'addProfileTag': self.result_set['permissions']['addProfileTag'],
                'removeProfileTag': self.result_set['permissions']['removeProfileTag']
            }
            main_data['geolocation']={
                'mode': self.result_set['geolocation']['mode'],
                'latitude': self.result_set['geolocation']['latitude'],
                'longitude': self.result_set['geolocation']['longitude'],
                'accuracy': self.result_set['geolocation']['accuracy'],
                'isCustomCoordinates': self.result_set['geolocation']['isCustomCoordinates'],
                'customize': self.result_set['geolocation']['customize'],
                'enabled': self.result_set['geolocation']['enabled'],
                'fillBasedOnIp': True
            }
            main_data['mediaDevices'] = {
                'enableMasking': self.result_set['mediaDevices']['enableMasking'],
                'uid': self.result_set['mediaDevices']['uid']
            }
            main_data['plugins'] = {
                'enableVulnerable': True,
                'enableFlash': True
            }
            main_data['webGL']={
                'mode': 'noise',
                'noise': self.result_set['webGL']['noise'],
                'getClientRectsNoise': self.result_set['webGL']['getClientRectsNoise']
            }
            main_data['webRtc'] = {
                'mode': self.result_set['webRtc']['mode'],
                'enabled': self.result_set['webRtc']['enabled'],
                'customize': self.result_set['webRtc']['customize'],
                'localIpMasking': self.result_set['webRtc']['localIpMasking'],
                'fillBasedOnIp': self.result_set['webRtc']['fillBasedOnIp'],
                'publicIp': self.result_set['webRtc']['publicIp'],
                'localIps': self.result_set['webRtc']['localIps'],
                'enable': self.result_set['webRtc']['enable']
            }
            main_data['webRTC'] = {
                'mode': self.result_set['webRTC']['mode'],
                'enabled': self.result_set['webRTC']['enabled'],
                'customize': self.result_set['webRTC']['customize'],
                'localIpMasking': self.result_set['webRTC']['localIpMasking'],
                'fillBasedOnIp': True,
                'publicIp': '',
                'localIps': [],
                'enable': True
            }
            main_data['webGLMetadata']={
                "renderer" : self.result_set['webgl']['metadata']['renderer'],
                "vendor" : self.result_set['webgl']['metadata']['vendor']
            }
            main_data['storage'] = {
                'local': self.result_set['storage']['local'],
                'extensions': self.result_set['storage']['extensions'],
                'bookmarks': self.result_set['storage']['bookmarks'],
                'history': self.result_set['storage']['history'],
                'passwords': self.result_set['storage']['passwords'],
                'session': self.result_set['storage']['session'],
                'indexedDb': self.result_set['storage']['indexedDb']
            }
        
        elif self.result_set['navigator']['platform'] == 'linux armv81':
            self.webglnoise = round(random.uniform(20, 40), 2)
            main_data["mobile"]={
                "device_scale_factor":random.uniform(2.10, 4.99),
                "enable":False,
                "height":int(self.result_set['screenHeight']),
                "width":int(self.result_set['screenWidth'])
            }
            main_data['canvasNoise'] = self.result_set['canvasNoise']
            main_data['geolocation']= {
                'mode': self.result_set['geolocation']['mode'],
                'latitude': self.result_set['geolocation']['latitude'],
                'longitude': self.result_set['geolocation']['longitude'],
                'accuracy': self.result_set['geolocation']['accuracy'],
            }
            main_data['is_m1'] = False
            main_data['langHeader'] = self.lanval
            main_data['mediaDevices'] = {
                'enableMasking': self.result_set['mediaDevices']['enableMasking'],
                'uid': self.result_set['mediaDevices']['uid'],
                'audioInputs' : random.randint(0,5),
                'audioOutputs' : random.randint(0,4),
                'videoInputs' : random.randint(0,4)
            }
            main_data['plugins'] = {
                'all_enable': True,
                'flash_enable': True
            },
            main_data['startupUrl'] = ""
            main_data['startup_urls']=[""]
            main_data['unpinable_extension_names']=["passwords-ext"]
            main_data['webGl'] = {
                'mode': True,
                "renderer" : self.result_set['webgl']['metadata']['renderer'],
                "vendor" : self.result_set['webgl']['metadata']['vendor']
            }      
            main_data['webRtc'] = {
            'mode': self.result_set['webRtc']['mode'],
            'localIpMasking': self.result_set['webRtc']['localIpMasking'],
            'fillBasedOnIp': self.result_set['webRtc']['fillBasedOnIp'],
            'publicIp': self.result_set['webRtc']['publicIp'],
            }
            main_data['webglNoiseEnable'] = False
            main_data['webglNoiseValue'] = self.webglnoise
            main_data['webgl_noice_enable'] = False
            main_data['webgl_noise_enable'] = False
            main_data['webgl_noise_value'] = self.webglnoise
            main_data['webGLMetadata']={
                "renderer" : self.result_set['webgl']['metadata']['renderer'],
                "vendor" : self.result_set['webgl']['metadata']['vendor']
            }
            main_data['storage'] = {
                'local': self.result_set['storage']['local'],
                'extensions': self.result_set['storage']['extensions'],
                'bookmarks': self.result_set['storage']['bookmarks'],
                'history': self.result_set['storage']['history'],
                'passwords': self.result_set['storage']['passwords'],
                'session': self.result_set['storage']['session'],
                'indexedDb': self.result_set['storage']['indexedDb']
            }
        
        elif self.result_set['navigator']['platform'] == 'win32':
            self.webglnoise = round(random.uniform(20, 40), 2)
            self.webglnoice = round(random.uniform(1, 20), 6)
            main_data["mobile"]={
                "device_scale_factor":random.uniform(2.10, 4.99),
                "enable":False,
                "height":int(self.result_set['screenHeight']),
                "width":int(self.result_set['screenWidth'])
            }
            main_data['canvasNoise'] = self.result_set['canvasNoise']
            main_data['geolocation']= {
                'mode': self.result_set['geolocation']['mode'],
                'latitude': self.result_set['geolocation']['latitude'],
                'longitude': self.result_set['geolocation']['longitude'],
                'accuracy': self.result_set['geolocation']['accuracy'],
            }
            main_data['is_m1'] = False
            main_data['langHeader'] = self.lanval
            main_data['mediaDevices'] = {
                'enableMasking': self.result_set['mediaDevices']['enableMasking'],
                'uid': self.result_set['mediaDevices']['uid'],
                'audioInputs' : random.randint(0,5),
                'audioOutputs' : random.randint(0,4),
                'videoInputs' : random.randint(0,4)
            }
            main_data['plugins'] = {
                'all_enable': True,
                'flash_enable': True
            },
            main_data['startupUrl'] = ""
            main_data['startup_urls']=[""]
            main_data['unpinable_extension_names']=["passwords-ext"]
            main_data['webGl'] = {
                'mode': True,
                "renderer" : self.result_set['webgl']['metadata']['renderer'],
                "vendor" : self.result_set['webgl']['metadata']['vendor']
            }      
            main_data['webRtc'] = {
            'mode': self.result_set['webRtc']['mode'],
            'localIpMasking': self.result_set['webRtc']['localIpMasking'],
            'fillBasedOnIp': self.result_set['webRtc']['fillBasedOnIp'],
            'publicIp': self.result_set['webRtc']['publicIp'],
            }
            main_data['webglNoiseEnable'] = False
            main_data['webglNoiseValue'] = self.webglnoise
            main_data['webgl_noice_enable'] = False
            main_data['webgl_noise_enable'] = False
            main_data['webgl_noise_value'] = self.webglnoise
            main_data['getClientRectsNoice'] = self.webglnoice
            main_data['get_client_rects_noise'] = self.webglnoice
            main_data['storage'] = {
                'local': self.result_set['storage']['local'],
                'extensions': self.result_set['storage']['extensions'],
                'bookmarks': self.result_set['storage']['bookmarks'],
                'history': self.result_set['storage']['history'],
                'passwords': self.result_set['storage']['passwords'],
                'session': self.result_set['storage']['session'],
                'indexedDb': self.result_set['storage']['indexedDb']
            }
        elif self.result_set['navigator']['platform'] == 'macintel' or 'iphone':
            self.webglnoise = round(random.uniform(20, 40), 2)
            self.webglnoice = round(random.uniform(1, 20), 6)
            self.canvasnoise = round(random.uniform(0,5), 8)
            main_data['storage'] = {
                'enable': True
            }
            main_data["mobile"]={
                "device_scale_factor":random.uniform(2.10, 4.99),
                "enable":False,
                "height":int(self.result_set['screenHeight']),
                "width":int(self.result_set['screenWidth'])
            }
            main_data['canvasNoise'] = self.result_set['canvasNoise']
            main_data['geolocation']= {
                'mode': self.result_set['geolocation']['mode'],
                'latitude': self.result_set['geolocation']['latitude'],
                'longitude': self.result_set['geolocation']['longitude'],
                'accuracy': self.result_set['geolocation']['accuracy'],
            }
            main_data['is_m1'] = False
            main_data['langHeader'] = self.lanval
            main_data['mediaDevices'] = {
                'enableMasking': self.result_set['mediaDevices']['enableMasking'],
                'uid': self.result_set['mediaDevices']['uid'],
                'audioInputs' : random.randint(0,5),
                'audioOutputs' : random.randint(0,4),
                'videoInputs' : random.randint(0,4)
            }
            main_data['plugins'] = {
                'all_enable': True,
                'flash_enable': True
            },
            main_data['startupUrl'] = ""
            main_data['startup_urls']=[""]
            main_data['unpinable_extension_names']=["passwords-ext"]
            main_data['webGl'] = {
                'mode': True,
                "renderer" : self.result_set['webgl']['metadata']['renderer'],
                "vendor" : self.result_set['webgl']['metadata']['vendor']
            }      
            main_data['webRtc'] = {
            'mode': self.result_set['webRtc']['mode'],
            'localIpMasking': self.result_set['webRtc']['localIpMasking'],
            'fillBasedOnIp': self.result_set['webRtc']['fillBasedOnIp'],
            'publicIp': self.result_set['webRtc']['publicIp'],
            }
            main_data['webglNoiseEnable'] = False
            main_data['webglNoiceEnable'] = False
            main_data['webglNoiseValue'] = self.webglnoise
            main_data['webgl_noice_enable'] = False
            main_data['webgl_noise_enable'] = False
            main_data['webgl_noise_value'] = self.webglnoise
            main_data['getClientRectsNoice'] = self.webglnoice
            main_data['get_client_rects_noise'] = self.webglnoice
            main_data['canvasNoise'] = self.canvasnoise
        
        self.main_data = main_data  # Store main_data as an instance variable
        # Save profile data to the Chrome Preferences file
        loc_path = os.path.join(self.main_path, 'Default', 'Preferences')
        data_loc = json.loads(open(loc_path, 'r').read())
        data_loc['gologin'] = main_data
        myval=json.dumps(data_loc)
        open(loc_path, 'w').write(myval)

    def launch_browser(self):
        folder_path = ''
        gologin_path = ''
        for root, dirs, files in os.walk('/'):
            if '.ownbrowser' in dirs:
                folder_path = os.path.join(root, '.ownbrowser', 'browser')
                break
        if not folder_path:
            print('no gologin found')

        if folder_path:
            main_path_list = []
            for path_var in os.listdir(folder_path):
                if '.zip' not in path_var and '.tar.gz' not in path_var:
                    if 'orbita-browser' in path_var:
                        if os.name == 'nt':
                            gologin_path = os.path.join(folder_path, path_var, 'chrome.exe')
                            main_path_list.append(gologin_path)
                        else:
                            gologin_path = os.path.join(folder_path, path_var, 'chrome')
                            main_path_list.append(gologin_path)
            gologin_path = random.choice(main_path_list)
            if gologin_path == '':
                for path_var in os.listdir(folder_path):
                    if '.zip' in path_var:
                        with zipfile.ZipFile(os.path.join(folder_path, path_var), 'r') as zip_ref:
                            main_path = re.sub('.zip', '', path_var)
                            zip_ref.extractall(os.path.join(folder_path, main_path))
                            if os.name == 'nt':
                                gologin_path = os.path.join(folder_path, main_path, 'chrome.exe')
                            else:
                                gologin_path = os.path.join(folder_path, main_path, 'chrome')
                            break

        self.executablePath = gologin_path
        self.extension_path = os.path.join(os.getcwd(), 'chromeext')
        self.random_port = getRandomPort()
        
        self.process = subprocess.Popen(
            [f"{self.executablePath}", f"--remote-debugging-port={self.random_port}", 
             f"--remote-allow-origins=*", f"--user-data-dir={self.main_path}", 
             f"--password-store=basic", f"--tz={self.result_set['timezone']['id']}", 
             f"--gologin-profile={self.profile_name}", f"--lang={self.result_set['languages']}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        
    def get_time_zone(self):
        data = requests.get('https://time.gologin.com')
        return json.loads(data.content.decode('utf-8')) 
    
    def get_time_zone_proxy(self):
        data = requests.get('https://time.gologin.com')
        return json.loads(data.content.decode('utf-8'))   
        
    def UserProfileGenerator(self,useragent_path, hardware_path, maxtouchpoints_path,
                 devicememory_path, language_path, webgl_path, mediadevice_path, os_path, resolution_path,
                 devicepixel_path,):
        self.fake = Faker()
        self.tz = self.get_time_zone()
        self.timezone = self.tz.get('timezone')
        self.useragent_df = pd.read_parquet(useragent_path)
        self.hardware_df = pd.read_parquet(hardware_path)
        self.maxtouchpoints_df = pd.read_parquet(maxtouchpoints_path)
        self.devicememory_df = pd.read_parquet(devicememory_path)
        self.language_df = pd.read_parquet(language_path)
        self.webgl_df = pd.read_parquet(webgl_path)
        self.mediadevice_df = pd.read_parquet(mediadevice_path)
        self.os_df = pd.read_parquet(os_path)
        self.res_df = pd.read_parquet(resolution_path)
        self.devicepixel_df = pd.read_parquet(devicepixel_path)  
        self.wmtval = random.choice(self.webgl_df['webGlMetaData'].to_list())
        self.wpmval = random.choice(self.webgl_df['webGlParamsValues'].to_list())  
        self.mtpval = random.choice(self.maxtouchpoints_df['maxtouchpoints'].to_list())
        self.hwval = random.choice(self.hardware_df['hardwareConcurrency'].to_list())
        self.userval = random.choice(self.useragent_df['useragent'].to_list())
        self.dmval = random.choice(self.devicememory_df['devicememory'].to_list())
        self.lanval = random.choice(self.language_df['language'].to_list())
        self.mdval = random.choice(self.mediadevice_df['mediadevice'].to_list())
        self.osval = random.choice(self.os_df['os'].to_list())
        self.resval = random.choice(self.res_df['resolution'].to_list())
        self.dpval = random.choice(self.devicepixel_df['devicepixelratio'].to_list())
        self.webglmeta = json.loads(self.wmtval)
        self.webglparam = json.loads(self.wpmval)
        self.webgl={}
        if 'unmaskedRenderer' in self.webglmeta:
            self.webgl['vendor']=self.webglmeta['unmaskedVendor']
            self.webgl['renderer']=self.webglmeta['unmaskedRenderer']
        else:
            self.webgl['vendor']=self.webglmeta['vendor']
            self.webgl['renderer']=self.webglmeta['renderer']
        
        result = {}

        result['navigator'] = {
            'platform': self.useragent_df['platform'].iloc[0]
        }
        
        result['navigator']['userAgent'] = self.userval
        
        result['navigator']['hardwareConcurrency'] = int(self.hwval)
        
        result['navigator']['resolution'] = self.resval
        
        result['navigator']['maxTouchPoints'] = self.mtpval

        result['navigator']['deviceMemory'] = self.dmval

        result['navigator']['language'] = self.tz.get('languages')

        bookmarks = {
            'bookmark_bar': {
                'children': [
                    {
                        'type': 'folder',
                        'name': 'Southwest',
                        'children': [{'name': 'Southwest', 'type': 'url', 'url': ''}]
                    }
                ],
                'name': 'Bookmarks bar',
                'type': 'folder'
            },
            'other': {
                'children': [],
                'name': 'Other bookmarks',
                'type': 'folder'
            },
            'synced': {
                'children': [],
                'name': 'Mobile bookmarks',
                'type': 'folder'
            }
        }
        
        result.update({
            'name': "",
            'id': str(uuid.uuid4()).replace('-', ''),
            'notes': '',
            'browserType': 'chrome',
            'os': self.osval,
            'bookmarks': bookmarks,
            'profile_id': str(uuid.uuid4()).replace('-', ''),
            'deviceMemory' : self.dmval,
            'timezone': {
                'id': self.timezone,
            },
            'extensions': {
                'enabled': True,
                'preloadCustom': True,
                'names': random.sample(['humanTyping','AutomationTask','TypeSupport','SnippetPlus','screenRecorder','DictionaryPro','TypoMaster','DocEval','ScannerPro','FileRead','FileShare'],4),
            },
            'screenWidth': self.resval.split('x')[1],
            'screenHeight': self.resval.split('x')[0],
            'storage': {
                'local': True,
                'extensions': True,
                'bookmarks': True,
                'history': True,
                'passwords': True,
                'session': True,
                'indexedDb': False,
            },
            'plugins': {
                'enableVulnerable': True,
                'enableFlash': True,
            },
            'geolocation': {
                'mode': 'prompt',
                'latitude': float(self.tz.get('ll', [0, 0])[0]),
                'longitude': float(self.tz.get('ll', [0, 0])[1]),
                'accuracy': self.tz.get('accuracy', 0),
                'isCustomCoordinates': False,
                'customize': True,
                'enabled': True,
                'fillBasedOnIp': True,
            },
            'fonts': {
                'enableMasking': True,
                'enableDomRect': True,
                'families': '',
            },
            'audioContext': {
                'enable': True,
                'noiseValue': float(f'{random.uniform(1e-10, 1e-7):.12e}')
            },
            'canvas': {
                'mode': 'noise',
                'noise': round(random.uniform(0, 1), 8),
            },
            'canvasNoise': round(random.uniform(0, 1), 8), 
            's3Date': '',
            's3Path': 'zero_profile.zip',
            'devicePixelRatio': round(float(self.dpval)),
            'owner': str(uuid.uuid4()).replace('-', '')[:58],
            'autoProxyPassword': '',
            'autoProxyServer': '',
            'autoProxyUsername': '',
            'canBeRunning': True,
            'checkCookies': False,
            'debugMode': False,
            'dns': '',
            'languages': self.tz.get('languages'),
            'lockEnabled': False,
            'isBookmarksSynced': True,
            'mediaDevices': {
                'enableMasking': True,
                'uid': (str(uuid.uuid4()) + str(uuid.uuid4())).replace('-', '')[:58],
            },
            'webRTC': {
                'mode': 'alerted',
                'enabled': True,
                'customize': True,
                'localIpMasking': True,
                'fillBasedOnIp': True,
                'publicIp': '',
                'localIps': [],
                'enable': True,
            },
            'webGL': {
                'mode': 'noise',
                'noise': round(random.uniform(0, 100), 3),
                'getClientRectsNoise': round(random.uniform(0, 100), 5)
            },
            "webgl":{
                "metadata":{
                    "mode":True,
                    "renderer" : self.webgl['renderer'],
                    "vendor" : self.webgl['vendor']
                    }
                },
            'webGLMetadata' : self.webglmeta,
            'webGlParamsValues' : self.webglparam,
            'webRtc': {
                'mode': 'alerted',
                'enabled': True,
                'customize': True,
                'localIpMasking': True,
                'fillBasedOnIp': True,
                'publicIp': '',
                'localIps': [],
                'enable': True,
            },
            'canvasMode': 'noise',
            'client_rects_noise_enable': True,
            'audioContextMode': 'noise',
            'permissions': {
                'transferProfile': True,
                'transferToMyWorkspace': True,
                'shareProfile': True,
                'manageFolders': True,
                'editProfile': True,
                'deleteProfile': True,
                'cloneProfile': True,
                'exportProfile': True,
                'updateUA': True,
                'addVpnUfoProxy': True,
                'runProfile': True,
                'viewProfile': True,
                'addProfileTag': True,
                'removeProfileTag': True,
            },
            'autoLang': True,
            'chromeExtensions': [],
            'hardwareConcurrency': int(self.hwval),
            'proxy': {
                'id': str(uuid.uuid4()).replace('-', ''),
                'mode': '',
                'host': '',
                'port': '',
                'autoProxyRegion': '',
                'torProxyRegion': '',
                'username': '',
                'password': '',
                'changeIpUrl': None
            },
            'proxyEnabled': False,
            'startUrl': '',
            'userAgent': self.userval,
            'userChromeExtensions': [],
            'googleServicesEnabled': True,
        })
        self.result=result
        return self.result
        
    
    def terminate_and_delete_profiles(profile_name):
        profile_data_path = os.path.join(os.getcwd(),'profile_data')
        if os.path.exists(profile_data_path):
            try:
                shutil.rmtree(profile_data_path)
            except OSError as e:
                print(f"Error: {e}")


            print(f"Deleted existing profile_data directory: {profile_name}")
            

def kill_chrome_by_port(random_port):
        for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
            try:
                if 'chrome' in process.info['name'].lower():
                    for arg in process.info['cmdline']:
                        if f'--remote-debugging-port={random_port}' in arg:
                            process.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    
def stop(random_port):
    kill_chrome_by_port(random_port)
     
    
def create_and_run_profile(profile_name):
    instance = IntegratedDataGenerator(profile_name)
    instance.UserProfileGenerator(
        useragent_path=os.path.join(os.getcwd(), f'parquet_files/{instance.platform_type}/useragent.parquet'),
        hardware_path=os.path.join(os.getcwd(), f'parquet_files/{instance.platform_type}/hardwareConcurrency.parquet'),
        maxtouchpoints_path=os.path.join(os.getcwd(), f'parquet_files/{instance.platform_type}/maxtouchpoints.parquet'),
        devicememory_path=os.path.join(os.getcwd(), f'parquet_files/{instance.platform_type}/devicememory.parquet'),
        language_path=os.path.join(os.getcwd(), f'parquet_files/{instance.platform_type}/language.parquet'),
        webgl_path=os.path.join(os.getcwd(), f'parquet_files/{instance.platform_type}/webgl.parquet'),
        mediadevice_path=os.path.join(os.getcwd(), f'parquet_files/{instance.platform_type}/mediadevice.parquet'),
        os_path=os.path.join(os.getcwd(), f'parquet_files/{instance.platform_type}/os.parquet'),
        resolution_path=os.path.join(os.getcwd(), f'parquet_files/{instance.platform_type}/resolution.parquet'),
        devicepixel_path=os.path.join(os.getcwd(), f'parquet_files/{instance.platform_type}/devicepixelratio.parquet')
    )   
    instance.create_profile()
    instance.launch_browser()
    time.sleep(1000)
    stop(instance.random_port)
    instance.terminate_and_delete_profiles()
    time.sleep(5)
    
def run_processes():
    # Run two instances simultaneously
    processes = []
    instance = IntegratedDataGenerator()
    iterations = 30 # Adjust the number of iterations as needed

    for _ in range(iterations):  
        fake = Faker()
        profile_name = fake.name()
        instance.profile_name = profile_name
        create_and_run_profile(profile_name)

    # Wait for all processes to finish (if they haven't terminated)
    for process in processes:
        process.join()

if __name__ == '__main__':
    exec_obj = concurrent.futures.ThreadPoolExecutor()
    profile_count = 1
    threads=[]
    for i in range(profile_count):
        threads.append(exec_obj.submit(run_processes))
        
    for thread in threads:
        thread.result()
