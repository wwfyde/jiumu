# 九牧坐席助手接口文档

## -1 坐席来电信息查询接口

> 根据坐席查询坐席最近通话
>

```http
GET http://127.0.0.1:8188/call_info/{agent}
```

### Request fileds

| Name  | Type   | Require | Description |
| ----- | ------ | ------- | ----------- |
| agent | String | True    | 坐席ID      |

### Response fileds

| Name         | Type   | Description                                                  |
| ------------ | ------ | ------------------------------------------------------------ |
| code         | Int    | 1:成功<br />2:接口失败<br />3:请求错误                       |
| message      | String | success: 请求接口成功<br />error: 接口错误<br />failed: 错误的请求 |
| data         | Object | 接口数据                                                     |
| data.call_id | String | 通话ID                                                       |
| data.phone   | String | 客户手机号                                                   |
| ...          | ...    | ...                                                          |

### 

## 0 意图获取接口

> 进线意图获取

```http
GET http://192.168.128.82:8188/intention
```

### 接口说明

从云问知识库接口实时获取客户意图

关于辅助页面的意图对接，请求云问的接口，获取意图填充 语音流打包的信息传递过来后，根据信息请求云问接口获取意图，

进线意图可能发生变化 需要持续获取

### Request fileds

| Name  | Type   | Require | Description |
| ----- | ------ | ------- | ----------- |
| phone | String | True    | 手机号码    |
| agent | String | True    | 坐席ID      |

请求示例

```json
{
    "phone": "13733339999"
}
```

### Response fileds

| Name           | Type    | Description                                                  |
| -------------- | ------- | ------------------------------------------------------------ |
| code           | Int     | 1:成功<br />2:接口失败<br />3:请求错误                       |
| message        | String  | success: 请求接口成功<br />error: 接口错误<br />failed: 错误的请求 |
| data           | Object  | 接口数据                                                     |
| intention      | Object  | 进线意图                                                     |
| intention.id   | Integer | 进线意图号                                                   |
| intention.name | String  | 意图名称                                                     |

### Example

```json
{
    "code": 1,
    "message": "success",
    "data": {
        "intention": {
            "name": "马桶维修",
            "id": 1002
        },
        ...
    }
}
```

### ERROR Example

接口错误

```json
{
    "code": 2,
    "message": "error",
    "data": ""
}
```

## 1 来电统计接口

```http
GET http://192.168.128.82:8188/call
```

### 接口说明

查询来电号码今日和本月的来电记录

与内部接口交互

### Request fileds

| Name  | Type   | Require | Description |
| ----- | ------ | ------- | ----------- |
| phone | String | True    | 来电手机号  |
| agent | String | True    | 坐席ID      |

请求示例

```json
{
    "phone": "13733334444",
    "agent": "23567"
}
```

### Response fileds

| Name    | Type   | Description                                                  |
| ------- | ------ | ------------------------------------------------------------ |
| code    | Int    | 1:成功<br />2:接口失败<br />3:请求错误                       |
| message | String | success: 请求接口成功<br />error: 接口错误<br />failed: 错误的请求 |
| data    | Object | 统计详情                                                     |
| today   | Int    | 今日来电统计                                                 |
| month   | Int    | 本月来电统计                                                 |
| mobile  | String | 手机号码                                                     |

### Example

```json
{
    "code": 1,
    "message": "success",
    "data": {
        "today": 0,
        "month": 3
    }
}
```

### ERROR Response

接口错误

```json
{
    "code": 2,
    "message": "error",
    "data": ""
}
```

## 2.1 查询问题标签列表

> 相关解释
>
> 查询TOP问题

```http
GET http://192.168.128.82:8188/question
```

### 接口说明

根据实时对话信息, 查询知识并获取问题标签列表 最多展示20条, 并支持增加或删除功能

需要查询外部接口

### Request fileds

| Name           | Type    | Require | Description                 |
| -------------- | ------- | ------- | --------------------------- |
| call_id        | String  | True    | 通话ID 用于标识标签所属通话 |
| agent          | String  | True    | 坐席ID                      |
| intention      | Integer | True    | 进线意图号码                |
|                |         |         |                             |
| intention_name | String  | False   | 进线意图名称                |
|                |         |         |                             |

请求示例

```json
{
    "intention": 1001,
    "call_id": "8c6d5237-a08c-4a71-adfd-df0a0ee37af0",
    "agent": 23459,
    "gid":1
}
```

### Response fileds

