<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="消息ID" prop="id">
        <el-input
          v-model="queryParams.id"
          placeholder="请输入消息ID"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="账户" prop="accountId">
        <el-select v-model="queryParams.accountId" placeholder="请选择账号" clearable size="small">
          <el-option :label="acc.name" :value="acc.id" v-for="acc in accountList" :key="'acc_2_'+acc.id"/>
        </el-select>
      </el-form-item>
      <el-form-item label="消息类型" prop="type">
        <el-select v-model="queryParams.type" placeholder="请选择消息类型" clearable size="small">
          <el-option
            v-for="dict in typeOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="消息状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择消息状态" clearable size="small">
          <el-option
            v-for="dict in statusOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="已执行?" prop="executed">
        <el-select v-model="queryParams.executed" placeholder="请选择是否已执行" clearable size="small">
          <el-option
            v-for="dict in executedOptions"
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
          v-hasPermi="['stock:message:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="messageList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="消息ID" align="center" prop="id" />
      <el-table-column label="账户" align="center" prop="account.nickname" />
      <el-table-column label="消息类型" align="center" prop="type" :formatter="typeFormat" />
      <el-table-column label="消息标题" align="center" prop="subject" />
      <el-table-column label="创建时间" align="center" prop="createTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.createTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="签收时间" align="center" prop="signTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.signTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="客户端" align="center" prop="clientName" />
      <el-table-column label="消息权重" align="center" prop="weight" />
      <el-table-column label="消息状态" align="center" prop="status" :formatter="statusFormat" />
      <el-table-column label="已执行?" align="center" prop="executed" :formatter="executedFormat" />
      <el-table-column label="执行时间" align="center" prop="executedTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.executedTime) }}</span>
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
import { listMessage, getMessage, exportMessage } from "@/api/stock/message";

export default {
  name: "Message",
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
      // 消息记录表格数据
      messageList: [],
      accountList:[],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 消息类型字典
      typeOptions: [],
      // 消息状态：0：未发送，1:已发送, 2:已签收字典
      statusOptions: [],
      // 是否已经执行，1：已执行，0:未执行字典
      executedOptions: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        id: null,
        accountId: null,
        type: null,
        signClientId: null,
        status: null,
        executed: null,
        orderBy: "id desc",
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
      }
    };
  },
  created() {
    this.getList();
    this.getDicts("stock_message_base_type").then(response => {
      this.typeOptions = response.data;
    });
    this.getDicts("stock_message_send_status").then(response => {
      this.statusOptions = response.data;
    });
    this.getDicts("stock_message_exe_result").then(response => {
      this.executedOptions = response.data;
    });
    this.getAccountList();
  },
  methods: {
    /** 查询消息记录列表 */
    getList() {
      this.loading = true;
      listMessage(this.queryParams).then(response => {
        this.messageList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 消息类型字典翻译
    typeFormat(row, column) {
      return this.selectDictLabel(this.typeOptions, row.type);
    },
    // 消息状态：0：未发送，1:已发送, 2:已签收字典翻译
    statusFormat(row, column) {
      return this.selectDictLabel(this.statusOptions, row.status);
    },
    // 是否已经执行，1：已执行，0:未执行字典翻译
    executedFormat(row, column) {
      return this.selectDictLabel(this.executedOptions, row.executed);
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
      this.$confirm('是否确认导出所有消息记录数据项?', "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(function() {
        return exportMessage(queryParams);
      }).then(response => {
        this.download(response.msg);
      })
    }
  }
};
</script>
