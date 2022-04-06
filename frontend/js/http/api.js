// 九牧项目

// 意图获取
function getIntention(data) {
  return fetch_GET('/intention', data)
}

// 通话信息
function getCallInfo(data) {
  return fetch_GET('/call_info', data)
}

// 来电统计接口
function getCallRecord(data) {
  return fetch_GET('/call', data)
}

// 查询问题标签列表
function getTags(data) {
  return fetch_GET('/question', data)
}

// 删除问题标签
function deletTag(data) {
  return fetch_DELETE('/question', data)
}

// 增加问题标签
function addTags(data) {
  return fetch_POST('/question', data)
}

// 通过搜索框, 搜索标准问题, 返回可能的标准问题列表
function getSearchList(data) {
  return fetch_GET('/search', data)
}

// 根据进线意图获取TOP问题
function getTopList(data) {
  return fetch_GET('/top', data)
}

// 点击问题标签时, 根据该问题名称查询知识库 并返回知识内容
function getAnswerDetail(data) {
  return fetch_GET('/answer', data)
}

// 命中模型 语⾳分析结果提醒
function getReminder(data) {
  return fetch_GET('/reminder', data)
}

// 业务统计报表
function getTableChart(data) {
  return fetch_GET('/chart/count', data)
}

// 导出报表
function getchartExport() {
  return fetch_GET('/chart/export', data)
}

// 问题反馈结果提交
function feedBack(data) {
  return fetch_POST('/feedback', data)
}

// 执行获取语音识别文本流任务
function runTaskGetSpeechStream(data){
  return fetch_GET('/speech_stream', data)
}