| Name                  | Type   | Description                                                  |
| --------------------- | ------ | ------------------------------------------------------------ |
| code                  | Int    | 1:成功<br />2:接口失败<br />3:请求错误                       |
| message               | String | success: 请求接口成功<br />error: 接口错误<br />failed: 错误的请求 |
| data                  | List   | 数据对象 问题列表[question1, question2, ...]                 |
| question              | Object | 问题(标签)对象                                               |
| question.question     | String | 问题名称                                                     |
| question.time         | String | 问题生成时间 格式: YYYY-MM-DD hh:mm:ss                       |
| question.knowledge_id | Int    | 问题知识ID                                                   |
| question.source       | Int    | 问题来源 1:语音流, 2:搜索检索, 3: 热点问题                   |

### Request Example

```json
{
    "code": 1,
    "message": "success",
    "data": [
        {
            "question": "问题名称1",
            "time": "2022-02-13 12:53:53"
        },
        {
            "question": "问题名称2",
            "time": "2022-02-13 12:51:53"
        }
    ]
}
```

```json
// 根据进线意图获取TOP问题 原始接口 仅供参考

{
    "code": 1,
    "data": {
        "questionList": [
            {
                "id": 654,
                "domainId": 0,
                "question": "你好",
                "knowledgeId": 8900,
                "type": 1,
                "source": 2,
                "hits": 1,
                "useful": 10,
                "useless": 8,
                "del": 0,
                "web_id": 1,
                "create_user_id": 1001,
                "create_time": "2021-12-09 15:42:13",
                "update_user_id": 1001,
                "update_time": "2021-12-09 15:42:50",
                "alias": "你好"
            },
            {
                "id": 654,
                "domainId": 0,
                "question": "你好",
                "knowledgeId": 8900,
                "type": 1,
                "source": 2,
                "hits": 1,
                "useful": 10,
                "useless": 8,
                "del": 0,
                "web_id": 1,
                "create_user_id": 1001,
                "create_time": "2021-12-09 15:42:13",
                "update_user_id": 1001,
                "update_time": "2021-12-09 15:42:50",
                "alias": "你好"
            },
            {
                "id": 654,
                "domainId": 0,
                "question": "你好",
                "knowledgeId": 8900,
                "type": 1,
                "source": 2,
                "hits": 1,
                "useful": 10,
                "useless": 8,
                "del": 0,
                "web_id": 1,
                "create_user_id": 1001,
                "create_time": "2021-12-09 15:42:13",
                "update_user_id": 1001,
                "update_time": "2021-12-09 15:42:50",
                "alias": "你好"
            }
        ]
    },
    "message": "操作成功!"
}
```

### Response Example

```json
{
    "code": 1,
    "message": "success",
    "data": [
        {
            tag_id: 1,
            tag_name: "问题标签1",
            ...
        },
        {
            tag_id: 2,
            tag_name: "问题标签2",
            ...
        },
        ...
    ]
}
```

### ERROR Response

接口错误

```json
{
    "code": 2,
    "message": "error",
    "data": ""
}
```

## 2.2 增加或删除问题标签

```http
# 添加知识标签
POST http://192.168.128.82:8188/question
```

```http
# 删除问题标签
DELETE http://192.168.128.82:8188/question
```

### 接口说明

根据实时对话, 查询知识并获取问题标签列表, 并支持增加或删除功能

### Request fileds

| Name           | Type   | Require | Description                                       |
| -------------- | ------ | ------- | ------------------------------------------------- |
| call_id        | String | True    | 通话ID 用于标识标签所属通话                       |
| question       | String | True    | 问题名称                                          |
| intention      | Int    | True    | 进线意图号码                                      |
|                |        |         |                                                   |
| intention_name | String | True    | 意图名称                                          |
| agent_id       | String | True    | 坐席ID                                            |
| knowledge_id   | Int    | True    | 问题ID=知识ID                                     |
|                |        |         |                                                   |
| source         | Int    | True    | 问题来源: 1: 文本(默认), 2: 标准搜索, 3: 热点问题 |

请求示例

```json
{
    "call_id": "8c6d5237-a08c-4a71-adfd-df0a0ee37af0",
    "agent_id": 2345,
    "intention": 1001,
    "intention_name": "马桶",
    "question": "测试",
    "knowledge_id": 1234
}
```

### Response fileds

