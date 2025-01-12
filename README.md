# wechat-miniprogram-payment
这是一个Python语言通过fastapi框架搭建服务端，实现微信小程序端进行微信支付案例项目。

# 安装环境依赖

```
pip install -r requirements.txt -i [镜像地址]
```



# 项目配置数据调整

![image](https://github.com/user-attachments/assets/b82f87c5-2a43-4de6-8e94-39f7404cb82e)

![image](https://github.com/user-attachments/assets/b4557dba-5c95-4fa3-b55d-eaf76a36ade9)

![image](https://github.com/user-attachments/assets/a9ae4128-f06d-4aa5-b310-d96a37bcdf1e)

**腾讯案例私钥（需要调整配置自己的私钥）**

![image](https://github.com/user-attachments/assets/0d6a7b0a-835e-4192-a085-c03dcfef9129)



# 启动服务器

点击 launch.bat 执行启动服务器程序

```
uvicorn app:app --host 0.0.0.0 --port 5000
```





# 微信小程序端

封装微信 wx.request 请求：**./utils/request.js**

```js
class Request {
	constructor(host, port) {
		this.host = host;
		this.port = port;
	}

	get(url, data) {
		return this.request('GET', url, data)
	}
	post(url, data) {
		return this.request('POST', url, data)
	}

	request(method, url, data) {
		const URL = this.host + ":" + this.port + url;
		return new Promise((resolve, reject) => {
			wx.request({
				url: URL,
				data,
				method,
				success: res => {
					if (res.statusCode == 200) {
						resolve(res)
					} else {
						reject(res)
					}
				},
				fail: res => {
					reject({
						message: res.errMsg,
						url: URL,
						method,
						data,
						statusCode: res.statusCode,
						result: res.data
					})
				}
			})
		})
	}
}

const request = new Request("http://127.0.0.1", 5000)
module.exports = request
```

统一管理接口：**./utils/api.js**

```js
import request from './request.js'

class Http {
    Login(data) {
        return request.post('/login', data)
	}
	WechatPay(data) {
		return request.post('/wechat/pay', data)
	}
}
const api = new Http()
export default api
```

测试页面：**./pages/index/index.js**

```js
import api from '../../utils/api.js'
Page({
	WechatPay() {
		api.WechatPay({
			description: "付费会员",
			amount_total: 100 // 100 分 = 1 元
		}).then(res => {
			if (res.data.code == 200) {
				console.log(res.data)
				let payment = res.data.data
				wx.requestPayment({
					"timeStamp": payment.timeStamp,
					"nonceStr": payment.nonceStr,
					"package": payment.package,
					"signType": "RSA",
					"paySign": payment.paySign,
					"success": res => {
						console.log(res)
					},
					"fail": err => {
						console.log(err)
					},
					"complete": res => {
						console.log(res)
					}
				})
			}
		})
		
	},
	data: {

	},

	onLoad(options) {

	}
})
```

```html
<view class="contain">
	<view>微信支付测试</view>
	<button bind:tap="WechatPay">支付 1 元</button>
</view>
```

