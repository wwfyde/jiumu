function deepclone(target) {
  if (typeof target !== "object") return target;

  let obj;
  if (!Array.isArray) {
    Array.isArray = function(arg) {
      return Object.prototype.toString.call(arg) === "[object Array];";
    };
  }
  if (Array.isArray(target)) {
    obj = [];
  } else {
    obj = {};
  }
  for (let prop in target) {
    // obj.hasOwnProperty 判断某个对象是否含有指定的属性
    // 该方法会忽略掉从原型链上继承的属性
    if (target.hasOwnProperty(prop)) {
      if (typeof target === "object") {
        obj[prop] = deepclone(target[prop]);
      } else {
        obj[prop] = target[prop];
      }
    }
  }
  return obj;
}



function uniqueArr(arr, ...arguements) {
  // 去重
  function getBoolean(o, m) {
    let list = arguements.map(x => o[x] == m[x]); //值均为布尔
    return list.every(i => i); //要使这些布尔值都真才能满足条件，因为要求的条件是 并且
  }
  
  let result = [];//新数组
  //总数组与新数组比较，遍历总数组时用新数组的some方法进行判断
  arr.map(o => !result.some(m => getBoolean(o, m)) ? result.push(o) : '');
  return result;
}

// 比较时间大小
function compareDate(date1, date2){
  let oDate1 = new Date(date1);
  let oDate2 = new Date(date2);

  if(oDate1.getTime() >= oDate2.getTime()){
    return true; // 第一个大
  } else {
    return false; // 第二个大
  }
}
// 替换tip内容
function replaceTipWord (keyword, data) {


  let arr = keyword.split(' ')
  let reg = ''

  arr.forEach((item, index) => {
    if (index === arr.length - 1) {
      reg += item
    } else {
      reg += `${item}.*?`
    }
  })
  let replaceReg = new RegExp(reg)// 匹配关键字正则

  let res = data.match(replaceReg)
  if (!res) {
    return data
  }
  let content = res[0]

  let prevIndex = -1
  let endIndex = -1
  let partContent = '' // 高亮的内容

  arr = arr.map(item => {
    let obj = {}
    let index = content.indexOf(item, prevIndex)

    prevIndex = index
    endIndex = index + item.length

    obj.begin = prevIndex
    obj.end = endIndex
    obj.value = item
    return obj
  })


  for(let i = 0; i < content.length;) {
    let filterArr = arr.filter(item => item.begin === i)
    if (filterArr.length > 0) {
      partContent += replaceWord(filterArr[0].value, content.slice(filterArr[0].begin, filterArr[0].end))
      i = filterArr[0].end
    } else {
      partContent += content[i]
      i++
    }
  }
  return data.replace(content, partContent)
}

function replaceWord(keyword, data) {
  let replaceReg = new RegExp(keyword, 'g')// 匹配关键字正则
  let replaceString = '<span class="highlights-text">' + keyword + '</span>'
  data = data.replace(replaceReg, replaceString)
  return data
}
// 高亮文本
function handleWord (content, arr) {
  let res = ''
  let end = 0
  
  for(let i = 0; i < content.length; i++) {
    let matchFlag = false
    for(let j = 0; j < arr.length; j++) {
      if (arr[j].begin === i) {
        let keyword = content.slice(arr[j].begin, arr[j].end)
        let replaceReg = new RegExp(keyword)// 匹配关键字正则

        let replaceString = '<span class="highlights-text">' + keyword + '</span>'

        res += keyword.replace(replaceReg, replaceString)
        matchFlag = true
        end = arr[j].end
        // console.log('end', end);
        break
      }
    }
    if (i > end || !matchFlag) {      
      res += content[i]
    }
    
  }
  return res
}
// 找到需要插入的下标
function findKeyWordIndex(keyword, data, beginIndex) {
  // console.log(keyword, data, beginIndex);
  let indexArr = []

  let arr = keyword.split(/and|or|after|near|''/)

  arr.forEach((item, index) => {
    let val = item.trim()
    let replaceReg = new RegExp(val)// 匹配关键字正则
  
    if (replaceReg.test(data)) {
      let value = Number(beginIndex) + Number(data.indexOf(val))

      indexArr.push({
        begin: value,
        end: value + val.length,
        val: item
      })
    }

  })

  return indexArr
}
// 替换文本内容 暂不用
function replaceWord1(keyword, data) {

  let arr = keyword.split(/and|or|after|near|''/)

  arr.forEach(item => {
    let replaceReg = new RegExp(item.trim(), 'g')// 匹配关键字正则
  
    let replaceString = '<span class="highlights-text">' + item.trim() + '</span>'
    data = data.replace(replaceReg, replaceString)
  })


  return data
}