| Name             | Type   | Description                                                  |
| ---------------- | ------ | ------------------------------------------------------------ |
| code             | Int    | 1:成功<br />2:接口失败<br />3:请求错误                       |
| message          | String | success: 请求接口成功<br />error: 接口错误<br />failed: 错误的请求 |
| data             | Object | 返回操作                                                     |
| data.status      | Int    | 操作状态 1:成功, 0: 失败                                     |
| data.description | String | 状态描述信息: 操作成功                                       |
| data.error       | String | 操作失败时的错误提示信息                                     |

### Response Example

```json
{
    "code": 1,
    "message": "success",
    "data": {
        "status": 1,
        "description": "操作成功",
        "error": ""
    }
}
```

### ERROR Response

接口错误

```json
{
    "code": 2,
    "message": "error",
    "data": ""
}
```

## 2.3 问题标签知识内容查询

```http
GET http://127.0.0.1:8188/answer
```

### 接口说明

点击问题标签时, 根据该问题名称查询知识库 并返回知识内容

### Request fileds

| Name     | Type   | Require | Description                             |
| -------- | ------ | ------- | --------------------------------------- |
| question | String | True    | 问题名称(标准问题名称)                  |
| agent    | String | False   | 用于跟踪谁点击的问题                    |
| call_id  | String | False   | 问题所属通话                            |
| source   | Int    | True    | 问题来源: 1:语音文本流, 2:检索, 3: 热点 |

### Response fileds

| Name                    | Type   | Description                                                  |
| ----------------------- | ------ | ------------------------------------------------------------ |
| code                    | Int    | 1:成功<br />2:接口失败<br />3:请求错误                       |
| message                 | String | success: 请求接口成功<br />error: 接口错误<br />failed: 错误的请求 |
| data                    | []     | 问题知识列表 为空时表示不存在                                |
| data.answer_list        | List   | 问题答案 html文本 用于渲染页面                               |
| data.seed_question      | String | 标准问题                                                     |
| data.match_question     | String | 命中问题                                                     |
|                         |        |                                                              |
| ----以下为可能用到内容  |        |                                                              |
| data.answer_detail_list | List   | 需要根据实际接口考证                                         |
| data.index              | Int    | 答案序列                                                     |
|                         |        |                                                              |
| data.match_question     | String | 命中问题                                                     |
| data.question_label     | List   | 问题标签列表, label_id, label_name                           |

### Response Example

