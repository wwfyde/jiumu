// 假数据
// const baseUrl = 'https://www.fastmock.site/mock/36329655758cd689742ae22a1a1b5b2d/intention'
// TODO 服务器地址配置
const baseUrl = "http://10.222.26.183:8188"
// const baseUrl = "http://127.0.0.1:8188"
const qs = Qs
// 响应时间
// axios.defaults.timeout = 40000
/* 配置请求头 */
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
// 配置接口地址
axios.defaults.baseURL = baseUrl

axios.interceptors.response.use((res) => {
  // 对响应数据做些事
  if (res.data.code === 1) {
    return Promise.resolve(res)
  }
  return res
}, (error) => {

  return Promise.reject(error)
})

// 公共POST请求
let fetch_POST = (url, params) => {
  return new Promise((resolve, reject) => {
    axios.post(url, params)
      .then(response => {
        resolve(response)
      }, err => {
        reject(err)
      })
      .catch((error) => {
        reject(error)
      })
  })
}

// 公共GET请求
let fetch_GET = (url, params) => {
  // params = qs.stringify(params)
  return new Promise((resolve, reject) => {
    axios.get(url, { params: params })
      .then(response => {
        resolve(response)
      }, err => {
        reject(err)
      })
      .catch((error) => {
        reject(error)
      })
  })
}

// 公共DELETE请求
let fetch_DELETE = (url, data) => {
  return new Promise((resolve, reject) => {
    axios.delete(url, { data: data })
      .then(response => {
        resolve(response)
      }, err => {
        reject(err)
      })
      .catch((error) => {
        reject(error)
      })
  })
}

