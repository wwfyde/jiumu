var vm = new Vue({
  el: '#app',
  data() {
    return {
      zxName:'',
      total: 0,
      pagesize: 10,
      currentPage: 1,
      headers: [],
      tableData: [],
      allTableData: []
    }
  },
  watch:{
    zxName(newVal,old) {
      if (newVal === '') {
        this.tableData = this.allTableData
      }
    }
  },
  computed: {
    tableHeight() {
      return window.innerHeight - 15 - 60 - 15 - 15 - 60 - 15 - 1  
    }
  },
  methods: {
    searchList() {
      this.currentPage = 1
      this.tableData = this.allTableData.filter(n => {
        if (n && n.坐席姓名 === this.zxName) {
         return n
        }
      })
    },
    getTableDatas() {
      console.log("尝试获取报表")
      getTableChart().then(res => {
        let resData = res.data
        if (resData.code === 1) {
          console.log("获取报表成功", resData.data)
          for(let key in resData.data.data[0]) {
            this.headers.push(key)
          }
          this.allTableData = resData.data.data.map(n => {
            return n
          })
          this.tableData = resData.data.data.map(m => {
            return m
          })
        }
      }).catch(err => {
        console.log(err)
      }).catch(err => {
        console.log(err)
      })
    },
    calcHeight() {
      let avr = (window.innerHeight - 15 - 60 - 15 - 15 - 60 - 15 - 1)
      $('.tableBody').height(avr)
      $('.tableee').height(avr)
    },
    handleCurrentChange(currentPage){
      this.currentPage = currentPage
    },
    // 导出报表按钮
    exportTable() {
      console.log("准备导出文件")
      window.open(baseUrl + '/chart/export')
    }
  },
  mounted() {
    this.calcHeight()
    this.getTableDatas()
    window.onresize = () => {
      this.calcHeight()
    }
  }
})