```json
{
    "code": 1,
    "message": "success",
    "data": [
        {
            "answerDetaillist": [
                {
                    "": "",
                    "": ""
                },
                {}
            ],
            "answer_list": [
                "<p><h2 style=\"text-align: center;\">安新县行政审批局</h2><h2 style=\"text-align: center;\">政务服务“帮您办”清单</h2><p><br/></p><table height=\"177\" border=\"1\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" style=\"margin:0 auto\" width=\"1080\"><colgroup><col width=\"100\"/><col width=\"100\"/><col width=\"80\"/><col width=\"250\"/><col width=\"450\"/><col width=\"100\"/></colgroup><tbody><tr height=\"37\" class=\"firstRow\" style=\"height: 28pt;\"><td class=\"et2\" height=\"28\" width=\"26\" style=\"text-align:center\">事项名称</td><td class=\"et2\" width=\"26\" style=\"text-align:center\">子项名称</td><td class=\"et2\" width=\"21\" style=\"text-align:center\">材料序号</td><td class=\"et2\" width=\"67\" style=\"text-align:center\">材料清单</td><td class=\"et2\" width=\"121\" style=\"text-align:center\">审核要点</td><td class=\"et2\" width=\"26\" style=\"text-align:center\">审核情况</td></tr><tr height=\"25\" style=\"height:20px\"><td rowspan=\"7\" height=\"140\" x:str=\"\" style=\"\" width=\"26\">公共场所卫生许可</td><td rowspan=\"7\" x:str=\"\" width=\"26\">&nbsp;设立</td><td x:num=\"1\" width=\"21\">&nbsp;1</td><td x:str=\"\" width=\"67\"><a href=\"https://www.baidu.com/\" target=\"_self\">公共场所卫生许可申请表</a>（下载空表）</td><td width=\"121\" x:str=\"\" style=\"\">1、单位名使用工商部门依法核准的名称全称；<br/>2、使用A4规格纸张打印，建议中文使用四号字,英文使用12号字，所有外文均应译为规范中文；<br/>3、申请人应当使用钢笔或签字笔工整地填写表格，不需申明的事项请注明“无”，不得空项，填写内容应完整、清楚、不得涂改；</td><td width=\"26\"><br/></td></tr><tr height=\"25\" style=\"height:20px\"><td x:num=\"2\" width=\"21\">&nbsp;2</td><td x:str=\"\" width=\"67\">公共场所卫生管理制度</td><td x:str=\"\" width=\"121\"><p>①申请单位卫生管理组织②卫生管理制度③消毒制度④传染病疫情报告制度⑤公共场所突发公共卫生事件应急预案⑥公共场所通风设施、通风情况</p></td><td width=\"26\"><br/></td></tr><tr height=\"25\" style=\"height:20px\"><td x:num=\"3\" width=\"21\">&nbsp;3</td><td width=\"67\" x:str=\"\" style=\"\">公共场所地址方位示意图、平面图和卫生设施平面布局图</td><td width=\"121\" x:str=\"\" style=\"\">1.与实际情况一致，盖公章<br/>2.卫生设施平面布局图需有消毒间（区）</td><td width=\"26\"><br/></td></tr><tr height=\"25\" style=\"height:20px\"><td x:num=\"4\" width=\"21\">&nbsp;4</td><td width=\"67\" x:str=\"\" style=\"\">法定代表人或负责人有效身份证明</td><td x:str=\"\" width=\"121\">核原件收复印件，复印件注明“此复印件与原件一致”</td><td width=\"26\"><br/></td></tr><tr height=\"25\" style=\"height:20px\"><td x:num=\"5\" width=\"21\">5</td><td x:str=\"\" width=\"67\">营业执照复印件</td><td x:str=\"\" width=\"121\">核营业执照原件，收复印件</td><td width=\"26\"><br/></td></tr><tr height=\"25\" style=\"height:20px\"><td x:num=\"6\" width=\"21\">6</td><td x:str=\"\" width=\"67\">申请人承诺书</td><td x:str=\"\" width=\"121\">申请单位公章，法人代表签字</td><td width=\"26\"><br/></td></tr><tr height=\"25\" style=\"height:20px\"><td x:num=\"7\" width=\"21\">7</td><td x:str=\"\" width=\"67\">授权委托书及身份证复印件</td><td width=\"121\" x:str=\"\" style=\"\">1.委托期限不少于办理整个事项全流程时限<br/>2.委托人签字盖公章<br/>3.身份证核原件收复印件，复印件注明“此复印件与原件一致”签字按手印（盖章）</td><td width=\"26\"><br/></td></tr><tr height=\"45\" style=\"height:45px\"><td colspan=\"6\" height=\"45\" x:str=\"\" style=\"text-align:right\" width=\"290\">帮办人&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 日期&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 月&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 日&nbsp;</td></tr></tbody></table><div contenteditable=\"false\" style=\"width: 15px; height: 15px; background-image: url(&quot;/webadmin/UEditor/dialogs/table/dragicon.png&quot;); position: absolute; cursor: move; top: 133px; left: 196px; user-select: none;\"></div></p>"
            ],
            "seed_question": "abc",
            "match_question": "abc",
            "question_label": [
                {
                    "label_id": 11,
                    "label_name": "标签1"
                },
                {
                    "label_id": 12,
                    "label_name": "标签2"
                },
                {
                    "label_idd": 13,
                    "label_name": "标签3"
                }
            ]
        }
    ]
}

```