// 过滤筛选条件的对话
function filterDetailData(searchForm, data) {
  let detailData = deepclone(data)
  // 筛选条件为空，则返回全部数据
  // if (!(searchForm.labelType === 1 || searchForm.labelType === 2 ||searchForm.role.length > 0 || searchForm.beginTime || searchForm.endTime)) {
  //   return deepclone(detailData)
  // }
  let res = []

  detailData.forEach((item, index) => {
    let roleFlag = true
    let sendTimeFlag = true
    let endTimeFlag = true
    let labelTypeFlag = true

    // // 搜索标签类别对应的会话
    // if (searchForm.labelType === 0 || searchForm.labelType === 1) {
    //   labelTypeFlag = item.hit_keywords.some(hitItem => {
    //     return hitItem.label_type === searchForm.labelType
    //   })
    // }

    // 搜索当前类别对应的标签
    if (item.hit_keywords.length > 0) {
      item.hit_keywords = item.hit_keywords.filter(hitItem => {
        return hitItem.label_type == searchForm.labelType
      })
    }

    // 搜索角色对应的会话
    if (searchForm.role.length > 0) {
      roleFlag = searchForm.role.includes(item.role)
    }

    // 搜索开始时间对应的会话
    if (!!searchForm.beginTime) {
      sendTimeFlag = compareDate(item.send_time, searchForm.beginTime)
    }

    // 搜索结束时间对应的会话
    if (!!searchForm.endTime) {
      endTimeFlag = compareDate(searchForm.endTime, item.send_time)
    }

    if (roleFlag && sendTimeFlag && endTimeFlag && labelTypeFlag) {
      res.push(item)
    }
  })
  return res
}

function highlightSection(data) {
  // 高亮 begin & end 之间的内容
  data.map(item => {
    // 展示label_name
    item.isShowKeyword = true

    
    let content = item.content
    let finalContent = '' // 高亮后的内容


    // 去重
    item.hit_keywords = uniqueArr(item.hit_keywords, 'label_id', 'begin', 'end')
    
    // 高亮内容

    if (item.hit_keywords.length > 0) {
      // console.log('item.hit_keywords', item.hit_keywords);

      let insertIndex = []

      item.hit_keywords.forEach(hitItem => {

        let begin = hitItem.begin - item.wordStart
        let end = hitItem.end - item.wordStart


        if (begin < 0) {
          // 跨句
          // 找到插入的下标
          let tempIndexArr = findKeyWordIndex(hitItem.hit_keyword, content.slice(0, end+1), 0)

          if (tempIndexArr.length > 0) {
            insertIndex = [...insertIndex, ...tempIndexArr]
          }

        } else {
          // 找到插入的下标
          let tempIndexArr = findKeyWordIndex(hitItem.hit_keyword, content.slice(begin, end+1), begin)


          if (tempIndexArr.length > 0) {
            insertIndex = [...insertIndex, ...tempIndexArr]
          }

        }
      })
      // 高亮对应的位置
      finalContent = handleWord(content, insertIndex)

      item.content = finalContent
    }

    // 高亮提示
    if (item.hit_keywords.length > 0) {
      
      let labelIdList = []
      let hitKeyList = []

      item.hit_keywords.forEach((hitItem) => {
        if (labelIdList.indexOf(hitItem.label_id) === -1) {
          // 高亮
          hitItem.formula = replaceTipWord(hitItem.hit_keyword, hitItem.formula)
          // id 列表
          labelIdList.push(hitItem.label_id)
          // 显示的标签List
          hitKeyList.push(hitItem)
        } else {
          for(let i = 0; i < hitKeyList.length; i++) {
            if (hitKeyList[i].label_id === hitItem.label_id) {
              hitKeyList[i].formula = replaceTipWord(hitItem.hit_keyword, hitKeyList[i].formula)
            }
          }
        }
      })
      item.hit_keywords = hitKeyList
    }    
  })
  return data
}

// 高亮
function highlightWord(searchForm, data) {  
  let matchIndex = -1

  // 筛选条件为空，则返回原数据
  if (!(searchForm.labelName || searchForm.labelId)) {

    data = highlightSection(data)
    return {data, matchIndex}
  }

  data = data.map((item, index) => {
    item.isShowKeyword = false
    let nameFlag = false
    let idFlag = false

    if (searchForm.labelName && item.hit_keywords && item.hit_keywords.length > 0) {
      nameFlag = item.hit_keywords.some(hitItem => {
        return hitItem.label_name === searchForm.labelName
      })
    }

    if (searchForm.labelId && item.hit_keywords && item.hit_keywords.length > 0) {
      idFlag = item.hit_keywords.some(hitItem => {
        return hitItem.label_id === searchForm.labelId
      })
    }

    // 匹配到了 name 或 id
    if (nameFlag || idFlag) {
      // 高亮悬浮提示的匹配词
      data = data.map((item, index) => {
        item.hit_keywords = item.hit_keywords.filter((hitItem) => {
          return searchForm.labelName === hitItem.label_name || searchForm.labelId === hitItem.label_id
        })
        return item
      })

      data = highlightSection(data)
      

      if (matchIndex === -1) {
        matchIndex = index
      }
    }

    return item
  })
  return {data, matchIndex}
  
}

// 获取路由参数
function getParamByRouter (key) {
  let obj = {}
  let name, value;
  let str = location.href; //取得整个地址栏
  let num = str.indexOf("?")
  str = str.substr(num + 1); //取得所有参数   stringvar.substr(start [, length ]

  let arr = str.split("&"); //各个参数放到数组里
  for(let i = 0;i < arr.length; i++){
    num = arr[i].indexOf("=");
    if (num > 0) {
      name = arr[i].substring(0,num);
      value = arr[i].substr(num+1);
      obj[name] = value;
    }
  }
  return obj[key]
}