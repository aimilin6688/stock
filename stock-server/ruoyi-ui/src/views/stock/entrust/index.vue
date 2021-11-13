<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="账户" prop="accountId">
        <el-select v-model="queryParams.accountId" placeholder="请选择账号" clearable size="small">
          <el-option :label="acc.name" :value="acc.id" v-for="acc in accountList" :key="'acc_2_'+acc.id"/>
        </el-select>
      </el-form-item>
      <el-form-item label="委托日期" prop="date">
        <el-date-picker clearable size="small"
                        v-model="queryParams.date"
                        type="date"
                        value-format="yyyy-MM-dd"
                        placeholder="选择委托日期">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="证券代码" prop="stockCode">
        <el-input
          v-model="queryParams.stockCode"
          placeholder="请输入证券代码"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="证券名称" prop="stockName">
        <el-input
          v-model="queryParams.stockName"
          placeholder="请输入证券名称"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="委托编号" prop="entrustNo">
        <el-input
          v-model="queryParams.entrustNo"
          placeholder="请输入委托编号"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="委托类型" prop="type">
        <el-select v-model="queryParams.type" placeholder="请选择委托类型" clearable size="small">
          <el-option
            v-for="dict in typeOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
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
          v-hasPermi="['stock:entrust:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="entrustList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="委托日期" align="center" prop="date" width="140" fixed="left">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.date, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="账户" align="center" prop="account.reportName" />
      <el-table-column label="证券代码" align="center" prop="stockCode" />
      <el-table-column label="证券名称" align="center" prop="stockName" />
      <el-table-column label="委托编号" align="center" prop="entrustNo" />
      <el-table-column label="委托日期" align="center" prop="entrustDate" />
      <el-table-column label="委托时间" align="center" prop="entrustTime" />
      <el-table-column label="委托类型" align="center" prop="type" :formatter="typeFormat" />
      <el-table-column label="委托数量" align="center" prop="num" />
      <el-table-column label="委托价格" align="center" prop="price" />
      <el-table-column label="成交数量" align="center" prop="dealNum" />
      <el-table-column label="成交均价" align="center" prop="dealPrice" />
      <el-table-column label="备注" align="center" prop="remark" />
      <el-table-column label="股东代码" align="center" prop="stockHolder" />
      <el-table-column label="交易市场" align="center" prop="tradingMarket" />
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
import { listEntrust, getEntrust, exportEntrust } from "@/api/stock/entrust";

export default {
  name: "Entrust",
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
      // 委托表格数据
      entrustList: [],
      accountList:[],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 委托类型字典
      typeOptions: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        accountId: null,
        date: null,
        stockCode: null,
        stockName: null,
        entrustNo: null,
        type: null,
        orderBy: "date desc,accountId desc"
      },
    };
  },
  created() {
    this.getList();
    this.getDicts("stock_buy_sell").then(response => {
      this.typeOptions = response.data;
    });
    this.getAccountList();
  },
  methods: {
    /** 查询委托列表 */
    getList() {
      this.loading = true;
      listEntrust(this.queryParams).then(response => {
        this.entrustList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 委托类型字典翻译
    typeFormat(row, column) {
      return this.selectDictLabel(this.typeOptions, row.type);
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
    handleExport() {
      const queryParams = this.queryParams;
      this.$confirm('是否确认导出所有委托数据项?', "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(function() {
        return exportEntrust(queryParams);
      }).then(response => {
        this.download(response.msg);
      })
    }
  }
};
</script>