```json

{
    "code": 1,
    "message": "success",
    "time": "2022-02-15 17:35:10",
    "data": {
        "seed_question": "测试",
        "match_question": "测试",
        "answer": [
            "<p><h2 style=\"text-align: center;\">安新县行政审批局</h2><h2 style=\"text-align: center;\">政务服务“帮您办”清单</h2><p><br/></p><table height=\"177\" border=\"1\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" style=\"margin:0 auto\" width=\"1080\"><colgroup><col width=\"100\"/><col width=\"100\"/><col width=\"80\"/><col width=\"250\"/><col width=\"450\"/><col width=\"100\"/></colgroup><tbody><tr height=\"37\" class=\"firstRow\" style=\"height: 28pt;\"><td class=\"et2\" height=\"28\" width=\"26\" style=\"text-align:center\">事项名称</td><td class=\"et2\" width=\"26\" style=\"text-align:center\">子项名称</td><td class=\"et2\" width=\"21\" style=\"text-align:center\">材料序号</td><td class=\"et2\" width=\"67\" style=\"text-align:center\">材料清单</td><td class=\"et2\" width=\"121\" style=\"text-align:center\">审核要点</td><td class=\"et2\" width=\"26\" style=\"text-align:center\">审核情况</td></tr><tr height=\"25\" style=\"height:20px\"><td rowspan=\"7\" height=\"140\" x:str=\"\" style=\"\" width=\"26\">公共场所卫生许可</td><td rowspan=\"7\" x:str=\"\" width=\"26\">&nbsp;设立</td><td x:num=\"1\" width=\"21\">&nbsp;1</td><td x:str=\"\" width=\"67\"><a href=\"https://www.baidu.com/\" target=\"_self\">公共场所卫生许可申请表</a>（下载空表）</td><td width=\"121\" x:str=\"\" style=\"\">1、单位名使用工商部门依法核准的名称全称；<br/>2、使用A4规格纸张打印，建议中文使用四号字,英文使用12号字，所有外文均应译为规范中文；<br/>3、申请人应当使用钢笔或签字笔工整地填写表格，不需申明的事项请注明“无”，不得空项，填写内容应完整、清楚、不得涂改；</td><td width=\"26\"><br/></td></tr><tr height=\"25\" style=\"height:20px\"><td x:num=\"2\" width=\"21\">&nbsp;2</td><td x:str=\"\" width=\"67\">公共场所卫生管理制度</td><td x:str=\"\" width=\"121\"><p>①申请单位卫生管理组织②卫生管理制度③消毒制度④传染病疫情报告制度⑤公共场所突发公共卫生事件应急预案⑥公共场所通风设施、通风情况</p></td><td width=\"26\"><br/></td></tr><tr height=\"25\" style=\"height:20px\"><td x:num=\"3\" width=\"21\">&nbsp;3</td><td width=\"67\" x:str=\"\" style=\"\">公共场所地址方位示意图、平面图和卫生设施平面布局图</td><td width=\"121\" x:str=\"\" style=\"\">1.与实际情况一致，盖公章<br/>2.卫生设施平面布局图需有消毒间（区）</td><td width=\"26\"><br/></td></tr><tr height=\"25\" style=\"height:20px\"><td x:num=\"4\" width=\"21\">&nbsp;4</td><td width=\"67\" x:str=\"\" style=\"\">法定代表人或负责人有效身份证明</td><td x:str=\"\" width=\"121\">核原件收复印件，复印件注明“此复印件与原件一致”</td><td width=\"26\"><br/></td></tr><tr height=\"25\" style=\"height:20px\"><td x:num=\"5\" width=\"21\">5</td><td x:str=\"\" width=\"67\">营业执照复印件</td><td x:str=\"\" width=\"121\">核营业执照原件，收复印件</td><td width=\"26\"><br/></td></tr><tr height=\"25\" style=\"height:20px\"><td x:num=\"6\" width=\"21\">6</td><td x:str=\"\" width=\"67\">申请人承诺书</td><td x:str=\"\" width=\"121\">申请单位公章，法人代表签字</td><td width=\"26\"><br/></td></tr><tr height=\"25\" style=\"height:20px\"><td x:num=\"7\" width=\"21\">7</td><td x:str=\"\" width=\"67\">授权委托书及身份证复印件</td><td width=\"121\" x:str=\"\" style=\"\">1.委托期限不少于办理整个事项全流程时限<br/>2.委托人签字盖公章<br/>3.身份证核原件收复印件，复印件注明“此复印件与原件一致”签字按手印（盖章）</td><td width=\"26\"><br/></td></tr><tr height=\"45\" style=\"height:45px\"><td colspan=\"6\" height=\"45\" x:str=\"\" style=\"text-align:right\" width=\"290\">帮办人&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 日期&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 月&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 日&nbsp;</td></tr></tbody></table><div contenteditable=\"false\" style=\"width: 15px; height: 15px; background-image: url(&quot;/webadmin/UEditor/dialogs/table/dragicon.png&quot;); position: absolute; cursor: move; top: 133px; left: 196px; user-select: none;\"></div></p>"
        ]
    }
}
```

### ERROR Response

接口错误

```json
{
    "code": 2,
    "message": "error",
    "data": ""
}
```

## 3 命中模型/语音分析结果提醒

> 实时预警提醒

```http
GET http://192.168.128.82:8188/reminder?call_id=94fae609-51cb-4e68-b2a9-86551b9589a2
```



### Request fileds

| Name     | Type   | Require | Description |
| -------- | ------ | ------- | ----------- |
| call_id  | String | True    | 通话流水号  |
| agent_id | String | False   | 坐席人员ID  |
|          |        |         |             |

请求示例

```json
{
    "call_id": "8c6d5237-a08c-4a71-adfd-df0a0ee37af0",
    "agent_id": 23459
}
```

