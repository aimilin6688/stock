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
      <el-form-item label="委托编号" prop="entrustNo">
        <el-input
          v-model="queryParams.entrustNo"
          placeholder="请输入委托编号"
          clearable
          size="small"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
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
          v-hasPermi="['stock:entrust_user:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="entrust_userList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="委托日期" align="center" prop="date" width="140" fixed="left">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.date, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="账号" align="center" prop="account.nickname" />
      <el-table-column label="证券代码" align="center" prop="stockCode" />
      <el-table-column label="证券名称" align="center" prop="stockName" />
      <el-table-column label="委托时间" align="center" prop="entrustTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.entrustTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="委托数量" align="center" prop="num" />
      <el-table-column label="委托仓位" align="center" prop="position" />
      <el-table-column label="委托价格" align="center" prop="price" />
      <el-table-column label="委托类型" align="center" prop="type" :formatter="typeFormat" />
      <el-table-column label="委托编号" align="center" prop="entrustNo" />
      <el-table-column label="状态"     align="center" prop="status" :formatter="statusFormat" />
      <el-table-column label="撤销数量" align="center" prop="cancelNum" />
      <el-table-column label="成交数量" align="center" prop="dealNum" />
      <el-table-column label="成交时间" align="center" prop="dealTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.dealTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="成交编号" align="center" prop="dealNo" />
      <el-table-column label="更新时间" align="center" prop="updateTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.updateTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['stock:entrust_user:edit']"
          >修改</el-button>
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

    <!-- 添加或修改委托消息对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="账号" prop="accountId">
          <el-select v-model="form.accountId" placeholder="请选择账号"  size="small">
            <el-option :label="acc.name" :value="acc.id" v-for="acc in accountList" :key="'acc_2_'+acc.id"/>
          </el-select>
        </el-form-item>
        <el-form-item label="委托日期" prop="date">
          <el-date-picker clearable size="small"
                          v-model="form.date"
                          type="date"
                          value-format="yyyy-MM-dd"
                          placeholder="选择委托日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="证券代码" prop="stockCode">
          <el-input v-model="form.stockCode" placeholder="请输入证券代码" />
        </el-form-item>
        <el-form-item label="证券名称" prop="stockName">
          <el-input v-model="form.stockName" placeholder="请输入证券名称" />
        </el-form-item>
        <el-form-item label="委托数量" prop="num">
          <el-input v-model="form.num" placeholder="请输入委托数量" />
        </el-form-item>
        <el-form-item label="委托仓位" prop="position">
          <el-input v-model="form.position" placeholder="请输入委托仓位" />
        </el-form-item>
        <el-form-item label="委托价格" prop="price">
          <el-input v-model="form.price" placeholder="请输入委托价格" />
        </el-form-item>
        <el-form-item label="委托类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择委托类型">
            <el-option
              v-for="dict in typeOptions"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="parseInt(dict.dictValue)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="委托编号" prop="entrustNo">
          <el-input v-model="form.entrustNo" placeholder="请输入委托编号" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态">
            <el-option
              v-for="dict in statusOptions"
              :key="dict.dictValue"
              :label="dict.dictLabel"
              :value="parseInt(dict.dictValue)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="撤销数量" prop="cancelNum">
          <el-input v-model="form.cancelNum" placeholder="请输入撤销数量" />
        </el-form-item>
        <el-form-item label="成交数量" prop="dealNum">
          <el-input v-model="form.dealNum" placeholder="请输入成交数量" />
        </el-form-item>
        <el-form-item label="成交时间" prop="dealTime">
          <el-date-picker clearable size="small"
                          v-model="form.dealTime"
                          type="date"
                          value-format="yyyy-MM-dd"
                          placeholder="选择成交时间">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="成交编号" prop="dealNo">
          <el-input v-model="form.dealNo" placeholder="请输入成交编号" />
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
import { listAccountSimple } from "@/api/stock/account";
import { listEntrust_user, getEntrust_user, updateEntrust_user, exportEntrust_user } from "@/api/stock/entrust_user";

export default {
  name: "Entrust_user",
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
      // 委托消息表格数据
      entrust_userList: [],
      accountList:[],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 委托类型， 1：买入，0：卖出字典
      typeOptions: [],
      // 状态1：委托中，2：已委托, 3:部分成交. 4:全部成交，-1：撤单，-2：部分撤单字典
      statusOptions: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        accountId: null,
        date: null,
        stockCode: null,
        stockName: null,
        type: null,
        entrustNo: null,
        status: null,
        orderBy: "id desc"
      },
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        accountId: [
          { required: true, message: "账号Id不能为空", trigger: "change" }
        ],
        date: [
          { required: true, message: "委托日期不能为空", trigger: "blur" }
        ],
        stockCode: [
          { required: true, message: "证券代码不能为空", trigger: "blur" }
        ],
        stockName: [
          { required: true, message: "证券名称不能为空", trigger: "blur" }
        ],
      }
    };
  },
  created() {
    this.getList();
    this.getDicts("stock_buy_sell").then(response => {
      this.typeOptions = response.data;
    });
    this.getDicts("stock_entrust_user_status").then(response => {
      this.statusOptions = response.data;
    });
    this.getAccountList();
  },
  methods: {
    /** 查询委托消息列表 */
    getList() {
      this.loading = true;
      listEntrust_user(this.queryParams).then(response => {
        this.entrust_userList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 委托类型， 1：买入，0：卖出字典翻译
    typeFormat(row, column) {
      return this.selectDictLabel(this.typeOptions, row.type);
    },
    // 状态1：委托中，2：已委托, 3:部分成交. 4:全部成交，-1：撤单，-2：部分撤单字典翻译
    statusFormat(row, column) {
      return this.selectDictLabel(this.statusOptions, row.status);
    },
    getAccountList(){
      listAccountSimple({pageNum: 1,pageSize: 1000,orderBy:"id"}).then(res=>{
        this.accountList = res.rows;
      });
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
        accountId: null,
        date: null,
        stockCode: null,
        stockName: null,
        num: null,
        position: null,
        price: null,
        type: null,
        createTime: null,
        entrustNo: null,
        status: null,
        cancelNum: null,
        dealNum: null,
        dealTime: null,
        dealNo: null,
        version: null,
        updateTime: null
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
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const id = row.id || this.ids
      getEntrust_user(id).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改委托消息";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (this.form.id != null) {
            updateEntrust_user(this.form).then(response => {
              this.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          }else{
            this.msgError("不能添加");
          }
        }
      });
    },
    /** 导出按钮操作 */
    handleExport() {
      const queryParams = this.queryParams;
      this.$confirm('是否确认导出所有委托消息数据项?', "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(function() {
        return exportEntrust_user(queryParams);
      }).then(response => {
        this.download(response.msg);
      })
    }
  }
};
</script>
