# 智慧商情/求购信息/接口文档

客户端调用服务器提供的Web接口:

- hint.json
- poll.json
- fetch.json
- contact.json

服务器返回JSON数据格式:

    {
        "code": <code>, # 返回码(公共字段)
        "msg":  <msg>,  # 提示语(公共字段)
        "time": <time>, # 时间戳(公共字段)
        "data": <data>  # 数据
    }

返回码对照表:

    code    msg
    ----    ---
    200     OK
    400     Client Error
    500     Server Error

> 另外, 请求/响应, 统一使用UNIX时间戳(类型:`float`, 单位:`second`), 来表示时间.

----

## hint.json

### 用途

获取指定时间范围内, 指定分类编号的, 新增的求购数量

### 参数

- `sites`: 站点名称(可选), 多个站点之间用逗号分割
- `cates`: 分类编号(必填), 多个编号之间用逗号分割
- `mintime`: 最小时间(可选), 默认值为:0
- `maxtime`: 最大时间(可选), 默认值为:+∞

### 返回

- `data`: 数据
    - `key`: 分类编号
    - `value`: 求购数量, 若值为`null`, 则该分类不存在

### 示例


    # HTTP请求
    curl 'http://localhost:9090/hint.json?cates=53,57,58,9999&mintime=1400728660.000'

    # HTTP响应
    {
        "code": 200,
        "msg": "OK",
        "time": 1400729292.232,
        "data": {
            "53": 0,
            "57": 2,
            "58": 4,
            "9999": null
        }
    }

## poll.json

### 用途

获取指定时间范围内, 指定分类编号的, 新增的求购列表

### 参数

- `sites`: 站点名称(可选), 多个站点之间用逗号分割
- `cates`: 分类编号(必填), 多个编号之间用逗号分割
- `mintime`: 最小时间(可选), 默认值为:0
- `maxtime`: 最大时间(可选), 默认值为:+∞

### 返回

- `data`: 数据

### 示例

    # HTTP请求
    curl 'http://localhost:9090/poll.json?cates=57,58&mintime=1400728660.000'

    # HTTP响应
    {
        "code": 200,
        "msg": "OK",
        "time": 1400729292.232,
        "data": [
            {"time": 1400728696.000, "site":"alibaba", "oid":"666666", "url":"http://go.1688.com/buyoffer/666666.htm", "title":"cccccc", "cates":["58"]},
            {"time": 1400728694.000, "site":"alibaba", "oid":"555555", "url":"http://go.1688.com/buyoffer/555555.htm", "title":"bbbbbb", "cates":["58", "1046758"]},
            {"time": 1400728692.000, "site":"alibaba", "oid":"444444", "url":"http://go.1688.com/buyoffer/444444.htm", "title":"aaaaaa", "cates":["58", "121192010", "1046762"]},
            {"time": 1400728690.000, "site":"alibaba", "oid":"333333", "url":"http://go.1688.com/buyoffer/333333.htm", "title":"zzzzzz", "cates":["58"]},
            {"time": 1400728680.000, "site":"alibaba", "oid":"222222", "url":"http://go.1688.com/buyoffer/222222.htm", "title":"yyyyyy", "cates":["57", "122250002", "122218012"]},
            {"time": 1400728670.000, "site":"alibaba", "oid":"111111", "url":"http://go.1688.com/buyoffer/111111.htm", "title":"xxxxxx", "cates":["57", "1043726"]}
        ]
    }

## fetch.json

### 用途

获取指定站点的，指定求购编号的求购详情

### 参数

- `site`: 站点名称(必填), 取值范围: `alibaba`
- `oid`: 求购编号(必填), 必须于`site`相对应

### 返回

- `data`: 数据(待定)

### 示例

    # HTTP请求
    curl 'http://localhost:9090/fetch.json?site=alibaba&oid=33656618'

    # HTTP响应
    {
      "code": 200,
      "msg": "OK"
      "time": 1400907988.005676,
      "data": {
        "buyer": "青岛卡乐夫贸易有限公司",
        "time": 1400904008,
        "cates": [
          "2",
          "229"
        ],
        "buy_list": [
          {
            "desc": null,
            "img": null,
            "unit": "kg",
            "product": "多春鱼籽",
            "count": 1000
          }
        ],
        "addr": "山东青岛",
        "title": "蟹黄鱼籽--染色多春鱼籽",
        "url": "http://go.1688.com/buyoffer/33656618.htm",
        "oid": "33656618",
        "mid": "b2b-1740827997",
        "site": "alibaba",
        "req_list": [
          {
            "extra_info": "多春鱼籽染色（蟹黄色）",
            "invoice": "无需发票",
            "payment": "支付宝担保交易",
            "rcv_addr": "山东 青岛 即墨市"
          }
        ]
      }
    }
    
## contact.json

### 用途

获取指定站点的，指定用户编号的联系信息

### 参数

- `site`: 站点名称(必填), 取值范围: `alibaba`
- `mid`: 用户编号(必填), 必须于`site`相对应

### 返回

- `data`: 数据

### 示例

    # HTTP请求
    curl 'http://localhost:9090/contact.json?site=alibaba&mid=b2b-1740827997'

    # HTTP响应
    {
      "code": 200,
      "msg": "OK",
      "time": 1400907431.057254,
      "data": {
        "site": "alibaba",
        "mid": "b2b-1740827997",
        "contact": "王海涛 先生 （总经理）",
        "phone": "86 0532 15253220238",
        "mobile": "15253220238",
        "address": "中国 山东 青岛市崂山区青大一路9号"
      }
    }