### Response fileds

| Name                      | Type    | Description                                                  |
| ------------------------- | ------- | ------------------------------------------------------------ |
| code                      | Int     | 1:成功<br />2:接口失败<br />3:请求错误                       |
| message                   | String  | success: 请求接口成功<br />error: 接口错误<br />failed: 错误的请求 |
| data                      | List    | 命中模型名称列表[model1, model2]                             |
| reminder                  | Object  | 提醒                                                         |
| reminder.name             | String  | 提醒名称                                                     |
| reminder.background       | String  | 背景色信息 格式:#ff33cc                                      |
| reminder.type             | String  | 提醒类别: 非预警模型/预警模型/语音分析结果                   |
| reminder.time             | String  | 提醒接收时间, 格式: YYYY-MM_DD hh:mm:ss                      |
|                           |         |                                                              |
|                           |         |                                                              |
| --弃用--                  |         |                                                              |
| model                     | String  | 模型名称                                                     |
| model.agent_id            | String  | 坐席ID                                                       |
| model.call_id             | String  | 通话ID                                                       |
| model.model_name          | String  | 模型名称                                                     |
| model.model_id            | Integer | 模型ID                                                       |
| model.warning_name        | String  | 预警名称                                                     |
| model.warning             | Boolean | 是否预警类型                                                 |
| model.customer_phone      | String  | 客户号码                                                     |
| ****model.create_time**** | String  | 预警接收时间, 格式: YYYY-MM-DD hh:mm:ss                      |
| model.call_time           | String  | 通话接入时间, 格式: YYYY-MM-DD hh:mm:ss                      |

### Example

```json
{
    "code": 1,
    "message": "success",
    "data": [
        {
            "agent_id": "1000",
            "call_id": "8c6d5237-a08c-4a71-adfd-df0a0ee37af0",
            "name": "语速过快",
            "background": "#FF3355",
            "type": "语音分析结果",
            "time": "2022-09-11 14:59:32"
        },
        {
            "agent_id": "1000",
            "call_id": "8c6d5237-a08c-4a71-adfd-df0a0ee37af0",
            "name": "预警模型1",
            "background": "#00CCAA",
            "type": "预警模型",
            "time": "2022-09-11 13:58:32"
        },
        {
            "agent_id": "1000",
            "call_id": "8c6d5237-a08c-4a71-adfd-df0a0ee37af0",
            "name": "非预警模型1",
            "background": "#2299FF",
            "type": "非预警模型",
            "time": "2022-09-11 13:57:32"
        }
    ]
}
```

### ERROR Response

接口错误

```json
{
    "code": 0,
    "message": "error",
    "data": ""
}
```

## 4 标准问题搜索

> 通过搜索框, 搜索标准问题, 返回可能的标准问题列表

```http
GET http://192.168.128.82:8188/search
```

### 接口说明

本接口主要用于获取相关问题和答案, 原始接口数据由外部接口提供

对应接口文档中的标准问题答案

### Request fileds

| Name     | Type   | Description             |
| -------- | ------ | ----------------------- |
| question | String | 搜索问题名称 输入的问题 |

### Response fileds

| Name                  | Type    | Description                                                  |
| --------------------- | ------- | ------------------------------------------------------------ |
| code                  | Int     | 1:成功<br />2:接口失败<br />3:请求错误                       |
| message               | String  | success: 请求接口成功<br />error: 接口错误<br />failed: 错误的请求 |
| data                  | Object  | 接口数据, 列表中的元素为返回的标准问题                       |
| question_list         | List    | 标准问题列表                                                 |
| question.knowledge_id | Integer | 知识ID                                                       |
| question.question     | String  | 问题名称                                                     |
|                       |         |                                                              |

### Example

```jsonc
```



```json
{
    "code": 1,
    "data": {
        "question_list": [
            {
                "knowledge_id": 300515,
                "question": "你好"
            },
            {
                "knowledge_id": 300516,
                "question": "你好we"
            }
        ]
    },
    "message": "success"
}
```

```json
{
    "code": 1,
    "message": "success",
    "data": {
        "answerDetaillist": [
            {
                "": "",
                "": ""
            },
            {}
        ],
        "answer_list": [
            "xxxxxx"
        ],
        "index": 1,
        "seed_question": "abc",
        "match_question": "abc",
        "question_label": [
            {
                "label_id": 11,
                "label_name": "标签1"
            },
            {
                "label_id": 12,
                "label_name": "标签2"
            },
            {
                "label_idd": 13,
                "label_name": "标签3"
            }
        ]
    }
}
```

