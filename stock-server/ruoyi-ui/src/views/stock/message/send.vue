<template>
  <div class="app-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>发送消息</span>
      </div>
      <div class="text item">
        <el-form ref="form" :model="form" label-width="100px">
          <el-row>
            <el-col :span="8">
              <el-form-item label="消息类型">
                <el-select v-model="form.type" placeholder="请选择消息类型" clearable @change="handleMessageTypeChange">
                  <el-option
                    v-for="dict in typeOptions"
                    :key="dict.dictValue"
                    :label="dict.dictLabel"
                    :value="dict.dictValue"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="账户状态">
                <el-select v-model="form.status" placeholder="请选择账户状态" clearable @change="handleStatusChange">
                  <el-option
                    v-for="dict in statusOptions"
                    :key="dict.value"
                    :label="dict.label"
                    :value="dict.value"
                  />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="24">
              <el-form-item label="选择券商">
                <el-card class="select_broker" shadow="hover">
                  <el-checkbox-group v-model="checkedBrokers" @change="handleCheckedBrokersChange">
                    <el-checkbox :label="b" v-for="b in brokerList" :key="b"/>
                  </el-checkbox-group>
                </el-card>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="24">
              <el-form-item label="选择账户">
                <el-card class="select_broker" shadow="hover">
                  <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
                  <el-checkbox-group v-model="checkedAccounts" @change="handleCheckedAccountsChange">
                    <el-checkbox :label="a.id" v-for="a in showAccountList" :key="'c_acc_'+a.id">{{ a.name }}</el-checkbox>
                  </el-checkbox-group>
                </el-card>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row v-show="showBuyOrSell">
            <el-col :span="24">
              <el-form-item label="买入、卖出">
                <el-card class="select_broker" shadow="hover">
                  <div slot="header" class="clearfix">
                    <el-button type="text" @click="handleAddDialog">添加</el-button>
                  </div>
                  <el-table :data="buyOrSellList">
                    <el-table-column label="证券代码" align="center" prop="code"/>
                    <el-table-column label="证券名称" align="center" prop="name"/>
                    <el-table-column label="操作" align="center" prop="operation" :formatter="buyOrSellTypeOptionsFormat"/>
                    <el-table-column label="价格" align="center" prop="price"/>
                    <el-table-column label="股数" align="center" prop="number"/>
                    <el-table-column label="仓位" align="center" prop="position"/>
                    <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
                      <template slot-scope="scope">
                        <el-button  size="mini"  type="text"  icon="el-icon-edit"  @click="handleUpdate(scope.row)">编辑</el-button>
                        <el-button  size="mini"  type="text"  icon="el-icon-delete"  @click="handleDelete(scope.row)">删除</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-card>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row v-show="showEntrustCancel">
            <el-col :span="24">
              <el-form-item label="撤销委托">
                <el-card class="select_broker" shadow="hover">
                  <el-row>
                    <el-col :span="8">
                      <el-form-item label="撤单类型" prop="operation">
                        <el-select v-model="entrustCancelFrom.type" placeholder="请选择撤单类型">
                          <el-option v-for="dict in entrustCancelOptions"   :key="dict.value"   :label="dict.label"  :value="dict.value" />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="证券代码" prop="stockCodes">
                        <el-input v-model="entrustCancelFrom.stockCodes" type="textarea" placeholder="请输入证券代码多个逗号分隔" />
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="委托单号" prop="entrustNos">
                        <el-input v-model="entrustCancelFrom.entrustNos" type="textarea" placeholder="请输入委托单号多个逗号分隔" />
                      </el-form-item>
                    </el-col>
                  </el-row>
                </el-card>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item size="large">
            <el-button type="primary" @click="onSubmit">发送</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>


    <!-- 添加或修改券商对话框 -->
    <el-dialog title="买入卖出" :visible.sync="showBuyOrSellOpen" width="500px" :append-to-body="true" :close-on-click-modal="false">
      <el-form ref="buyOrSellForm" :model="buyOrSellForm" :rules="buyOrSellRules" label-width="80px">
        <el-form-item label="证券代码" prop="code">
          <el-input v-model="buyOrSellForm.code" placeholder="请输入证券代码" />
        </el-form-item>
        <el-form-item label="证券名称" prop="name">
          <el-input v-model="buyOrSellForm.name" placeholder="请输入证券名称" />
        </el-form-item>
        <el-form-item label="操作" prop="operation">
          <el-select v-model="buyOrSellForm.operation" placeholder="请选择操作类型">
            <el-option v-for="dict in buyOrSellTypeOptions"   :key="dict.dictValue"   :label="dict.dictLabel"  :value="dict.dictValue" />
          </el-select>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input v-model.number="buyOrSellForm.price" placeholder="请输入价格" type="number" min="0.01" step="0.01"/>
        </el-form-item>
        <el-form-item label="股数" prop="number">
          <el-input v-model="buyOrSellForm.number" placeholder="请输入股数" type="number" min="1" step="1" />
        </el-form-item>
        <el-form-item label="仓位" prop="position">
          <el-input v-model="buyOrSellForm.position" placeholder="请输入仓位%" type="number" min="0.00" max="100.00" step="1.00"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleAdd">确 定</el-button>
        <el-button @click="handleCancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listAccountSimple } from '@/api/stock/account'
