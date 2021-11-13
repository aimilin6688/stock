<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="账户" prop="accountId">
        <el-select v-model="queryParams.accountId" placeholder="请选择账号" clearable size="small">
          <el-option :label="acc.name" :value="acc.id" v-for="acc in accountList" :key="'acc_2_'+acc.id"/>
        </el-select>
      </el-form-item>
      <el-form-item label="日期" prop="date">
        <el-date-picker
          v-model="daterangeDate"
          size="small"
          style="width: 240px"
          value-format="yyyy-MM-dd"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        ></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="warning"
		  plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['stock:money:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="moneyList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="日期" align="center" prop="date" width="140" fixed="left">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.date, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="账户" align="center" prop="account.nickname" />
      <el-table-column label="总资金" align="center" prop="total" />
      <el-table-column label="可用资金" align="center" prop="available" />
      <el-table-column label="资金余额" align="center" prop="balance" />
      <el-table-column label="股票市值" align="center" prop="market" />
      <el-table-column label="可取资金" align="center" prop="withdraw" />
      <el-table-column label="净值" align="center" prop="netValue" />
      <el-table-column label="最大回测" align="center" prop="maxDrawdown" />
      <el-table-column label="增长率" align="center" prop="increase" />
      <el-table-column label="创建时间" align="center" prop="createTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.createTime) }}</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />
  </div>
</template>

<script>
import { listAccountSimple } from "@/api/stock/account";
import { listMoney,  exportMoney } from "@/api/stock/money";

export default {
  name: "Money",
  components: {
  },
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 资金表格数据
      moneyList: [],
      accountList:[],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 日期时间范围
      daterangeDate: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        accountId: null,
        date: null,
        orderBy: "date desc,accountId desc"
      },
    };
  },
  created() {
    this.getList();
    this.getAccountList();
  },
  methods: {
    /** 查询资金列表 */
    getList() {
      this.loading = true;
      this.queryParams.params = {};
      if (null != this.daterangeDate && '' != this.daterangeDate) {
        this.queryParams.params["beginDate"] = this.daterangeDate[0];
        this.queryParams.params["endDate"] = this.daterangeDate[1];
      }
      listMoney(this.queryParams).then(response => {
        this.moneyList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    getAccountList(){
      listAccountSimple({pageNum: 1,pageSize: 1000,orderBy:"id"}).then(res=>{
        this.accountList = res.rows;
      });
    },

    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.resetForm("queryForm");
      this.handleQuery();
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id)
      this.single = selection.length!==1
      this.multiple = !selection.length
    },
    /** 导出按钮操作 */
    handleExport() {
      const queryParams = this.queryParams;
      this.$confirm('是否确认导出所有资金数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function() {
          return exportMoney(queryParams);
        }).then(response => {
          this.download(response.msg);
        })
    }
  }
};
</script>