### ERROR Response

接口错误

```json
{
    "code": 0,
    "message": "error",
    "data": ""
}
```

## 5 知识库排行榜

```http
GET http://127.0.0.1:8188/top
```

### 接口说明

根据进线意图获取TOP问题 10条

查询接口并返回实时知识库排行榜(热门问题), 每次展示10条

### Request fileds

| Name      | Type    | Require | Description      |
| --------- | ------- | ------- | ---------------- |
| intention | Integer | True    | 客户意图号 vdnNo |

### Response fileds

| Name                    | Type       | Description                                                  |
| ----------------------- | ---------- | ------------------------------------------------------------ |
| code                    | Int        | 1:成功<br />2:接口失败<br />3:请求错误                       |
| message                 | String     | success: 请求接口成功<br />error: 接口错误<br />failed: 错误的请求 |
| data                    | Object     | 数据内容                                                     |
| question                | List       | 问题集合, 列表元素为一个热门问题                             |
| question                | Object     | 问题(标签)对象                                               |
| question.id             | Integer    | 问题id                                                       |
| **question.question**   | **String** | **问题名称**                                                 |
| question.knowledge_id   | Integer    | 知识ID                                                       |
| question.type           | Integer    | 问题类型(1：标准问题 2：相似问题 3：词条 4：原子知识 5：摘要) |
| question.source         | Integer    | 问题来源(0：手动 1：机器之不会 2：机器之猜测 3：回答问题时添加) |
| question.hits           | Long       | 点击次数                                                     |
| question.useful         | Long       | 有用的次数                                                   |
| question.useless        | Long       | 无用的次数                                                   |
| question.del            | Integer    | 是否删除（0：未删除 1：已删除）                              |
| question.web_id         | Long       | 站点id                                                       |
| question.create_user_id | Long       | 创建人id                                                     |
| question.create_time    | datetime   | 创建时间                                                     |
| question.update_user_id | Long       | 更新人id                                                     |
| question.update_time    | datetime   | 更新时间                                                     |
| question.alias          | String     | 别称                                                         |
|                         |            |                                                              |

### Response Example

```jsonc
// 根据进线意图获取TOP问题
{
    "code": 1,
    "data": {
        "question_list": [
            {
                "id": 654,
                "domain_id": 0,
                "question": "你好",
                "knowledge_id": 8900,
                "type": 1,
                "source": 2,
                "hits": 1,
                "useful": 10,
                "useless": 8,
                "del": 0,
                "web_id": 1,
                "create_user_id": 1001,
                "create_time": "2021-12-09 15:42:13",
                "update_user_id": 1001,
                "update_time": "2021-12-09 15:42:50",
                "alias": "你好"
            },
            {
                "id": 654,
                "domain_id": 0,
                "question": "你好",
                "knowledge_id": 8900,
                "type": 1,
                "source": 2,
                "hits": 1,
                "useful": 10,
                "useless": 8,
                "del": 0,
                "web_id": 1,
                "create_user_id": 1001,
                "create_time": "2021-12-09 15:42:13",
                "update_user_id": 1001,
                "update_time": "2021-12-09 15:42:50",
                "alias": "你好"
            },
            {
                "id": 654,
                "domain_id": 0,
                "question": "你好",
                "knowledge_id": 8900,
                "type": 1,
                "source": 2,
                "hits": 1,
                "useful": 10,
                "useless": 8,
                "del": 0,
                "web_id": 1,
                "create_user_id": 1001,
                "create_time": "2021-12-09 15:42:13",
                "update_user_id": 1001,
                "update_time": "2021-12-09 15:42:50",
                "alias": "你好"
            }
        ]
    },
    "message": "success"
}
```

### ERROR Response

接口错误

```json
{
    "code": 0,
    "message": "error",
    "data": ""
}
```

## 6 业务统计报表

### 功能说明

获取并统计后端推送到的所有预警

根据实时预警被调接口, 获取该系统下所有的预警信息,

前端发起调用时, 统计当天所有的

### 接口

```http
GET http://192.168.128.82:8188/chart/count

```

### Request fileds

| Name | Type   | Require | Description                                  |
| ---- | ------ | ------- | -------------------------------------------- |
| date | String | False   | 获取指定日期的报表统计<br />格式: yyyy-mm-dd |

### Response fileds

