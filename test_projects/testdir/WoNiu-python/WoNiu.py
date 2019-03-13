#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, hashlib, os, random, urllib, urllib2
from datetime import *

class APIClient(object):
    def http_request(self, url, paramDict):
        post_content = ''
        for key in paramDict:
            post_content = post_content + '%s=%s&'%(key,paramDict[key])
        post_content = post_content[0:-1]
        #print post_content
        req = urllib2.Request(url, data=post_content)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
        response = opener.open(req, post_content)  
        return response.read()

    def http_upload_image(self, url, paramKeys, paramDict, filebytes):
        timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        boundary = '------------' + hashlib.md5(timestr).hexdigest().lower()
        boundarystr = '\r\n--%s\r\n'%(boundary)
        
        bs = b''
        for key in paramKeys:
            bs = bs + boundarystr.encode('ascii')
            param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s"%(key, paramDict[key])
            #print param
            bs = bs + param.encode('utf8')
        bs = bs + boundarystr.encode('ascii')
        
        header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/jpeg\r\n\r\n'%('sample')
        bs = bs + header.encode('utf8')
        
        bs = bs + filebytes
        tailer = '\r\n--%s--\r\n'%(boundary)
        bs = bs + tailer.encode('ascii')
        
        import requests
        headers = {'Content-Type':'multipart/form-data; boundary=%s'%boundary,
                   'Connection':'Keep-Alive',
                   'Expect':'100-continue',
                   }
        response = requests.post(url, params='', data=bs, headers=headers)
        return response.text


    


def arguments_to_dict(args):
    argDict = {}
    if args is None:
        return argDict
    
    count = len(args)
    if count <= 1:
        print 'exit:need arguments.'
        return argDict
    
    for i in [1,count-1]:
        pair = args[i].split('=')
        if len(pair) < 2:
            continue
        else:
            argDict[pair[0]] = pair[1]

    return argDict
    
    


if __name__ == '__main__':
    client = APIClient()
    while 1:
        paramDict = {}
        result = ''
        act = raw_input('Action:')
        if cmp(act, 'GetAccount') == 0: 
            paramDict['UserName'] = raw_input('username:')
            paramDict['PassWord'] = raw_input('password:')
            result = client.http_request('http://api.woniudama.com/ApiWeb/GetAccount', paramDict)
        elif cmp(act, 'ReportError') == 0:
            paramDict['UserName'] = raw_input('username:')
            paramDict['PassWord'] = raw_input('password:')        
            paramDict['ID'] = raw_input('id:')
            result = client.http_request('http://api.woniudama.com/ApiWeb/ReportError', paramDict)
        elif cmp(act, 'upload') == 0:
            paramDict['UserName'] = raw_input('username:')
            paramDict['PassWord'] = raw_input('password:') 
            paramDict['SoftID'] = raw_input('softid:') 
            paramKeys = ['UserName',
                 'PassWord', 
                 'SoftID', 
                ]
            from PIL import Image
            imagePath = raw_input('Image Path:')
            img = Image.open(imagePath)
            if img is None:
                print 'get file error!'
                continue
            img.save("upload.jpg")
            filebytes = open("upload.jpg", "rb").read()
            result = client.http_upload_image("http://api.woniudama.com/ApiWeb/Create", paramKeys, paramDict, filebytes)
			# 如果您自己的http请求是把图片转换为字符串提交,那请用http://api.woniudama.com/ApiWeb/CreateFromBase64接口提交,参数名不变,但是要求image参数是图片字节数组的base64表示形式
        elif cmp(act, 'exit') == 0:
            break
        
        print result