import {sendBaseMessage} from '@/api/stock/message'
import { isNumberStr } from '@/utils'

export default {
  name: 'Message_send',
  components: {},
  data() {
    return {
      accountList: [],
      form: {},
      typeOptions: [],
      brokerList: [],
      statusName: 'statusAll',
      statusOptions: [
        { label: '可债券', value: 'creditorStatus' },
        { label: '可下单', value: 'orderStatus' },
        { label: '可报告', value: 'reportStatus' },
        { label: '已启用', value: 'status' }],
      entrustCancelOptions:[
        { label: '撤指定', value: 0 },
        { label: '撤全部', value: 1 },
        { label: '撤买入', value: 2 },
        { label: '撤卖出', value: 3 },
      ],
      showAccountList: [],
      checkedBrokers: [],
      isIndeterminate: false,
      checkAll: false,
      checkedAccounts: [],  // 所有选中的账户
      showBuyOrSell: false, // 买入或者卖出展示
      showEntrustCancel: false, // 撤销委托展示
      buyOrSellList: [],//买入卖出股票信息
      showBuyOrSellOpen: false,
      buyOrSellForm:{},
      buyOrSellRules: {
        code: [
          { required: true, message: "证券代码不能为空", trigger: "blur" }
        ],
        operation:[
          { required: true, message: '请选择操作类型', trigger: 'change'}
        ],
        price:[
          {required: true, message: '请输入价格', trigger: 'blur'},
          { type: 'number', message: '价格必须为数字值'}
        ],
        number:[
          { validator: this.checkNumber, trigger: 'blur' },
          { validator: this.checkNumberOrPosition, trigger: 'blur' }
        ],
        position:[
          { validator: this.checkNumberOrPosition, trigger: 'blur' }
        ]
      },
      buyOrSellIndex: 1,
      // 委托类型字典
      buyOrSellTypeOptions: [],
      entrustCancelFrom:{},
    }
  },
  created() {
    this.getAccountList()
    this.getDicts('stock_message_base_type').then(response => {
      this.typeOptions = response.data
    })
    this.getDicts("stock_buy_sell").then(response => {
      this.buyOrSellTypeOptions = response.data;
    });
  },
  methods: {
    initData() {
      this.checkAll = false
      this.brokerList = []
      this.accountList = []
      this.form = {}
      this.showAccountList = []
      this.checkedBrokers = []
      this.isIndeterminate = false
      this.checkedAccounts = []
    },
    getAccountList() {
      this.initData()
      let _this = this
      let query = { pageNum: 1, pageSize: 1000, orderBy: 'id', status: 1 }
      query[this.statusName] = 1
      listAccountSimple(query).then(res => {
        this.accountList = res.rows
        this.showAccountList = res.rows
        this.showAccountList.forEach(c => {
          _this.brokerList.push(c.brokerName)
        })
      })
    },
    // 委托类型字典翻译
    buyOrSellTypeOptionsFormat(row, column) {
      return this.selectDictLabel(this.buyOrSellTypeOptions, row.operation);
    },
    handleStatusChange(value) {
      this.statusName = value
      this.getAccountList()
    },
    // 消息类型字典翻译
    typeFormat(row, column) {
      return this.selectDictLabel(this.typeOptions, row.type)
    },
    // 提交数据
    onSubmit() {
      if (this.checkedAccounts.length === 0) {
        this.msgError('请选择账户')
        return false
      }
      // 发送消息的账户
      this.form.accountIds = this.checkedAccounts;
      this.form.buyOrSellList = this.buyOrSellList;
      this.form.entrustCancel = this.entrustCancelFrom;
      sendBaseMessage(this.form).then(res=>{
        this.msgSuccess(res.msg);
      });
    },
    // 券商选择
    handleCheckedBrokersChange(val) {
      this.showAccountList = []
      if (val.length === 0) {
        this.showAccountList = this.accountList.slice(0) // 复制数组对象
      } else {
        this.showAccountList = this.accountList.filter(c => val.indexOf(c.brokerName) !== -1)
      }
      this.handleCheckedAccountsChange(this.checkedAccounts)
    },
    handleCheckAllChange(val) {
      let _this = this
      _this.checkedAccounts = []
      if (val) {
        this.showAccountList.forEach(({ id }) => {
          _this.checkedAccounts.push(id)
        })
      }
      this.isIndeterminate = false
    },
    handleCheckedAccountsChange(value) {
      let checkedCount = value.length
      this.checkAll = checkedCount === this.showAccountList.length
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.showAccountList.length
    },
    // 消息类型修改
    handleMessageTypeChange(value) {
      this.showBuyOrSell = false
      this.showEntrustCancel = false
      // 类型：2 登录，3:退出登录,4:资金查询,5:买入，6：卖出，7：持仓，8：成交，9：委托，10：撤销委托
      if (value === '5' || value === '6') {
        this.showBuyOrSell = true
      } else if (value === '10') {
        this.showEntrustCancel = true
      }
    },

    // 买入卖出弹框
    handleAddDialog(){
      this.buyOrSellReset();
      this.showBuyOrSellOpen = true;
    },
    handleCancel(){
      this.buyOrSellReset();
      this.showBuyOrSellOpen = false;
    },
    buyOrSellReset(){
      this.buyOrSellForm = {
        id: null,
        code: '',
        name: '',
        operation: null,
        price: null,
        number: null,
        position: null,
      };
      this.resetForm("buyOrSellForm");
    },
    handleAdd(){
      this.$refs["buyOrSellForm"].validate((valid) => {
        if (valid) {
          let form = JSON.parse(JSON.stringify(this.buyOrSellForm));
          if(form.id == null){// 添加
            form.id = this.buyOrSellIndex++;
            this.buyOrSellList.push(form);
          }else{// 更新
            let currentIndex = null, currentId = form.id;
            this.buyOrSellList.forEach((c,index)=>{ if(c.id === currentId){ currentIndex = send; } });
            this.buyOrSellList.splice(currentIndex,1, form);
          }
          this.handleCancel();
        }
      });

    },
    handleDelete(row){
      this.buyOrSellList.splice(this.buyOrSellList.indexOf(row),1);
    },
    handleUpdate(row){
      this.buyOrSellForm = JSON.parse(JSON.stringify(row));
      this.showBuyOrSellOpen = true;
    },
    checkNumber(rule, value, callback){
      let opt = this.buyOrSellForm.operation;
      if (isNumberStr(value) && opt === '1' && parseInt(value) % 100.0 !== 0) {
          callback(new Error('买入股数必须为100整数倍'))
      } else {
        callback()
      }
    },
    checkNumberOrPosition(rule, value, callback){
      let number = this.buyOrSellForm.number;
      let position = this.buyOrSellForm.position;
      if(rule['field'] === "position" && isNumberStr(position)){
        position = parseFloat(position);
        if(position < 0 || position > 100){
          callback(new Error('仓位必须大于0小于100'));
          return;
        }
      }
      if((number == null || number === '') && (position == null || position === "")){
        callback(new Error('股数或仓位二选一'));
      }else{
        callback();
      }
    }
  }
}
</script>
<style scoped lang="scss">
  .box-card {
}
</style>