| Name          | Type    | Description                                                  |
| ------------- | ------- | ------------------------------------------------------------ |
| code          | Int     | 1:成功<br />2:接口失败<br />3:请求错误                       |
| message       | String  | success: 请求接口成功<br />error: 接口错误<br />failed: 错误的请求 |
| data          | List    | 报表统计                                                     |
| data.headers  | List    | 表头                                                         |
| data.data     | List    | 坐席统计列表                                                 |
| agent         | String  | 坐席姓名                                                     |
| agent_id      | String  | 坐席ID                                                       |
| calling       | Integer | 通话总数                                                     |
| reminding     | Integer | 提醒总数                                                     |
| warning       | Int     | 预警总数                                                     |
| reminding_[N] | Int     | 提醒[1, 2, 3, ...]总数                                       |
| warning_[N]   | Int     | 预警[1, 2, 3, ...]总数                                       |
| tag_name      | String  | 问题标签名称                                                 |

### Response Example

```json
{
    "code": 1,
    "message": "success",
    "data": {
        "headers": [
            "坐席姓名",
            "坐席ID",
            "通话总数",
            "提醒总数",
            "预警总数",
            "提醒_1",
            "提醒_2",
            "提醒_...",
            "预警_1",
            "预警_2",
            "预警_..."
        ],
        "data": [
            {
                "坐席姓名": "张三",
                "坐席ID": 2345,
                "通话总数": 2345,
                "提醒总数": 15,
                "预警总数": 20,
                "提醒_1": 10,
                "提醒_2": 15,
                "预警_1": 5,
                "预警_2": 3
            },
            {
                "坐席姓名": "李四",
                "坐席ID": 2349,
                "通话总数": 2345,
                "提醒总数": 15,
                "预警总数": 20,
                "提醒_1": 10,
                "提醒_2": 15,
                "预警_1": 5,
                "预警_2": 3
            },
            ...

            ...
        ]
    }
}
```

## 7 报表导出

### 功能说明

服务器

提醒:  非预警模型

预警: 预警模型

列表展示当天的统计数据，统计范围为当前用户组所有坐席、所有已上线模型的统计；

当前用户组所有坐席姓名；

每个坐席的当天通话总数；

每个坐席的对应模型命中数量；

“提醒”（非预警模型）等级模型命中总数；

“预警”（预警模型）等级模型命中总数；

将表格数据生成xlsx文件

文件名称: 业务统计报表_[日期].xlsx

```http
GET http://192.168.128.82:8000/chart/export
```

### Request fileds

| Name  | Type   | Require | Description                                                  |
| ----- | ------ | ------- | ------------------------------------------------------------ |
| date  | String | False   | 获取指定日期的报表统计, 为空时表示当天<br />格式: yyyy-mm-dd |
| agent | List   | True    | 坐席姓名列表, 如果为空将导出全部<br />**需注意**             |

### Response

示例

```json
{
}
```

## 8 问题反馈结果提交

### 功能说明

关于问题点击接口, 前端每次点击问题并获取知识答案时 后端将自动记录问题点击情况

在问题答案界面提供反馈按钮, 向云问传递该问题是否为可用反馈

### 接口

```http
POST http://127.0.0.1:8188/feedback
```

### Request fileds

| Name         | Type    | Require | Description                         |
| ------------ | ------- | ------- | ----------------------------------- |
| question     | String  | True    | 问题名称                            |
| knowledge_id | Integer | True    | 问题ID                              |
| feedback     | Integer | True    | 1:可用反馈; 2: 不可用反馈; 0:未选择 |
|              |         |         |                                     |
| agent        | String  | False   | 坐席账号                            |
| call_id      | String  | False   | 通话流水号                          |

请求示例

```json
{
    "question": "测试",
    "knowledge_id": 1235,
    "feedback": 2,
    "agent": "23457"
}
```

### Response fileds

| Name        | Type    | Description                                                  |
| ----------- | ------- | ------------------------------------------------------------ |
| code        | Int     | 1:成功<br />2:接口失败<br />3:请求错误                       |
| message     | String  | success: 请求接口成功<br />error: 接口错误<br />failed: 错误的请求 |
| data        | Object  | 提交状态提示                                                 |
| data.status | Integer | 提交状态 1:成功, 0: 失败, -1: 接口错误, 2: 重复提交.         |

### Response Example

```json
{
    "code": 1,
    "message": "success",
    "data": {
        status: 1,
        description: "提交成功"
    }
}
```

### ERROR Response

接口错误

```json
{
    "code": 2,
    "message": "error",
    "data": {
        "state": 0,
        "error": "提交失败"
    }
}
```

