var vm = new Vue({
    el: '#app',
    data() {
        return {
            //所有参数
            allParams: {
                phone: '', // 来电手机号
                agent: "", // 坐席ID
                intention: null, // 进线意图号码
                intention_name: '', // 进线意图号码
                call_id: ''
            },
            externalLinksHost: 'http://10.222.26.19',
            smart_order_path: '/webadmin/jomoo/index.html?customerName=',
            defaultProps: {
                label: 'question',
            },
            publicQuestion: '', // 公用的问题
            publicKnowledgeId: null, // 共用的知识ID
            isLoading: true,
            isTopLoading: true,
            intentionName: '',
            today: '',
            month: '',
            tags: [],  // 问题标签列表
            resultOneColor: '',
            resultTwoColor: '',
            resultOneName: '',
            resultTwoName: '',
            isShow: false, // 是否展开问题内容
            iconDatas: 'el-icon-caret-bottom',
            searchProblem: '',
            treeData: [], // 搜索问题列表数据
            hotDatas: [], // 热门Top问题
            answerContent: '', // 知识内容
            options: [{
                value: 0,
                label: '请选择'
            }, {
                value: 1,
                label: '可⽤反馈'
            }, {
                value: 2,
                label: '不可⽤反馈'
            }],
            isDisabled: true,  // 反馈禁用状态
            value: ''
            // tinymceInit:{
            //   selector: '#mytextarea',
            //   toolbar: false,
            //   menubar: false,
            //   branding: false,
            //   elementpath: false,
            //   statusbar: false,
            //   height: 645,
            //   plugins: "link",
            //   default_link_target: '_blank',
            //   link_context_toolbar: true,
            // }
        }
    },
    watch: {
        // publicQuestion(newVal, oldVal) {
        //   if(newVal && oldVal!= newVal) {
        //     this.isDisabled = false
        //   }
        // }
        // filterText(val) {
        //   this.$refs.tree.filter(val);
        // }
    },
    computed: {
        firstFiveTabs() {
            return this.tags.filter((item, index) => {
                return index < 5
            })
        },
        secondFiveTabs() {
            return this.tags.filter((item, index) => {
                return 10 > index && index > 4
            })
        },
        thirdFiveTabs() {
            return this.tags.filter((item, index) => {
                return 15 > index && index > 9
            })
        },
        fourthFiveTabs() {
            return this.tags.filter((item, index) => {
                return 20 > index && index > 14
            })
        }
    },
    methods: {
        // 问题反馈
        feedBackClick() {
            feedBack({
                question: this.publicQuestion,
                feedback: this.value,
                knowledge_id: this.publicKnowledgeId,
                agent: this.allParams.agent,
                call_id: this.allParams.call_id
            }).then(res => {
                let resData = res.data
                if (resData.code === 1) {
                    this.$message({message: resData.data.description, type: 'success', duration: 1000})
                    if (resData.data.status === 1) {
                        this.isDisabled = true
                    }
                }
            }).catch(err => {
                console.log(err);
            })
        },
        search() {
            // 通过搜索框, 搜索标准问题, 返回可能的标准问题列表
            console.log("尝试搜索标准问题")
            getSearchList({
                question: this.searchProblem
            }).then(res => {
                let resData = res.data
                if (resData.code === 1) {
                    this.treeData = resData.data.question_list
                }
            }).catch(err => {
                console.log(err);
            })
        },
        calcHeight() {
            $('.rightBox').height(window.innerHeight - 46 - 21)
            $('.leftBox').height(window.innerHeight - 46 - 21)
            $('.firstHot').height(window.innerHeight - 46 - 21 - 300 - 20 - 20)
            $('.questionContent').height(window.innerHeight - 46 - 21 - 44)
        },
        showBtn(val) {
            this.isShow = !val
            this.iconDatas = this.isShow === true ? 'el-icon-caret-top' : 'el-icon-caret-bottom'
            document.getElementById("btnId").blur()
        },
        // 意图获取
        getIntentionData() {
            getIntention({
                phone: this.allParams.phone,
                agent: this.allParams.agent
            }).then(res => {
                let resData = res.data
                if (resData.code === 1) {
                    this.intentionName = resData.data.intention.name
                    this.allParams.intention = resData.data.intention.id
                    this.allParams.intention_name = resData.data.intention.name
                    this.getTagsData()
                    this.getTopQuestion()
                }
                this.isLoading = false
            }).catch(err => {
                console.log(err);
            })
        },
        // 获取通话信息
        getCallInfoData() {
            getCallInfo({
                agent: this.allParams.agent
            }).then(res => {
                let resData = res.data
                if (resData.code === 1) {
                    console.log('获取通话信息成功', resData)
                    this.allParams.call_id = resData.data.call_id
                    this.allParams.phone = resData.data.phone
                    this.allParams.intention = resData.data.intention_id
                    this.allParams.intention_name = resData.data.intention_name
                }
            }).catch(err => {
                console.log(err);
            })
        },
        // 开启文本流识别任务
        runTaskData() {
            runTaskGetSpeechStream({
                agent: this.allParams.agent
            }).then(res => {
                let resData = res.data
                if (resData.code === 1) {
                    console.log("执行后台任务成功")
                }
            }).catch(err => {
                console.log(err);
            })
        },
        // 来电统计信息
        getCallRecordData() {
            getCallRecord({
                phone: this.allParams.phone,
                agent: this.allParams.agent
            }).then(res => {
                let resData = res.data
                if (resData.code === 1) {
                    this.today = resData.data.today
                    this.month = resData.data.month
                }
            }).catch(err => {
                console.log(err);
            })
        },
        // 查询问题标签列表
        getTagsData() {
            getTags({
                call_id: this.allParams.call_id,
                intention: this.allParams.intention,
                agent: this.allParams.agent,
            }).then(res => {
                let resData = res.data
                if (resData.code === 1) {
                    let tagsList = resData.data.map((n, index) => {
                        if (n) {
                            n.type = 'warning'
                            n.id = index
                        }
                        return n
                    })

                    this.tags = tagsList
                    console.log("标签列表,", this.tags)
                }
            }).catch(err => {
                console.log(err);
            })
        },
        // 获取url中的参数
        GetQueryString(name) {
            let query = window.location.search.substring(1);
            let vars = query.split("&");
            for (let i = 0; i < vars.length; i++) {
                let pair = vars[i].split("=");
                if (pair[0] == name) {
                    console.log(pair[1])
                    return pair[1];
                }
            }
            return (false);
        },
        // 移除tag时触发
        handleClose(tag) {
            deletTag({
                call_id: this.allParams.call_id,
                agent_id: this.allParams.agent,
                intention: this.allParams.intention,
                intention_name: this.allParams.intention_name,
                question: tag.question
            }).then(res => {
                let resData = res.data
                if (resData.code === 1) {
                    this.getTagsData()
                    this.$message({message: '删除成功', type: 'success', duration: 1000})
                }
            }).catch(err => {
                console.log(err);
            }).catch(err => {
                console.log(err);
            })
        },
        // 点击tag显示问题详情
        tagClick(tag) {
            this.getDetail(tag.question, tag.question_id, 1)
            this.showBtn(false)
        },
        // 点击搜索框检索出的问题详情
        handleNodeClick(data) {
            this.getDetail(data.question, data.knowledge_id, 2)
        },
        //  添加tags
        addAppend(data) {
            addTags({
                call_id: this.allParams.call_id,
                agent_id: this.allParams.agent,
                intention: this.allParams.intention,
                intention_name: this.allParams.intention_name,
                question: data.question,
                knowledge_id: data.knowledge_id
            }).then(res => {
                let resData = res.data
                if (resData.code === 1) {
                    this.getTagsData()
                    if (resData.status) {
                        this.$message({message: '添加成功', type: 'success', duration: 1000})

                    } else {
                        this.$message({message: '重复添加', type: 'warning', duration: 1000})


                    }
                }
            }).catch(err => {
                console.log(err);
            })
        },
        // 根据进线意图获取TOP问题
        getTopQuestion() {
            getTopList({
                intention: this.allParams.intention
            }).then(res => {
                let resData = res.data
                if (resData.code === 1) {
                    this.hotDatas = resData.data.filter((n, index) => {
                        if (index < 10) {
                            return n
                        }
                    })
                }
                this.isTopLoading = false
            }).catch(err => {
                console.log(err);
            })
        },
        // 点击topClick
        topClick(obj) {
            console.log("尝试查询热点问题", obj, obj.question, obj.knowledge_id)
            this.getDetail(obj.question, obj.knowledge_id, 3)
        },
        // 问题标签知识内容查询
        getDetail(question, knowledge_id, source) {
            console.log("尝试查询问题知识")
            this.publicQuestion = question
            this.publicKnowledgeId = knowledge_id
            getAnswerDetail({
                question: question,
                knowledge_id: knowledge_id,
                call_id: this.allParams.call_id,
                agent: this.allParams.agent,
                source: source
            }).then(res => {
                let resData = res.data
                console.log("问题知识查询结果", resData)
                if (resData.code === 1) {
                    // 会返回一个状态是否可以点击反馈状态
                    this.answerContent = resData.data[0].answer_list[0].replaceAll('src="/', 'src="'+ this.externalLinksHost+ '/').replaceAll('href="/', 'href="'+ this.externalLinksHost+'/')
                    //  问题反馈状态
                    if (resData.status === 0) {
                        this.isDisabled = false
                    } else {
                        this.isDisabled = true
                    }


                }
            }).catch(err => {
                console.log(err);
            })
        },
        // 实时展示最新命中模型和语⾳分析结果, 最多展示2个, 新的覆盖旧的
        getCheckReminder() {
            console.log("尝试获取提醒信息")
            getReminder({
                call_id: this.allParams.call_id,
                agent_id: this.allParams.agent
            }).then(res => {
                let resData = res.data
                if (resData.code === 1) {
                    var checkReminder = []
                    console.log(res)
                    checkReminder = resData.data.filter((n, index) => {
                        if (index < 2) {
                            return n
                        }
                    })
                }
                if (checkReminder.length === 1) {
                    this.resultOneColor = checkReminder[0].color
                    this.resultOneName = checkReminder[0].model_name
                }
                if (checkReminder.length === 2) {
                    this.resultOneColor = checkReminder[0].color
                    this.resultTwoColor = checkReminder[1].color
                    this.resultOneName = checkReminder[0].model_name
                    this.resultTwoName = checkReminder[1].model_name
                }
            }).catch(err => {
                console.log(err);
            })
        },
        // 实时访问
        getTimer() {
            let timer = setInterval(() => {
                this.getIntentionData()
                this.getCheckReminder()
                this.getTopQuestion()
            }, 5000);
            this.$once('hook:beforeDestroy', () => {
                clearInterval(timer);
                timer = null;
            })
        },
        handleSmartOrder(){
            window.open(this.externalLinksHost + this.smart_order_path + this.allParams.agent, '_blank')
        }
    },
    mounted() {
        // 通过url参数获取坐席账号
        console.log("url参数中的agent", this.GetQueryString('agent'))
        this.allParams.agent = this.GetQueryString('agent')
        console.log("url参数中的agent", this.allParams.agent)
        // 实时获取语音流信息
        this.runTaskData()
        // 获取通话信息
        this.getCallInfoData()
        // 获取意图信息
        this.getIntentionData()
        // 获取来电统计
        this.getCallRecordData()
        // 获取预警提醒
        this.getCheckReminder()
        // TODO 是否定时获取
        this.getTimer()

        // 弃用
        // tinymce.init(this.tinymceInit)
        this.calcHeight()
        window.onresize = () => {
            this.calcHeight()
        }
    }
})