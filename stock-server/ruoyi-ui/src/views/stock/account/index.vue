<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择状态" clearable size="small">
          <el-option
            v-for="dict in statusOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="账户类型" prop="type">
        <el-select v-model="queryParams.type" placeholder="请选择账户类型" clearable size="small">
          <el-option
            v-for="dict in typeOptions"
            :key="dict.dictValue"
            :label="dict.dictLabel"
            :value="dict.dictValue"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="客户端" prop="clientId">
        <el-select v-model="queryParams.clientId" placeholder="请选择客户端" clearable size="small">
          <el-option v-for="c in listClientAll" :key="'c+'+c.id" :label="c.name" :value="c.id"/>
        </el-select>
      </el-form-item>
      <el-form-item label="券商" prop="brokerId">
        <el-select v-model="queryParams.brokerId" placeholder="请选择券商" clearable size="small">
          <el-option v-for="broker in listBrokerOptions"
                     :key="'broker_q'+broker.id" :label="broker.name" :value="broker.id"/>
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
          type="primary"
		  plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['stock:account:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
		  plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['stock:account:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
		  plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['stock:account:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
		  plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['stock:account:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="accountList" @selection-change="handleSelectionChange" @sort-change="sortChange">
      <el-table-column type="selection" width="45" align="center" />
      <el-table-column label="ID" align="center" prop="id" sortable="custom"/>
      <el-table-column label="用户名" align="center" prop="username" />
      <el-table-column label="昵称" align="center" prop="nickname" />
      <el-table-column label="报告名称" align="center" prop="reportName" />
      <el-table-column label="状态" align="center" prop="status" :formatter="statusFormat" />
      <el-table-column label="其他状态" align="center" width="100">
        <template slot-scope="scope" >
            下单：{{orderStatusFormat(scope.row)}}<br>
            债券：{{creditorStatusFormat(scope.row)}}<br>
            报告：{{reportStatusFormat(scope.row)}}<br>
        </template>
      </el-table-column>
      <el-table-column label="账户类型" align="center" prop="type" :formatter="typeFormat" />
      <el-table-column label="客户端" align="center" prop="client.name" />
      <el-table-column label="券商" align="center" prop="broker.name" />
      <el-table-column label="更新时间" align="center" prop="updateTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.updateTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="排序" align="center" prop="sort" sortable="custom"/>
      <el-table-column label="置顶" align="center" prop="top" >
        <template slot-scope="scope">
          <label v-if="scope.row.top == 1">是</label>
          <label v-else>否</label>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="100">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['stock:account:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['stock:account:remove']"
          >删除</el-button>
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

    <!-- 添加或修改下单账户对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body :close-on-click-modal="false">
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" placeholder="请输入密码" type="password"/>
        </el-form-item>
        <el-form-item label="通信密码" prop="comPassword">
          <el-input v-model="form.comPassword" placeholder="请输入通信密码" type="password"/>
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="请输入昵称" />
        </el-form-item>
        <el-form-item label="报告名称" prop="reportName">
          <el-input v-model="form.reportName" placeholder="请输入报告名称" />
        </el-form-item>
        <el-form-item label="债券状态">
          <el-radio-group v-model="form.creditorStatus">
            <el-radio
              v-for="dict in creditorStatusOptions"
              :key="dict.dictValue"
              :label="parseInt(dict.dictValue)"
            >{{dict.dictLabel}}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="下单状态">
          <el-radio-group v-model="form.orderStatus">
            <el-radio
              v-for="dict in orderStatusOptions"
              :key="dict.dictValue"
              :label="parseInt(dict.dictValue)"
            >{{dict.dictLabel}}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="报告状态">
          <el-radio-group v-model="form.reportStatus">
            <el-radio
              v-for="dict in reportStatusOptions"
              :key="dict.dictValue"
              :label="parseInt(dict.dictValue)"
            >{{dict.dictLabel}}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio
              v-for="dict in statusOptions"
              :key="dict.dictValue"
              :label="parseInt(dict.dictValue)"
            >{{dict.dictLabel}}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="账户类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择账户类型">
            <el-option
              v-for="dict in typeOptions"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="parseInt(dict.dictValue)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="券商" prop="brokerId">
          <el-select v-model="form.brokerId" placeholder="请选择券商"  @change="queryClient">
            <el-option v-for="broker in listBrokerOptions"
                       :key="'broker'+broker.id" :label="broker.name" :value="broker.id"/>
          </el-select>
        </el-form-item>
        <el-form-item label="客户端" prop="clientId">
          <el-select v-model="form.clientId" placeholder="请选择客户端">
            <el-option v-for="client in listClientOptions" :key="'client'+client.id" :label="client.name" :value="client.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input v-model="form.sort" placeholder="请输入排序，越大越靠前" type="number"/>
        </el-form-item>
        <el-form-item label="置顶" prop="top">
            <el-radio-group v-model="form.top">
              <el-tooltip content="置顶，决定报告顺序" placement="top">
                <el-radio  :label="1">是</el-radio>
              </el-tooltip>
              <el-radio  :label="0">否</el-radio>
            </el-radio-group>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listAccount, getAccount, delAccount, addAccount, updateAccount, exportAccount } from "@/api/stock/account";
import { listClientByBrokerId, listClient } from "@/api/stock/client";
import { listBroker } from "@/api/stock/broker";
export default {
  name: "Account",
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
      // 下单账户表格数据
      accountList: [],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 债券状态字典
      creditorStatusOptions: [],
      // 下单状态字典
      orderStatusOptions: [],
      // 报告状态字典
      reportStatusOptions: [],
      // 状态字典
      statusOptions: [],
      // 账户类型字典
      typeOptions: [],
      listBrokerOptions:[],
      listClientAll:[],
      listClientOptions:[],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        status: null,
        type: null,
        clientId: null,
        brokerId: null,
        orderBy: 'top desc,sort desc'
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        username: [
          { required: true, message: "用户名不能为空", trigger: "blur" }
        ],
        password: [
          { required: true, message: "密码不能为空", trigger: "blur" }
        ],
        nickname: [
          { required: true, message: "昵称不能为空", trigger: "blur" }
        ],
        type: [
          { required: true, message: "账户类型不能为空", trigger: "change" }
        ],
      }
    };
  },
  created() {
    this.getList();
    this.getDicts("stock_status").then(response => {
      this.creditorStatusOptions = response.data;
      this.orderStatusOptions = response.data;
      this.reportStatusOptions = response.data;
      this.statusOptions = response.data;
    });
    this.getDicts("stock_account_type").then(response => {
      this.typeOptions = response.data;
    });
    this.brokerOptions();
    listClient({pageNum:1,pageSize: 100}).then(res=>{
      this.listClientAll = res.rows;
    });
  },
  methods: {
    /** 查询下单账户列表 */
    getList() {
      this.loading = true;
      listAccount(this.queryParams).then(response => {
        this.accountList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 排序
    sortChange(sort){
      let sortDesc = sort.order === "descending" ? "desc" : sort.order === "ascending"?"asc": "";
      sortDesc = sortDesc === "" ? "top desc,sort desc":sort.prop + " " + sortDesc;
      this.queryParams.orderBy = sortDesc;
      this.handleQuery();
    },
    // 加载券商信息
    brokerOptions(){
      this.listBrokerOptions.slice(0,this.listBrokerOptions.length);
      listBroker({ pageNum: 1, pageSize: 1000}).then(res=>{
        this.listBrokerOptions = res.rows;
      });
    },
    // 查询客户端信息
    queryClient(brokerId){
      this.listClientOptions.slice(0,this.listClientOptions.length);
      listClientByBrokerId(brokerId).then(res=>{
        this.listClientOptions = res.data;
      });
    },
    // 债券状态字典翻译
    creditorStatusFormat(row, column) {
      return this.selectDictLabel(this.creditorStatusOptions, row.creditorStatus);
    },
    // 下单状态字典翻译
    orderStatusFormat(row, column) {
      return this.selectDictLabel(this.orderStatusOptions, row.orderStatus);
    },
    // 报告状态字典翻译
    reportStatusFormat(row, column) {
      return this.selectDictLabel(this.reportStatusOptions, row.reportStatus);
    },
    // 状态字典翻译
    statusFormat(row, column) {
      return this.selectDictLabel(this.statusOptions, row.status);
    },
    // 账户类型字典翻译
    typeFormat(row, column) {
      return this.selectDictLabel(this.typeOptions, row.type);
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        id: null,
        username: null,
        password: null,
        comPassword: null,
        nickname: null,
        reportName: null,
        creditorStatus: 0,
        orderStatus: 0,
        reportStatus: 0,
        status: 0,
        type: null,
        clientId: null,
        brokerId: null,
        createTime: null,
        updateTime: null,
        sort: 0,
        top: 0
      };
      this.resetForm("form");
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
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加下单账户";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const id = row.id || this.ids
      getAccount(id).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改下单账户";
        this.queryClient(this.form.brokerId);
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.id != null) {
            updateAccount(this.form).then(response => {
              this.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addAccount(this.form).then(response => {
              this.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const ids = row.id || this.ids;
      this.$confirm('是否确认删除下单账户编号为"' + ids + '"的数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function() {
          return delAccount(ids);
        }).then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        })
    },
    /** 导出按钮操作 */
    handleExport() {
      const queryParams = this.queryParams;
      this.$confirm('是否确认导出所有下单账户数据项?', "警告", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }).then(function() {
          return exportAccount(queryParams);
        }).then(response => {
          this.download(response.msg);
        })
    }
  }
};
</script>
